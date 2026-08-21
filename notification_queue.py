"""
LocalKard Notification Queue System
Non-blocking, async notification delivery with retry logic
"""

import json
import threading
import queue
import time
from datetime import datetime, timedelta
from typing import Dict, Optional, Callable
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum


# ============================================================================
# NOTIFICATION TYPES
# ============================================================================

class NotificationType(Enum):
    """Notification event types"""
    POINTS_EARNED = "points_earned"
    POINTS_REDEEMED = "points_redeemed"
    TIER_UPGRADE = "tier_upgrade"
    BALANCE_INQUIRY = "balance_inquiry"
    REFERRAL_REWARD = "referral_reward"
    WELCOME = "welcome"
    CUSTOM = "custom"


@dataclass
class Notification:
    """Notification data structure"""
    type: NotificationType
    customer_phone: str
    merchant_id: str
    merchant_name: str
    data: Dict
    language: str = 'en'
    priority: int = 5  # 1=highest, 10=lowest
    retry_count: int = 0
    max_retries: int = 3
    created_at: str = None
    scheduled_at: str = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
        if self.scheduled_at is None:
            self.scheduled_at = datetime.now().isoformat()

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'type': self.type.value,
            'customer_phone': self.customer_phone,
            'merchant_id': self.merchant_id,
            'merchant_name': self.merchant_name,
            'data': self.data,
            'language': self.language,
            'priority': self.priority,
            'retry_count': self.retry_count,
            'max_retries': self.max_retries,
            'created_at': self.created_at,
            'scheduled_at': self.scheduled_at
        }


# ============================================================================
# NOTIFICATION QUEUE
# ============================================================================

