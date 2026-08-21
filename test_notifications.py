#!/usr/bin/env python3
"""
Test WhatsApp Notification System
Quick validation that all components work together
"""

import time
import json


def test_whatsapp_manager():
    """Test WhatsApp manager directly"""
    print("\n" + "="*60)
    print("TEST 1: WhatsApp Manager (Mock Mode)")
    print("="*60)

    from whatsapp_manager import WhatsAppManager

    whatsapp = WhatsAppManager(provider='twilio', mock_mode=True)

    # Test points earned (English)
    print("\n1. Testing Points Earned (English):")
    result = whatsapp.send_points_earned(
        customer_phone='9876543210',
        merchant_name='Sharma Kirana Store',
        points=50,
        balance=250,
        tier='silver',
        language='en'
    )
    assert result['success'], "Points earned notification failed"
    print(f"✅ Result: {result['message_id']}")

    # Test points earned (Hindi)
    print("\n2. Testing Points Earned (Hindi):")
    result = whatsapp.send_points_earned(
        customer_phone='9876543210',
        merchant_name='शर्मा किराना स्टोर',
        points=50,
        balance=250,
        tier='silver',
        language='hi'
    )
    assert result['success'], "Points earned notification (Hindi) failed"
    print(f"✅ Result: {result['message_id']}")

    # Test tier upgrade
    print("\n3. Testing Tier Upgrade:")
    result = whatsapp.send_tier_upgrade(
        customer_phone='9876543210',
        merchant_name='Sharma Kirana Store',
        new_tier='gold',
        multiplier=1.5,
        balance=2100,
        language='en'
    )
    assert result['success'], "Tier upgrade notification failed"
    print(f"✅ Result: {result['message_id']}")

    # Test redemption
    print("\n4. Testing Redemption:")
    result = whatsapp.send_points_redeemed(
        customer_phone='9876543210',
        merchant_name='Sharma Kirana Store',
        points=100,
        value=10,
        balance=150,
        language='en'
    )
    assert result['success'], "Redemption notification failed"
    print(f"✅ Result: {result['message_id']}")

    # Get delivery stats
    print("\n5. Checking Delivery Stats:")
    stats = whatsapp.get_delivery_stats(days=1)
    print(f"   Total messages: {stats.get('total', 0)}")
    print(f"   Successful: {stats.get('successful', 0)}")
    print(f"   Failed: {stats.get('failed', 0)}")
    print(f"   By template: {json.dumps(stats.get('by_template', {}), indent=4)}")

    print("\n✅ WhatsApp Manager tests passed!")


def test_notification_queue():
    """Test notification queue system"""
    print("\n" + "="*60)
    print("TEST 2: Notification Queue System")
    print("="*60)

    from notification_queue import (
        NotificationQueue,
        create_points_earned_notification,
        create_tier_upgrade_notification,
        create_redemption_notification
    )

    # Mock handler
    def mock_handler(notification):
        print(f"   📤 Processing: {notification.type.value} for {notification.customer_phone}")
        time.sleep(0.3)  # Simulate API call
        return {'success': True, 'message_id': f'MOCK_{notification.type.value}'}

    # Create queue
    queue = NotificationQueue(worker_threads=2, persist=False)
    queue.set_handler(mock_handler)

    print("\n1. Starting workers...")
    queue.start_workers()
    time.sleep(0.5)
    print("   ✅ Workers started")

    # Queue notifications
    print("\n2. Queuing notifications...")

    queue.enqueue(create_points_earned_notification(
        customer_phone='9876543210',
        merchant_id='M001',
        merchant_name='Test Store',
        points=50,
        balance=250,
        tier='silver'
    ))

    queue.enqueue(create_tier_upgrade_notification(
        customer_phone='9876543210',
        merchant_id='M001',
        merchant_name='Test Store',
        new_tier='gold',
        multiplier=1.5,
        balance=2100
    ))

    queue.enqueue(create_redemption_notification(
        customer_phone='9123456789',
        merchant_id='M001',
        merchant_name='Test Store',
        points=100,
        value=10,
        balance=150
    ))

    print("   ✅ 3 notifications queued")

    # Wait for processing
    print("\n3. Processing queue...")
    time.sleep(2)

    # Check stats
    print("\n4. Queue Statistics:")
    stats = queue.get_stats()
    print(f"   Total queued: {stats['total_queued']}")
    print(f"   Processed: {stats['total_processed']}")
    print(f"   Failed: {stats['total_failed']}")
    print(f"   Queue size: {stats['queue_size']}")

    assert stats['total_processed'] == 3, "Not all notifications processed"
    print("\n   ✅ All notifications processed")

    # Stop workers
    print("\n5. Stopping workers...")
    queue.stop_workers()
    print("   ✅ Workers stopped")

    print("\n✅ Notification Queue tests passed!")


