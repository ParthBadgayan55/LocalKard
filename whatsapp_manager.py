"""
LocalKard WhatsApp Notification Manager
Sends customer notifications via WhatsApp using multiple provider options
"""

import os
from datetime import datetime
from typing import Dict, Optional, List
from abc import ABC, abstractmethod
import json
from pathlib import Path

# ============================================================================
# ABSTRACT BASE - Provider Interface
# ============================================================================

class WhatsAppProvider(ABC):
    """Abstract base for WhatsApp providers"""

    @abstractmethod
    def send_message(self, to_phone: str, message: str, template_name: str = None) -> Dict:
        """Send WhatsApp message"""
        pass

    @abstractmethod
    def get_status(self, message_id: str) -> Dict:
        """Check message delivery status"""
        pass


# ============================================================================
# TWILIO PROVIDER (Recommended for India)
# ============================================================================

class TwilioWhatsAppProvider(WhatsAppProvider):
    """Twilio WhatsApp Business API Integration"""

    def __init__(self, account_sid: str = None, auth_token: str = None,
                 from_number: str = None, mock_mode: bool = True):
        self.account_sid = account_sid or os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = auth_token or os.getenv('TWILIO_AUTH_TOKEN')
        self.from_number = from_number or os.getenv('TWILIO_WHATSAPP_NUMBER', 'whatsapp:+14155238886')
        self.mock_mode = mock_mode

        if not mock_mode:
            try:
                from twilio.rest import Client
                self.client = Client(self.account_sid, self.auth_token)
            except ImportError:
                print("⚠️ Twilio library not installed. Run: pip install twilio")
                self.mock_mode = True
                self.client = None
        else:
            self.client = None

    def send_message(self, to_phone: str, message: str, template_name: str = None) -> Dict:
        """Send WhatsApp message via Twilio"""

        # Format phone number for WhatsApp
        if not to_phone.startswith('whatsapp:'):
            # Add India country code if not present
            if not to_phone.startswith('+'):
                to_phone = f'+91{to_phone}'
            to_phone = f'whatsapp:{to_phone}'

        if self.mock_mode:
            # Mock implementation for testing
            return self._mock_send(to_phone, message, template_name)

        try:
            message_obj = self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=to_phone
            )

            return {
                'success': True,
                'message_id': message_obj.sid,
                'status': message_obj.status,
                'to': to_phone,
                'provider': 'twilio',
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'to': to_phone,
                'provider': 'twilio',
                'timestamp': datetime.now().isoformat()
            }

    def get_status(self, message_id: str) -> Dict:
        """Check message delivery status"""
        if self.mock_mode:
            return {'status': 'delivered', 'message_id': message_id}

        try:
            message = self.client.messages(message_id).fetch()
            return {
                'status': message.status,
                'message_id': message_id,
                'error_code': message.error_code,
                'error_message': message.error_message
            }
        except Exception as e:
            return {'error': str(e), 'message_id': message_id}

    def _mock_send(self, to_phone: str, message: str, template_name: str) -> Dict:
        """Mock send for testing without API keys"""
        mock_id = f"MOCK_{datetime.now().strftime('%Y%m%d%H%M%S')}"

        print(f"\n{'='*60}")
        print("📱 MOCK WhatsApp Message (Twilio)")
        print(f"{'='*60}")
        print(f"To: {to_phone}")
        print(f"Template: {template_name or 'custom'}")
        print(f"Message ID: {mock_id}")
        print(f"\n{message}\n")
        print(f"{'='*60}\n")

        return {
            'success': True,
            'message_id': mock_id,
            'status': 'queued',
            'to': to_phone,
            'provider': 'twilio_mock',
            'timestamp': datetime.now().isoformat()
        }


# ============================================================================
# WATI.IO PROVIDER (Indian service, popular for small businesses)
# ============================================================================