class NotificationQueue:
    """Thread-safe notification queue with retry logic"""

    def __init__(self, worker_threads: int = 2, persist: bool = True,
                 persist_dir: str = 'central_data'):
        """
        Initialize notification queue

        Args:
            worker_threads: Number of worker threads for processing
            persist: Whether to persist queue to disk
            persist_dir: Directory for persisting queue
        """
        self.queue = queue.PriorityQueue()
        self.worker_threads = worker_threads
        self.persist = persist
        self.persist_dir = Path(persist_dir)
        self.queue_file = self.persist_dir / 'notification_queue.json'
        self.failed_file = self.persist_dir / 'notification_failed.json'

        self.workers = []
        self.running = False
        self.handler = None
        self.stats = {
            'total_queued': 0,
            'total_processed': 0,
            'total_failed': 0,
            'total_retried': 0
        }

        # Ensure persist directory exists
        if persist:
            self.persist_dir.mkdir(exist_ok=True)
            self._load_persisted_queue()

    def set_handler(self, handler: Callable[[Notification], Dict]):
        """
        Set notification handler function

        Args:
            handler: Function that takes Notification and returns result Dict
        """
        self.handler = handler

    def enqueue(self, notification: Notification) -> bool:
        """
        Add notification to queue

        Args:
            notification: Notification object

        Returns:
            True if successfully queued
        """
        try:
            # Priority queue uses (priority, item) tuples
            self.queue.put((notification.priority, notification))
            self.stats['total_queued'] += 1

            # Persist queue
            if self.persist:
                self._persist_queue()

            return True
        except Exception as e:
            print(f"Error enqueueing notification: {e}")
            return False

    def start_workers(self):
        """Start background worker threads"""
        if self.running:
            print("Workers already running")
            return

        if not self.handler:
            raise ValueError("Handler not set. Call set_handler() first.")

        self.running = True

        for i in range(self.worker_threads):
            worker = threading.Thread(
                target=self._worker_loop,
                name=f"NotificationWorker-{i+1}",
                daemon=True
            )
            worker.start()
            self.workers.append(worker)

        print(f"✅ Started {self.worker_threads} notification worker threads")

    def stop_workers(self):
        """Stop all worker threads gracefully"""
        self.running = False

        # Wait for workers to finish
        for worker in self.workers:
            worker.join(timeout=5)

        self.workers.clear()
        print("✅ Stopped notification workers")

    def _worker_loop(self):
        """Worker thread main loop"""
        while self.running:
            try:
                # Get notification with timeout
                priority, notification = self.queue.get(timeout=1)

                # Check if scheduled time has arrived
                scheduled = datetime.fromisoformat(notification.scheduled_at)
                if datetime.now() < scheduled:
                    # Re-queue if not yet time
                    time.sleep(0.5)
                    self.queue.put((priority, notification))
                    continue

                # Process notification
                result = self._process_notification(notification)

                if result.get('success'):
                    self.stats['total_processed'] += 1
                else:
                    # Retry logic
                    if notification.retry_count < notification.max_retries:
                        notification.retry_count += 1
                        # Exponential backoff: 2^retry_count minutes
                        delay_minutes = 2 ** notification.retry_count
                        notification.scheduled_at = (
                            datetime.now() + timedelta(minutes=delay_minutes)
                        ).isoformat()

                        self.queue.put((priority, notification))
                        self.stats['total_retried'] += 1
                        print(f"⚠️ Retry {notification.retry_count}/{notification.max_retries} "
                              f"scheduled in {delay_minutes} minutes")
                    else:
                        # Max retries exceeded
                        self.stats['total_failed'] += 1
                        self._log_failed_notification(notification, result)
                        print(f"❌ Failed after {notification.max_retries} retries")

                self.queue.task_done()

                # Persist queue state
                if self.persist:
                    self._persist_queue()

            except queue.Empty:
                # No items in queue, continue
                continue
            except Exception as e:
                print(f"Error in worker loop: {e}")
                time.sleep(1)

    def _process_notification(self, notification: Notification) -> Dict:
        """Process a single notification"""
        try:
            if not self.handler:
                return {'success': False, 'error': 'No handler set'}

            print(f"📤 Processing {notification.type.value} for {notification.customer_phone}")
            result = self.handler(notification)
            return result
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _persist_queue(self):
        """Persist queue to disk"""
        try:
            # Extract all items from queue (this is not thread-safe in production)
            items = []
            temp_queue = queue.PriorityQueue()

            while not self.queue.empty():
                try:
                    item = self.queue.get_nowait()
                    items.append(item)
                    temp_queue.put(item)
                except queue.Empty:
                    break

            # Restore queue
            self.queue = temp_queue

            # Save to file
            queue_data = {
                'notifications': [
                    {'priority': priority, 'notification': notif.to_dict()}
                    for priority, notif in items
                ],
                'stats': self.stats,
                'timestamp': datetime.now().isoformat()
            }

            with open(self.queue_file, 'w') as f:
                json.dump(queue_data, f, indent=2)

        except Exception as e:
            print(f"Warning: Failed to persist queue: {e}")

    def _load_persisted_queue(self):
        """Load persisted queue from disk"""
        try:
            if not self.queue_file.exists():
                return

            with open(self.queue_file, 'r') as f:
                queue_data = json.load(f)

            # Restore notifications
            for item in queue_data.get('notifications', []):
                priority = item['priority']
                notif_data = item['notification']

                # Reconstruct notification object
                notification = Notification(
                    type=NotificationType(notif_data['type']),
                    customer_phone=notif_data['customer_phone'],
                    merchant_id=notif_data['merchant_id'],
                    merchant_name=notif_data['merchant_name'],
                    data=notif_data['data'],
                    language=notif_data.get('language', 'en'),
                    priority=notif_data.get('priority', 5),
                    retry_count=notif_data.get('retry_count', 0),
                    max_retries=notif_data.get('max_retries', 3),
                    created_at=notif_data.get('created_at'),
                    scheduled_at=notif_data.get('scheduled_at')
                )

                self.queue.put((priority, notification))

            # Restore stats
            self.stats = queue_data.get('stats', self.stats)

            print(f"📥 Loaded {len(queue_data.get('notifications', []))} persisted notifications")

        except Exception as e:
            print(f"Warning: Failed to load persisted queue: {e}")

    def _log_failed_notification(self, notification: Notification, result: Dict):
        """Log failed notification for manual review"""
        try:
            failed_logs = []
            if self.failed_file.exists():
                with open(self.failed_file, 'r') as f:
                    failed_logs = json.load(f)

            failed_logs.append({
                'notification': notification.to_dict(),
                'result': result,
                'failed_at': datetime.now().isoformat()
            })

            # Keep only last 500 failed notifications
            if len(failed_logs) > 500:
                failed_logs = failed_logs[-500:]

            with open(self.failed_file, 'w') as f:
                json.dump(failed_logs, f, indent=2)

        except Exception as e:
            print(f"Warning: Failed to log failed notification: {e}")

    def get_stats(self) -> Dict:
        """Get queue statistics"""
        return {
            **self.stats,
            'queue_size': self.queue.qsize(),
            'workers_running': len(self.workers),
            'workers_active': self.running
        }

    def clear_queue(self):
        """Clear all pending notifications"""
        while not self.queue.empty():
            try:
                self.queue.get_nowait()
                self.queue.task_done()
            except queue.Empty:
                break

        print("✅ Queue cleared")


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def create_points_earned_notification(customer_phone: str, merchant_id: str,
                                     merchant_name: str, points: float,
                                     balance: float, tier: str,
                                     language: str = 'en') -> Notification:
    """Create points earned notification"""
    return Notification(
        type=NotificationType.POINTS_EARNED,
        customer_phone=customer_phone,
        merchant_id=merchant_id,
        merchant_name=merchant_name,
        data={
            'points': points,
            'balance': balance,
            'tier': tier
        },
        language=language,
        priority=3  # Medium-high priority
    )