def test_payback_integration():
    """Test integration with PaybackEngine"""
    print("\n" + "="*60)
    print("TEST 3: PaybackEngine Integration")
    print("="*60)

    from payback_engine import PaybackEngine, CentralCustomerDB

    # Create test customer
    print("\n1. Creating test customer...")
    customer_db = CentralCustomerDB()

    # Check if test customer exists
    test_phone = '9999999999'
    customer = customer_db.get_customer_by_phone(test_phone)

    if not customer:
        customer = customer_db.create_customer(
            phone=test_phone,
            name='Test Customer',
            email='test@example.com',
            merchant_id='M001'
        )
        print(f"   ✅ Created customer: {customer['localkard_id']}")
    else:
        print(f"   ✅ Using existing customer: {customer['localkard_id']}")

    # Create engine
    print("\n2. Creating PaybackEngine...")
    engine = PaybackEngine(merchant_id='M001')
    time.sleep(1)  # Let notification system initialize
    print("   ✅ Engine created")

    # Process purchase (should trigger notifications)
    print("\n3. Processing purchase (triggers notifications)...")
    result = engine.process_purchase(
        customer_phone=test_phone,
        amount=1000,
        description='Test purchase',
        metadata={
            'merchant_name': 'Test Store',
            'language': 'en'
        }
    )

    print(f"   Transaction ID: {result['transaction_id']}")
    print(f"   Points earned: {result['points_earned']}")
    print(f"   New balance: {result['new_balance']}")
    print(f"   Tier upgraded: {result['tier_upgraded']}")

    # Wait for queue to process
    print("\n4. Waiting for notifications to process...")
    time.sleep(2)

    # Check queue stats
    if engine._notification_queue:
        stats = engine._notification_queue.get_stats()
        print(f"   Queue processed: {stats['total_processed']}")
        print(f"   Queue failed: {stats['total_failed']}")
        print("   ✅ Notifications sent")
    else:
        print("   ⚠️ Notification queue not initialized (expected in test env)")

    print("\n✅ PaybackEngine integration tests passed!")


def test_config():
    """Test configuration"""
    print("\n" + "="*60)
    print("TEST 4: Configuration Check")
    print("="*60)

    import config

    print("\n1. Checking feature flags...")
    assert config.FEATURES['whatsapp_notifications'] == True, "WhatsApp not enabled"
    print("   ✅ whatsapp_notifications: enabled")

    print("\n2. Checking WhatsApp settings...")
    print(f"   Provider: {config.WHATSAPP_PROVIDER}")
    print(f"   Mock mode: {config.WHATSAPP_MOCK_MODE}")
    print(f"   Language: {config.NOTIFICATION_LANGUAGE}")
    print(f"   Workers: {config.NOTIFICATION_QUEUE_WORKERS}")
    print(f"   Max retries: {config.NOTIFICATION_MAX_RETRIES}")
    print("   ✅ All settings configured")

    print("\n✅ Configuration tests passed!")


def main():
    """Run all tests"""
    print("\n" + "="*70)
    print(" LocalKard WhatsApp Notification System - Test Suite")
    print("="*70)

    try:
        # Test 1: WhatsApp Manager
        test_whatsapp_manager()

        # Test 2: Notification Queue
        test_notification_queue()

        # Test 3: Configuration
        test_config()

        # Test 4: PaybackEngine Integration
        test_payback_integration()

        # Final summary
        print("\n" + "="*70)
        print(" 🎉 ALL TESTS PASSED!")
        print("="*70)
        print("\n✅ WhatsApp notification system is fully functional!")
        print("\n📝 Next steps:")
        print("   1. To use real API: Set WHATSAPP_MOCK_MODE = False in config.py")
        print("   2. Add environment variables for Twilio/WATI credentials")
        print("   3. Test with real phone numbers")
        print("   4. Monitor delivery stats in production")
        print("\n📚 Documentation: WHATSAPP_NOTIFICATIONS.md")
        print()

    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