class WatiWhatsAppProvider(WhatsAppProvider):
    """WATI.io WhatsApp Integration (Popular in India)"""

    def __init__(self, api_key: str = None, api_url: str = None, mock_mode: bool = True):
        self.api_key = api_key or os.getenv('WATI_API_KEY')
        self.api_url = api_url or os.getenv('WATI_API_URL', 'https://live-server.wati.io')
        self.mock_mode = mock_mode

    def send_message(self, to_phone: str, message: str, template_name: str = None) -> Dict:
        """Send WhatsApp message via WATI"""

        # Clean phone number (WATI uses plain numbers)
        clean_phone = to_phone.replace('whatsapp:', '').replace('+', '').replace('-', '')

        if self.mock_mode:
            return self._mock_send(clean_phone, message, template_name)

        try:
            import requests

            endpoint = f"{self.api_url}/api/v1/sendSessionMessage/{clean_phone}"
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            payload = {'messageText': message}

            response = requests.post(endpoint, json=payload, headers=headers)

            if response.status_code == 200:
                return {
                    'success': True,
                    'message_id': response.json().get('messageId'),
                    'status': 'sent',
                    'to': clean_phone,
                    'provider': 'wati',
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return {
                    'success': False,
                    'error': response.text,
                    'to': clean_phone,
                    'provider': 'wati',
                    'timestamp': datetime.now().isoformat()
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'to': clean_phone,
                'provider': 'wati',
                'timestamp': datetime.now().isoformat()
            }

    def get_status(self, message_id: str) -> Dict:
        """Check message status (WATI specific implementation)"""
        if self.mock_mode:
            return {'status': 'delivered', 'message_id': message_id}

        # WATI status check implementation
        return {'status': 'unknown', 'message_id': message_id}

    def _mock_send(self, to_phone: str, message: str, template_name: str) -> Dict:
        """Mock send for testing"""
        mock_id = f"WATI_{datetime.now().strftime('%Y%m%d%H%M%S')}"

        print(f"\n{'='*60}")
        print("📱 MOCK WhatsApp Message (WATI.io)")
        print(f"{'='*60}")
        print(f"To: +91{to_phone}")
        print(f"Template: {template_name or 'custom'}")
        print(f"Message ID: {mock_id}")
        print(f"\n{message}\n")
        print(f"{'='*60}\n")

        return {
            'success': True,
            'message_id': mock_id,
            'status': 'sent',
            'to': to_phone,
            'provider': 'wati_mock',
            'timestamp': datetime.now().isoformat()
        }


# ============================================================================
# MESSAGE TEMPLATES
# ============================================================================

class MessageTemplates:
    """Pre-built message templates for different events"""

    # Supported languages
    LANGUAGES = ['en', 'hi']  # English, Hindi

    @staticmethod
    def points_earned(merchant_name: str, points: float, balance: float,
                     tier: str, language: str = 'en') -> str:
        """Points earned notification"""
        templates = {
            'en': f"🎉 *{merchant_name}*\n\nYou earned *{points:.0f} points*!\n💰 Balance: {balance:.0f} pts\n🏆 Tier: {tier.title()}\n\n_Reply BALANCE to check anytime_",
            'hi': f"🎉 *{merchant_name}*\n\nआपने *{points:.0f} अंक* कमाए!\n💰 शेष: {balance:.0f} अंक\n🏆 श्रेणी: {tier.title()}\n\n_BALANCE भेजें जानकारी के लिए_"
        }
        return templates.get(language, templates['en'])

    @staticmethod
    def points_redeemed(merchant_name: str, points: float, value: float,
                       balance: float, language: str = 'en') -> str:
        """Points redemption notification"""
        templates = {
            'en': f"💎 *{merchant_name}*\n\nRedeemed: {points:.0f} points\n💰 Discount: ₹{value:.2f}\n🎁 New Balance: {balance:.0f} pts\n\nThank you! 🙏",
            'hi': f"💎 *{merchant_name}*\n\nभुनाया: {points:.0f} अंक\n💰 छूट: ₹{value:.2f}\n🎁 नया शेष: {balance:.0f} अंक\n\nधन्यवाद! 🙏"
        }
        return templates.get(language, templates['en'])

    @staticmethod
    def tier_upgrade(merchant_name: str, new_tier: str, multiplier: float,
                    balance: float, language: str = 'en') -> str:
        """Tier upgrade celebration"""
        tier_emojis = {
            'bronze': '🥉',
            'silver': '🥈',
            'gold': '🥇',
            'platinum': '💎'
        }
        emoji = tier_emojis.get(new_tier.lower(), '🏆')

        templates = {
            'en': f"🎊 *CONGRATULATIONS!* 🎊\n\n{emoji} You're now *{new_tier.upper()}* tier!\n\n✨ Enjoy {multiplier}x points on all purchases\n💰 Current Balance: {balance:.0f} pts\n\nKeep shopping at *{merchant_name}*! 🛍️",
            'hi': f"🎊 *बधाई हो!* 🎊\n\n{emoji} अब आप *{new_tier.upper()}* श्रेणी में हैं!\n\n✨ हर खरीद पर {multiplier}x अंक पाएं\n💰 वर्तमान शेष: {balance:.0f} अंक\n\n*{merchant_name}* पर खरीदारी जारी रखें! 🛍️"
        }
        return templates.get(language, templates['en'])

    @staticmethod
    def balance_inquiry(merchant_name: str, points: float, value: float,
                       tier: str, language: str = 'en') -> str:
        """Balance check response"""
        templates = {
            'en': f"💰 *{merchant_name} - Your Balance*\n\n🎁 Points: {points:.0f}\n💵 Worth: ₹{value:.2f}\n🏆 Tier: {tier.title()}\n\n_Use at your next purchase!_",
            'hi': f"💰 *{merchant_name} - आपका शेष*\n\n🎁 अंक: {points:.0f}\n💵 मूल्य: ₹{value:.2f}\n🏆 श्रेणी: {tier.title()}\n\n_अगली खरीद पर उपयोग करें!_"
        }
        return templates.get(language, templates['en'])

    @staticmethod
    def referral_reward(merchant_name: str, referrer_name: str, bonus: float,
                       balance: float, language: str = 'en') -> str:
        """Referral bonus notification"""
        templates = {
            'en': f"🎁 *Referral Bonus!*\n\n{referrer_name} joined *{merchant_name}* through your referral!\n\n✨ Bonus: {bonus:.0f} points\n💰 New Balance: {balance:.0f} pts\n\nShare & Earn more! 🚀",
            'hi': f"🎁 *रेफरल बोनस!*\n\n{referrer_name} ने आपके रेफरल से *{merchant_name}* में शामिल हुए!\n\n✨ बोनस: {bonus:.0f} अंक\n💰 नया शेष: {balance:.0f} अंक\n\nसाझा करें और अधिक कमाएं! 🚀"
        }
        return templates.get(language, templates['en'])

    @staticmethod
    def welcome_message(merchant_name: str, customer_name: str,
                       language: str = 'en') -> str:
        """Welcome new customer"""
        templates = {
            'en': f"🎉 Welcome to *{merchant_name}*!\n\nHi {customer_name}! 👋\n\nYou're now part of our loyalty program. Earn points on every purchase and enjoy exclusive rewards!\n\n💡 Reply BALANCE anytime to check your points.",
            'hi': f"🎉 *{merchant_name}* में आपका स्वागत है!\n\nनमस्ते {customer_name}! 👋\n\nअब आप हमारे लॉयल्टी प्रोग्राम का हिस्सा हैं। हर खरीद पर अंक कमाएं और विशेष पुरस्कार पाएं!\n\n💡 BALANCE भेजकर अपने अंक जांचें।"
        }
        return templates.get(language, templates['en'])

    @staticmethod
    def opt_out_info(merchant_name: str, language: str = 'en') -> str:
        """Opt-out information"""
        templates = {
            'en': f"To stop receiving messages from *{merchant_name}*, reply STOP\n\n_You can opt-in anytime by visiting the store_",
            'hi': f"*{merchant_name}* से संदेश बंद करने के लिए STOP भेजें\n\n_आप कभी भी स्टोर पर जाकर फिर से शुरू कर सकते हैं_"
        }
        return templates.get(language, templates['en'])


# ============================================================================
# MAIN WHATSAPP MANAGER
# ============================================================================

class WhatsAppManager:
    """Main WhatsApp notification manager with queue support"""

    def __init__(self, provider: str = 'twilio', mock_mode: bool = True,
                 log_dir: str = 'central_data'):
        """
        Initialize WhatsApp Manager

        Args:
            provider: 'twilio' or 'wati'
            mock_mode: If True, uses mock implementation (no API calls)
            log_dir: Directory to store delivery logs
        """
        self.provider_name = provider
        self.mock_mode = mock_mode
        self.log_dir = Path(log_dir)
        self.log_file = self.log_dir / 'whatsapp_logs.json'

        # Initialize provider
        if provider == 'twilio':
            self.provider = TwilioWhatsAppProvider(mock_mode=mock_mode)
        elif provider == 'wati':
            self.provider = WatiWhatsAppProvider(mock_mode=mock_mode)
        else:
            raise ValueError(f"Unknown provider: {provider}. Use 'twilio' or 'wati'")

        # Ensure log directory exists
        self.log_dir.mkdir(exist_ok=True)

    def send_notification(self, to_phone: str, message: str,
                         template_name: str = None, metadata: Dict = None) -> Dict:
        """Send WhatsApp notification"""

        # Send message
        result = self.provider.send_message(to_phone, message, template_name)

        # Log delivery attempt
        self._log_delivery(to_phone, message, template_name, result, metadata)

        return result

    def send_points_earned(self, customer_phone: str, merchant_name: str,
                          points: float, balance: float, tier: str,
                          language: str = 'en') -> Dict:
        """Send points earned notification"""
        message = MessageTemplates.points_earned(
            merchant_name, points, balance, tier, language
        )
        return self.send_notification(
            customer_phone, message,
            template_name='points_earned',
            metadata={'points': points, 'balance': balance, 'tier': tier}
        )

    def send_points_redeemed(self, customer_phone: str, merchant_name: str,
                            points: float, value: float, balance: float,
                            language: str = 'en') -> Dict:
        """Send redemption confirmation"""
        message = MessageTemplates.points_redeemed(
            merchant_name, points, value, balance, language
        )
        return self.send_notification(
            customer_phone, message,
            template_name='points_redeemed',
            metadata={'points': points, 'value': value, 'balance': balance}
        )

    def send_tier_upgrade(self, customer_phone: str, merchant_name: str,
                         new_tier: str, multiplier: float, balance: float,
                         language: str = 'en') -> Dict:
        """Send tier upgrade celebration"""
        message = MessageTemplates.tier_upgrade(
            merchant_name, new_tier, multiplier, balance, language
        )
        return self.send_notification(
            customer_phone, message,
            template_name='tier_upgrade',
            metadata={'tier': new_tier, 'multiplier': multiplier}
        )

    def send_balance_inquiry(self, customer_phone: str, merchant_name: str,
                            points: float, value: float, tier: str,
                            language: str = 'en') -> Dict:
        """Send balance information"""
        message = MessageTemplates.balance_inquiry(
            merchant_name, points, value, tier, language
        )
        return self.send_notification(
            customer_phone, message,
            template_name='balance_inquiry',
            metadata={'points': points, 'value': value}
        )

    def send_referral_reward(self, customer_phone: str, merchant_name: str,
                            referrer_name: str, bonus: float, balance: float,
                            language: str = 'en') -> Dict:
        """Send referral bonus notification"""
        message = MessageTemplates.referral_reward(
            merchant_name, referrer_name, bonus, balance, language
        )
        return self.send_notification(
            customer_phone, message,
            template_name='referral_reward',
            metadata={'bonus': bonus, 'referrer': referrer_name}
        )

    def send_welcome(self, customer_phone: str, merchant_name: str,
                    customer_name: str, language: str = 'en') -> Dict:
        """Send welcome message to new customer"""
        message = MessageTemplates.welcome_message(
            merchant_name, customer_name, language
        )
        return self.send_notification(
            customer_phone, message,
            template_name='welcome',
            metadata={'customer_name': customer_name}
        )

    def _log_delivery(self, to_phone: str, message: str, template_name: str,
                     result: Dict, metadata: Dict = None):
        """Log message delivery attempt"""
        try:
            # Load existing logs
            logs = []
            if self.log_file.exists():
                with open(self.log_file, 'r') as f:
                    logs = json.load(f)

            # Add new log entry
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'to_phone': to_phone,
                'template_name': template_name,
                'message_length': len(message),
                'result': result,
                'metadata': metadata or {}
            }
            logs.append(log_entry)

            # Keep only last 1000 logs
            if len(logs) > 1000:
                logs = logs[-1000:]

            # Save logs
            with open(self.log_file, 'w') as f:
                json.dump(logs, f, indent=2)
        except Exception as e:
            print(f"Warning: Failed to log WhatsApp delivery: {e}")

    def get_delivery_stats(self, days: int = 7) -> Dict:
        """Get delivery statistics for last N days"""
        try:
            if not self.log_file.exists():
                return {'total': 0, 'successful': 0, 'failed': 0}

            with open(self.log_file, 'r') as f:
                logs = json.load(f)

            # Filter by date
            cutoff = datetime.now() - timedelta(days=days)
            recent_logs = [
                log for log in logs
                if datetime.fromisoformat(log['timestamp']) > cutoff
            ]

            total = len(recent_logs)
            successful = sum(1 for log in recent_logs if log['result'].get('success'))
            failed = total - successful

            # Template breakdown
            templates = {}
            for log in recent_logs:
                template = log.get('template_name', 'unknown')
                templates[template] = templates.get(template, 0) + 1

            return {
                'total': total,
                'successful': successful,
                'failed': failed,
                'success_rate': (successful / total * 100) if total > 0 else 0,
                'by_template': templates,
                'period_days': days
            }
        except Exception as e:
            return {'error': str(e)}