def create_tier_upgrade_notification(customer_phone: str, merchant_id: str,
                                    merchant_name: str, new_tier: str,
                                    multiplier: float, balance: float,
                                    language: str = 'en') -> Notification:
    """Create tier upgrade notification"""
    return Notification(
        type=NotificationType.TIER_UPGRADE,
        customer_phone=customer_phone,
        merchant_id=merchant_id,
        merchant_name=merchant_name,
        data={
            'new_tier': new_tier,
            'multiplier': multiplier,
            'balance': balance
        },
        language=language,
        priority=1  # Highest priority - celebrate immediately!
    )


def create_redemption_notification(customer_phone: str, merchant_id: str,
                                  merchant_name: str, points: float,
                                  value: float, balance: float,
                                  language: str = 'en') -> Notification:
    """Create redemption notification"""
    return Notification(
        type=NotificationType.POINTS_REDEEMED,
        customer_phone=customer_phone,
        merchant_id=merchant_id,
        merchant_name=merchant_name,
        data={
            'points': points,
            'value': value,
            'balance': balance
        },
        language=language,
        priority=2  # High priority
    )


# ============================================================================
# QUICK TEST
# ============================================================================

if __name__ == "__main__":
    print("\n🚀 LocalKard Notification Queue Demo\n")

    # Mock handler
    def mock_handler(notification: Notification) -> Dict:
        """Mock notification handler"""
        print(f"   📱 Sending {notification.type.value} to {notification.customer_phone}")
        time.sleep(0.5)  # Simulate API call
        return {'success': True, 'message_id': 'MOCK_123'}

    # Create queue
    notif_queue = NotificationQueue(worker_threads=2, persist=False)
    notif_queue.set_handler(mock_handler)

    # Start workers
    notif_queue.start_workers()

    # Add some notifications
    print("📝 Queuing notifications...\n")

    notif_queue.enqueue(create_points_earned_notification(
        customer_phone='9876543210',
        merchant_id='M001',
        merchant_name='Sharma Kirana',
        points=50,
        balance=250,
        tier='silver'
    ))

    notif_queue.enqueue(create_tier_upgrade_notification(
        customer_phone='9876543210',
        merchant_id='M001',
        merchant_name='Sharma Kirana',
        new_tier='gold',
        multiplier=1.5,
        balance=2100
    ))

    notif_queue.enqueue(create_redemption_notification(
        customer_phone='9123456789',
        merchant_id='M001',
        merchant_name='Sharma Kirana',
        points=100,
        value=10,
        balance=150
    ))

    # Wait for processing
    print("\n⏳ Processing queue...\n")
    time.sleep(3)

    # Check stats
    print("\n📊 Queue Statistics:")
    stats = notif_queue.get_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")

    # Stop workers
    notif_queue.stop_workers()

    print("\n✅ Demo complete!")
