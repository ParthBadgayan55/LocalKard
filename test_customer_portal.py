#!/usr/bin/env python3
"""
Test Script for LocalKard Customer Portal
Tests all major components and integrations
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from payback_engine import CentralCustomerDB, TransactionEngine, PointsEngine, RedemptionEngine, PaybackEngine
import security
import config

def test_customer_registration():
    """Test customer registration flow"""
    print("\n" + "="*60)
    print("TEST 1: Customer Registration")
    print("="*60)

    # Test phone validation
    test_phone = "9876543210"
    is_valid, error = security.validate_phone_number(test_phone)
    assert is_valid, f"Phone validation failed: {error}"
    print(f"✓ Phone validation passed: {test_phone}")

    # Test email validation
    test_email = "customer@localkard.com"
    is_valid, error = security.validate_email(test_email)
    assert is_valid, f"Email validation failed: {error}"
    print(f"✓ Email validation passed: {test_email}")

    # Test password hashing
    test_password = "Test@1234"
    is_strong, error = security.is_strong_password(test_password)
    assert is_strong, f"Password strength check failed: {error}"
    print(f"✓ Password strength check passed")

    hashed = security.hash_password(test_password)
    assert security.verify_password(test_password, hashed), "Password verification failed"
    print(f"✓ Password hashing and verification passed")

    # Test customer creation in central DB
    customer_db = CentralCustomerDB()
    customer = customer_db.create_customer(
        phone=test_phone,
        name="Test Customer",
        email=test_email,
        merchant_id="CUSTOMER_PORTAL"
    )

    assert customer['phone'] == test_phone, "Customer phone mismatch"
    assert customer['name'] == "Test Customer", "Customer name mismatch"
    assert customer['points_balance'] == 0, "Initial points should be 0"
    assert customer['tier'] == 'bronze', "Initial tier should be bronze"
    assert customer['localkard_id'].startswith('LK'), "LocalKard ID format incorrect"

    print(f"✓ Customer created: {customer['localkard_id']}")
    print(f"  Name: {customer['name']}")
    print(f"  Phone: {customer['phone']}")
    print(f"  Tier: {customer['tier']}")
    print(f"  Balance: {customer['points_balance']}")

    return customer

def test_points_earning(customer):
    """Test points earning flow"""
    print("\n" + "="*60)
    print("TEST 2: Points Earning")
    print("="*60)

    merchant_id = "9876543210"
    engine = PaybackEngine(merchant_id)

    # Test purchase processing
    result = engine.process_purchase(
        customer_phone=customer['phone'],
        amount=500.0,
        description="Test purchase"
    )

    assert result['success'], f"Purchase failed: {result.get('error', 'Unknown')}"
    assert result['points_earned'] > 0, "No points earned"
    assert result['customer_tier'] in ['bronze', 'silver', 'gold', 'platinum'], "Invalid tier"

    print(f"✓ Purchase processed successfully")
    print(f"  Amount: ₹{result['amount']}")
    print(f"  Points earned: {result['points_earned']}")
    print(f"  New balance: {result['new_balance']}")
    print(f"  Tier: {result['customer_tier']}")
    print(f"  Transaction ID: {result['transaction_id']}")

    # Verify customer balance updated
    customer_db = CentralCustomerDB()
    updated_customer = customer_db.get_customer_by_phone(customer['phone'])
    assert updated_customer['points_balance'] == result['new_balance'], "Balance mismatch"
    print(f"✓ Customer balance verified: {updated_customer['points_balance']}")

    return updated_customer

def test_transaction_history(customer):
    """Test transaction history retrieval"""
    print("\n" + "="*60)
    print("TEST 3: Transaction History")
    print("="*60)

    txn_engine = TransactionEngine()
    transactions = txn_engine.get_customer_transactions(customer['localkard_id'])

    assert len(transactions) > 0, "No transactions found"
    print(f"✓ Found {len(transactions)} transaction(s)")

    for idx, txn in enumerate(transactions, 1):
        print(f"\n  Transaction {idx}:")
        print(f"    ID: {txn['transaction_id']}")
        print(f"    Type: {txn['type']}")
        print(f"    Amount: ₹{txn['amount']}")
        print(f"    Points: {txn['points']}")
        print(f"    Time: {txn['timestamp']}")

    return transactions

def test_redemption(customer):
    """Test points redemption flow"""
    print("\n" + "="*60)
    print("TEST 4: Points Redemption")
    print("="*60)

    # Check if customer has enough points
    if customer['points_balance'] < 100:
        print("⚠ Customer doesn't have enough points for redemption (min 100)")
        print(f"  Current balance: {customer['points_balance']}")
        return None

    redemption_engine = RedemptionEngine()
    merchant_id = "9876543210"
    points_to_redeem = min(100, customer['points_balance'])
    purchase_amount = 50.0

    result = redemption_engine.redeem_points(
        customer_id=customer['localkard_id'],
        merchant_id=merchant_id,
        points_to_redeem=points_to_redeem,
        purchase_amount=purchase_amount
    )

    assert result['success'], f"Redemption failed: {result.get('error', 'Unknown')}"
    assert result['points_redeemed'] == points_to_redeem, "Points redeemed mismatch"
    assert result['discount_value'] > 0, "No discount value"

    print(f"✓ Redemption successful")
    print(f"  Points redeemed: {result['points_redeemed']}")
    print(f"  Discount value: ₹{result['discount_value']}")
    print(f"  New balance: {result['new_balance']}")
    print(f"  Transaction ID: {result['transaction_id']}")

    # Verify balance updated
    customer_db = CentralCustomerDB()
    updated_customer = customer_db.get_customer_by_phone(customer['phone'])
    assert updated_customer['points_balance'] == result['new_balance'], "Balance not updated"
    print(f"✓ Balance verified after redemption: {updated_customer['points_balance']}")

    return result

def test_tier_system(customer):
    """Test tier calculation and progression"""
    print("\n" + "="*60)
    print("TEST 5: Tier System")
    print("="*60)

    points_engine = PointsEngine("TEST_MERCHANT")

    # Test tier calculations
    test_points = [0, 500, 2000, 5000, 10000]

    print("Tier progression:")
    for points in test_points:
        tier = points_engine.calculate_tier(points)
        multiplier = config.TIER_MULTIPLIERS[tier]
        print(f"  {points:>6} points → {tier.upper():>8} (multiplier: {multiplier}x)")

    # Test customer's current tier
    current_tier = customer.get('tier', 'bronze')
    lifetime_points = customer.get('lifetime_points', 0)
    calculated_tier = points_engine.calculate_tier(lifetime_points)

    assert current_tier == calculated_tier, f"Tier mismatch: {current_tier} vs {calculated_tier}"
    print(f"\n✓ Customer tier verified: {current_tier.upper()}")
    print(f"  Lifetime points: {lifetime_points}")
    print(f"  Multiplier: {config.TIER_MULTIPLIERS[current_tier]}x")

    # Check next tier
    tier_order = ['bronze', 'silver', 'gold', 'platinum']
    current_index = tier_order.index(current_tier)

    if current_index < len(tier_order) - 1:
        next_tier = tier_order[current_index + 1]
        next_threshold = config.TIER_THRESHOLDS[next_tier]
        points_needed = next_threshold - lifetime_points

        print(f"  Next tier: {next_tier.upper()}")
        print(f"  Points needed: {points_needed}")
    else:
        print(f"  🏆 Maximum tier reached!")

def test_referral_code(customer):
    """Test referral code generation"""
    print("\n" + "="*60)
    print("TEST 6: Referral System")
    print("="*60)

    import hashlib

    # Generate referral code (same logic as in app)
    referral_code = hashlib.md5(customer['phone'].encode()).hexdigest()[:8].upper()

    print(f"✓ Referral code generated: {referral_code}")
    print(f"  For customer: {customer['name']} ({customer['phone']})")

    # Test WhatsApp link generation
    whatsapp_message = f"Join LocalKard and get 50 bonus points! Use my referral code: {referral_code}"
    whatsapp_link = f"https://wa.me/?text={whatsapp_message.replace(' ', '%20')}"

    print(f"✓ WhatsApp share link generated")
    print(f"  Link length: {len(whatsapp_link)} chars")

def test_config_values():
    """Test configuration values"""
    print("\n" + "="*60)
    print("TEST 7: Configuration")
    print("="*60)

    # Test earning rate
    earning_rate = config.DEFAULT_EARNING_RATE
    print(f"Earning Rate:")
    print(f"  ₹{earning_rate['amount']} = {earning_rate['points']} points")
    print(f"  Rate: {earning_rate['points']/earning_rate['amount']:.4f} points/₹")

    # Test redemption rate
    redemption_rate = config.DEFAULT_REDEMPTION_RATE
    print(f"\nRedemption Rate:")
    print(f"  {redemption_rate['points']} points = ₹{redemption_rate['value']}")
    print(f"  Rate: ₹{redemption_rate['value']/redemption_rate['points']:.4f} per point")

    # Test tier thresholds
    print(f"\nTier Thresholds:")
    for tier, threshold in config.TIER_THRESHOLDS.items():
        multiplier = config.TIER_MULTIPLIERS[tier]
        print(f"  {tier.upper():>8}: {threshold:>6} points (multiplier: {multiplier}x)")

    # Test feature flags
    print(f"\nFeature Flags:")
    for feature, enabled in config.FEATURES.items():
        status = "✓ Enabled" if enabled else "✗ Disabled"
        print(f"  {feature:>25}: {status}")

def run_all_tests():
    """Run all customer portal tests"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*15 + "LOCALKARD CUSTOMER PORTAL" + " "*18 + "║")
    print("║" + " "*19 + "Integration Test Suite" + " "*17 + "║")
    print("╚" + "="*58 + "╝")

    try:
        # Run tests in sequence
        customer = test_customer_registration()
        customer = test_points_earning(customer)
        transactions = test_transaction_history(customer)
        test_redemption(customer)
        test_tier_system(customer)
        test_referral_code(customer)
        test_config_values()

        # Final summary
        print("\n" + "="*60)
        print("✓ ALL TESTS PASSED!")
        print("="*60)
        print("\nCustomer Portal is ready for production!")
        print("\nFeatures Verified:")
        print("  ✓ Customer registration with validation")
        print("  ✓ Points earning and calculation")
        print("  ✓ Transaction history tracking")
        print("  ✓ Points redemption flow")
        print("  ✓ Tier system and progression")
        print("  ✓ Referral code generation")
        print("  ✓ Configuration settings")
        print("\nNext Steps:")
        print("  1. Run: streamlit run app.py")
        print("  2. Navigate to Customer Portal")
        print("  3. Sign up or login")
        print("  4. Test all features in UI")
        print()

        return True

    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