# ============================================================================
# QUICK TEST
# ============================================================================

if __name__ == "__main__":
    # Demo usage
    print("\n🚀 LocalKard WhatsApp Manager Demo\n")

    # Initialize in mock mode
    whatsapp = WhatsAppManager(provider='twilio', mock_mode=True)

    # Test various notifications
    print("1. Points Earned (English)")
    whatsapp.send_points_earned(
        customer_phone='9876543210',
        merchant_name='Sharma Kirana Store',
        points=50,
        balance=250,
        tier='silver',
        language='en'
    )

    print("\n2. Points Earned (Hindi)")
    whatsapp.send_points_earned(
        customer_phone='9876543210',
        merchant_name='शर्मा किराना स्टोर',
        points=50,
        balance=250,
        tier='silver',
        language='hi'
    )

    print("\n3. Tier Upgrade")
    whatsapp.send_tier_upgrade(
        customer_phone='9876543210',
        merchant_name='Sharma Kirana Store',
        new_tier='gold',
        multiplier=1.5,
        balance=2100,
        language='en'
    )

    print("\n4. Balance Inquiry")
    whatsapp.send_balance_inquiry(
        customer_phone='9876543210',
        merchant_name='Sharma Kirana Store',
        points=2100,
        value=210,
        tier='gold',
        language='en'
    )

    print("\n✅ Demo complete!")
    print("\n📊 Delivery Stats:")
    stats = whatsapp.get_delivery_stats()
    print(json.dumps(stats, indent=2))
