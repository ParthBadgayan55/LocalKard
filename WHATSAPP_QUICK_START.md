# WhatsApp Notifications - Quick Start Guide

## 5-Minute Setup (Mock Mode)

The system is **already working** in mock mode! When a customer makes a purchase, you'll see WhatsApp notifications in the console.

### Current Status

✅ **Enabled** - Notifications are active
✅ **Mock Mode** - No API keys needed
✅ **Bilingual** - English & Hindi templates
✅ **Automatic** - Triggers on purchase, redemption, tier upgrade

### Test It Now

```python
python3 test_notifications.py
```

You'll see mock WhatsApp messages printed to console!

## Activate Real WhatsApp (15 Minutes)

### Option 1: Twilio (Easiest)

1. **Sign up**: https://www.twilio.com/try-twilio (Free ₹1,350 credit)

2. **Get credentials**:
   - Account SID (starts with AC...)
   - Auth Token
   - WhatsApp sandbox number

3. **Set environment variables**:
   ```bash
   export TWILIO_ACCOUNT_SID="AC..."
   export TWILIO_AUTH_TOKEN="..."
   export TWILIO_WHATSAPP_NUMBER="whatsapp:+14155238886"
   ```

4. **Activate in LocalKard**:
   ```python
   # config.py
   WHATSAPP_MOCK_MODE = False  # That's it!
   ```

5. **Test**: Send yourself a notification!

### Option 2: WATI.io (For India)

1. **Sign up**: https://www.wati.io (7-day free trial)

2. **Get credentials**:
   - API Key
   - API URL

3. **Set environment variables**:
   ```bash
   export WATI_API_KEY="your_key"
   export WATI_API_URL="https://live-server.wati.io"
   ```

4. **Activate in LocalKard**:
   ```python
   # config.py
   WHATSAPP_PROVIDER = 'wati'
   WHATSAPP_MOCK_MODE = False
   ```

5. **Install dependency**:
   ```bash
   pip install twilio  # or requests for WATI
   ```

## What Happens Automatically

### When Customer Makes Purchase
1. ✅ Points earned notification sent
2. ✅ If tier upgraded, celebration message sent

### When Customer Redeems Points
1. ✅ Redemption confirmation sent

### Example Notification (English)

```
🎉 Sharma Kirana Store

You earned 50 points!
💰 Balance: 250 pts
🏆 Tier: Silver

Reply BALANCE to check anytime
```

### Example Notification (Hindi)

```
🎉 शर्मा किराना स्टोर

आपने 50 अंक कमाए!
💰 शेष: 250 अंक
🏆 श्रेणी: Silver

BALANCE भेजें जानकारी के लिए
```

## Switch to Hindi

```python
# config.py
NOTIFICATION_LANGUAGE = 'hi'  # Default Hindi
```

Or per-transaction:

```python
engine.process_purchase(
    customer_phone='9876543210',
    amount=1000,
    metadata={
        'merchant_name': 'My Store',
        'language': 'hi'  # This purchase gets Hindi notification
    }
)
```

## Customize Messages

Edit templates in `whatsapp_manager.py`:

```python
class MessageTemplates:
    @staticmethod
    def points_earned(...):
        templates = {
            'en': f"Your custom message here",
            'hi': f"आपका संदेश यहां"
        }
        return templates.get(language, templates['en'])
```

## Monitor Performance

```python
from whatsapp_manager import WhatsAppManager

whatsapp = WhatsAppManager(provider='twilio')
stats = whatsapp.get_delivery_stats(days=7)

print(f"Messages sent: {stats['total']}")
print(f"Success rate: {stats['success_rate']:.2f}%")
```

## Disable Notifications

```python
# config.py
FEATURES['whatsapp_notifications'] = False
```

## Troubleshooting

### Messages not sending?

1. Check: `FEATURES['whatsapp_notifications'] = True`
2. Check: `WHATSAPP_MOCK_MODE` setting matches your intent
3. Check: Environment variables are set (if using real API)
4. Run: `python3 test_notifications.py`

### Messages in wrong language?

```python
# config.py
NOTIFICATION_LANGUAGE = 'en'  # or 'hi'
```

## Cost Estimate

### Twilio (Pay as you go)
- ₹0.50 per message
- 100 customers × 2 messages/month = ₹100/month
- Free trial: ₹1,350 credit (~2,700 messages)

### WATI.io (Monthly plan)
- ₹999/month (includes 1,000 messages)
- ₹0.25 per additional message
- Better for >500 messages/month

## Full Documentation

For complete details, see: **WHATSAPP_NOTIFICATIONS.md**

## Support

Run tests anytime:
```bash
python3 test_notifications.py
```

Check logs:
```bash
cat central_data/whatsapp_logs.json
```

---

**You're ready to engage customers via WhatsApp! 🚀**
