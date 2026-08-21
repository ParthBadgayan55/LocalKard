"""
LocalKard Payback-Style Backend Engine
Complete coalition loyalty system (Network features disabled, ready to enable)
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import hashlib

# ============================================================================
# 1. CENTRAL CUSTOMER DATABASE
# ============================================================================

class CentralCustomerDB:
    """Unified customer database across all merchants"""

    def __init__(self, data_dir='central_data'):
        self.data_dir = data_dir
        self.customers_file = os.path.join(data_dir, 'central_customers.json')
        self.ensure_data_dir()

    def ensure_data_dir(self):
        os.makedirs(self.data_dir, exist_ok=True)

    def load_customers(self) -> List[Dict]:
        """Load all customers from central database"""
        if os.path.exists(self.customers_file):
            try:
                with open(self.customers_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return []

    def save_customers(self, customers: List[Dict]) -> bool:
        """Save customers to central database"""
        try:
            with open(self.customers_file, 'w') as f:
                json.dump(customers, f, indent=2)
            return True
        except:
            return False

    def get_customer_by_phone(self, phone: str) -> Optional[Dict]:
        """Get customer by phone (unique identifier)"""
        customers = self.load_customers()
        for customer in customers:
            if customer.get('phone') == phone:
                return customer
        return None

    def get_customer_by_id(self, customer_id: str) -> Optional[Dict]:
        """Get customer by LocalKard ID"""
        customers = self.load_customers()
        for customer in customers:
            if customer.get('localkard_id') == customer_id:
                return customer
        return None

    def create_customer(self, phone: str, name: str, email: str = '',
                       merchant_id: str = None) -> Dict:
        """Create new customer in central database"""
        customers = self.load_customers()

        # Generate unique LocalKard ID
        localkard_id = f"LK{len(customers)+1:08d}"

        customer = {
            'localkard_id': localkard_id,
            'phone': phone,
            'name': name,
            'email': email,
            'points_balance': 0,
            'lifetime_points': 0,
            'tier': 'bronze',
            'tier_progress': 0,
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'created_by_merchant': merchant_id,
            'linked_merchants': [merchant_id] if merchant_id else [],
            'preferences': {},
            'tags': [],
            'last_transaction': None,
            'transaction_count': 0,
            'metadata': {}
        }

        customers.append(customer)
        self.save_customers(customers)
        return customer

    def update_customer(self, localkard_id: str, updates: Dict) -> bool:
        """Update customer data"""
        customers = self.load_customers()
        for i, customer in enumerate(customers):
            if customer.get('localkard_id') == localkard_id:
                customers[i].update(updates)
                return self.save_customers(customers)
        return False

    def link_merchant(self, localkard_id: str, merchant_id: str) -> bool:
        """Link customer to a merchant"""
        customer = self.get_customer_by_id(localkard_id)
        if customer:
            linked = customer.get('linked_merchants', [])
            if merchant_id not in linked:
                linked.append(merchant_id)
                return self.update_customer(localkard_id, {'linked_merchants': linked})
        return False


# ============================================================================
# 2. TRANSACTION ENGINE
# ============================================================================

class TransactionEngine:
    """Record and process all transactions"""

    def __init__(self, data_dir='central_data'):
        self.data_dir = data_dir
        self.transactions_file = os.path.join(data_dir, 'transactions.json')
        self.ensure_data_dir()

    def ensure_data_dir(self):
        os.makedirs(self.data_dir, exist_ok=True)

    def load_transactions(self) -> List[Dict]:
        """Load all transactions"""
        if os.path.exists(self.transactions_file):
            try:
                with open(self.transactions_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return []

    def save_transactions(self, transactions: List[Dict]) -> bool:
        """Save transactions"""
        try:
            with open(self.transactions_file, 'w') as f:
                json.dump(transactions, f, indent=2)
            return True
        except:
            return False

    def create_transaction(self, transaction_type: str, customer_id: str,
                          merchant_id: str, amount: float = 0,
                          points: float = 0, description: str = '',
                          metadata: Dict = None) -> Dict:
        """Create a new transaction"""
        transactions = self.load_transactions()

        transaction = {
            'transaction_id': f"TXN{len(transactions)+1:010d}",
            'type': transaction_type,  # 'earn', 'redeem', 'bonus', 'adjustment'
            'customer_id': customer_id,
            'merchant_id': merchant_id,
            'amount': amount,
            'points': points,
            'description': description,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'status': 'completed',
            'metadata': metadata or {}
        }

        transactions.append(transaction)
        self.save_transactions(transactions)
        return transaction

    def get_customer_transactions(self, customer_id: str,
                                  limit: int = None) -> List[Dict]:
        """Get all transactions for a customer"""
        transactions = self.load_transactions()
        customer_txns = [t for t in transactions if t.get('customer_id') == customer_id]
        customer_txns.sort(key=lambda x: x.get('timestamp', ''), reverse=True)

        if limit:
            return customer_txns[:limit]
        return customer_txns

    def get_merchant_transactions(self, merchant_id: str,
                                  limit: int = None) -> List[Dict]:
        """Get all transactions for a merchant"""
        transactions = self.load_transactions()
        merchant_txns = [t for t in transactions if t.get('merchant_id') == merchant_id]
        merchant_txns.sort(key=lambda x: x.get('timestamp', ''), reverse=True)

        if limit:
            return merchant_txns[:limit]
        return merchant_txns


# ============================================================================
# 3. POINTS CALCULATION ENGINE
# ============================================================================

class PointsEngine:
    """Calculate points based on complex rules"""

    TIER_MULTIPLIERS = {
        'bronze': 1.0,
        'silver': 1.25,
        'gold': 1.5,
        'platinum': 2.0
    }

    TIER_THRESHOLDS = {
        'bronze': 0,
        'silver': 500,
        'gold': 2000,
        'platinum': 5000
    }

    def __init__(self, merchant_id: str, data_dir='merchant_data'):
        self.merchant_id = merchant_id
        self.data_dir = data_dir

    def load_merchant_config(self) -> Dict:
        """Load merchant's points configuration"""
        config_file = os.path.join(self.data_dir, self.merchant_id, 'loyalty_config.json')
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    return json.load(f)
            except:
                pass

        # Default configuration
        return {
            'earning_rate': {'amount': 100, 'points': 5},
            'redemption_rate': {'points': 100, 'value': 10},
            'tier_multiplier_enabled': True,
            'bonus_campaigns': []
        }

    def calculate_base_points(self, amount: float) -> float:
        """Calculate base points from purchase amount"""
        config = self.load_merchant_config()
        rate = config['earning_rate']

        base_rate = rate['points'] / rate['amount']
        return amount * base_rate

    def apply_tier_multiplier(self, base_points: float, tier: str) -> float:
        """Apply tier-based multiplier"""
        config = self.load_merchant_config()
        if not config.get('tier_multiplier_enabled', True):
            return base_points

        multiplier = self.TIER_MULTIPLIERS.get(tier, 1.0)
        return base_points * multiplier

    def apply_bonus_campaigns(self, base_points: float, metadata: Dict = None) -> Tuple[float, str]:
        """Apply active bonus campaigns"""
        config = self.load_merchant_config()
        campaigns = config.get('bonus_campaigns', [])

        bonus = 0
        campaign_applied = ''

        for campaign in campaigns:
            if self._is_campaign_active(campaign):
                campaign_bonus = base_points * campaign.get('multiplier', 0)
                if campaign_bonus > bonus:
                    bonus = campaign_bonus
                    campaign_applied = campaign.get('name', '')

        return base_points + bonus, campaign_applied

    def _is_campaign_active(self, campaign: Dict) -> bool:
        """Check if campaign is currently active"""
        now = datetime.now()
        start = datetime.fromisoformat(campaign.get('start_date', now.isoformat()))
        end = datetime.fromisoformat(campaign.get('end_date', now.isoformat()))
        return start <= now <= end

    def calculate_total_points(self, amount: float, tier: str,
                              metadata: Dict = None) -> Dict:
        """Calculate total points with all modifiers"""
        base_points = self.calculate_base_points(amount)
        tier_points = self.apply_tier_multiplier(base_points, tier)
        final_points, campaign = self.apply_bonus_campaigns(tier_points, metadata)

        return {
            'base_points': round(base_points, 2),
            'tier_bonus': round(tier_points - base_points, 2),
            'campaign_bonus': round(final_points - tier_points, 2),
            'total_points': round(final_points, 2),
            'tier': tier,
            'multiplier': self.TIER_MULTIPLIERS.get(tier, 1.0),
            'campaign_applied': campaign
        }

    def calculate_tier(self, lifetime_points: float) -> str:
        """Determine customer tier based on lifetime points"""
        for tier in reversed(['platinum', 'gold', 'silver', 'bronze']):
            if lifetime_points >= self.TIER_THRESHOLDS[tier]:
                return tier
        return 'bronze'

    def calculate_redemption_value(self, points: float) -> float:
        """Calculate rupee value of points"""
        config = self.load_merchant_config()
        rate = config['redemption_rate']

        value_per_point = rate['value'] / rate['points']
        return points * value_per_point


# ============================================================================
# 4. REDEMPTION ENGINE
# ============================================================================

class RedemptionEngine:
    """Handle points redemption"""

    def __init__(self):
        self.customer_db = CentralCustomerDB()
        self.transaction_engine = TransactionEngine()

    def redeem_points(self, customer_id: str, merchant_id: str,
                     points_to_redeem: float, purchase_amount: float) -> Dict:
        """Redeem points for discount"""
        customer = self.customer_db.get_customer_by_id(customer_id)

        if not customer:
            return {'success': False, 'error': 'Customer not found'}

        current_balance = customer.get('points_balance', 0)

        if points_to_redeem > current_balance:
            return {'success': False, 'error': 'Insufficient points'}

        # Calculate discount value
        points_engine = PointsEngine(merchant_id)
        discount_value = points_engine.calculate_redemption_value(points_to_redeem)

        if discount_value > purchase_amount:
            discount_value = purchase_amount
            points_to_redeem = discount_value / (points_engine.load_merchant_config()['redemption_rate']['value'] / points_engine.load_merchant_config()['redemption_rate']['points'])

        # Deduct points
        new_balance = current_balance - points_to_redeem
        self.customer_db.update_customer(customer_id, {'points_balance': new_balance})

        # Record transaction
        transaction = self.transaction_engine.create_transaction(
            transaction_type='redeem',
            customer_id=customer_id,
            merchant_id=merchant_id,
            amount=purchase_amount,
            points=-points_to_redeem,
            description=f'Redeemed {points_to_redeem} points for ₹{discount_value} discount'
        )

        return {
            'success': True,
            'points_redeemed': points_to_redeem,
            'discount_value': discount_value,
            'new_balance': new_balance,
            'transaction_id': transaction['transaction_id']
        }


# ============================================================================
# 5. SETTLEMENT SYSTEM (Network ready, currently disabled)
# ============================================================================

class SettlementSystem:
    """Track settlements between merchants (for coalition network)"""

    def __init__(self, data_dir='central_data'):
        self.data_dir = data_dir
        self.settlements_file = os.path.join(data_dir, 'settlements.json')
        self.ensure_data_dir()
        self.network_enabled = False  # DISABLED for now

    def ensure_data_dir(self):
        os.makedirs(self.data_dir, exist_ok=True)

    def calculate_merchant_liability(self, merchant_id: str) -> Dict:
        """Calculate points liability for a merchant"""
        transaction_engine = TransactionEngine()
        transactions = transaction_engine.get_merchant_transactions(merchant_id)

        points_issued = sum(t['points'] for t in transactions if t['type'] == 'earn' and t['points'] > 0)
        points_redeemed = abs(sum(t['points'] for t in transactions if t['type'] == 'redeem'))
        outstanding = points_issued - points_redeemed

        return {
            'merchant_id': merchant_id,
            'points_issued': points_issued,
            'points_redeemed': points_redeemed,
            'outstanding_points': outstanding,
            'calculated_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }


# ============================================================================
# 6. FRAUD DETECTION
# ============================================================================

class FraudDetection:
    """Basic fraud detection and prevention"""

    @staticmethod
    def check_transaction(customer_id: str, amount: float,
                         merchant_id: str) -> Tuple[bool, str]:
        """Check transaction for fraud patterns"""

        transaction_engine = TransactionEngine()
        recent_txns = transaction_engine.get_customer_transactions(customer_id, limit=10)

        # Check 1: Velocity check (max 5 transactions per hour)
        one_hour_ago = (datetime.now() - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
        recent_hour = [t for t in recent_txns if t.get('timestamp', '') > one_hour_ago]

        if len(recent_hour) > 5:
            return False, "Too many transactions in short period"

        # Check 2: Abnormal amount (>10x average)
        if recent_txns:
            avg_amount = sum(t.get('amount', 0) for t in recent_txns) / len(recent_txns)
            if amount > avg_amount * 10:
                return False, "Abnormally high transaction amount"

        # Check 3: Duplicate transaction
        for txn in recent_txns[:5]:
            if (txn.get('amount') == amount and
                txn.get('merchant_id') == merchant_id and
                (datetime.now() - datetime.fromisoformat(txn.get('timestamp'))).seconds < 300):
                return False, "Possible duplicate transaction"

        return True, "Transaction approved"


# ============================================================================
# 7. MAIN PAYBACK ENGINE (Orchestrator)
# ============================================================================

class PaybackEngine:
    """Main engine that orchestrates all components"""

    def __init__(self, merchant_id: str):
        self.merchant_id = merchant_id
        self.customer_db = CentralCustomerDB()
        self.transaction_engine = TransactionEngine()
        self.points_engine = PointsEngine(merchant_id)
        self.redemption_engine = RedemptionEngine()
        self.settlement = SettlementSystem()
        self.fraud = FraudDetection()

    def process_purchase(self, customer_phone: str, amount: float,
                        description: str = '', metadata: Dict = None) -> Dict:
        """Complete purchase flow: validate, calculate, award points"""

        # Get or create customer
        customer = self.customer_db.get_customer_by_phone(customer_phone)
        if not customer:
            return {'success': False, 'error': 'Customer not found. Please enroll first.'}

        customer_id = customer['localkard_id']

        # Fraud check
        fraud_ok, fraud_msg = self.fraud.check_transaction(customer_id, amount, self.merchant_id)
        if not fraud_ok:
            return {'success': False, 'error': f'Fraud check failed: {fraud_msg}'}

        # Calculate points
        tier = customer.get('tier', 'bronze')
        points_breakdown = self.points_engine.calculate_total_points(amount, tier, metadata)
        points_earned = points_breakdown['total_points']

        # Update customer
        new_balance = customer.get('points_balance', 0) + points_earned
        new_lifetime = customer.get('lifetime_points', 0) + points_earned
        new_tier = self.points_engine.calculate_tier(new_lifetime)

        self.customer_db.update_customer(customer_id, {
            'points_balance': new_balance,
            'lifetime_points': new_lifetime,
            'tier': new_tier,
            'last_transaction': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'transaction_count': customer.get('transaction_count', 0) + 1
        })

        # Record transaction
        transaction = self.transaction_engine.create_transaction(
            transaction_type='earn',
            customer_id=customer_id,
            merchant_id=self.merchant_id,
            amount=amount,
            points=points_earned,
            description=description or f'Purchase of ₹{amount}',
            metadata={'points_breakdown': points_breakdown}
        )

        return {
            'success': True,
            'transaction_id': transaction['transaction_id'],
            'customer_name': customer['name'],
            'customer_tier': new_tier,
            'amount': amount,
            'points_earned': points_earned,
            'points_breakdown': points_breakdown,
            'new_balance': new_balance,
            'lifetime_points': new_lifetime,
            'tier_upgraded': new_tier != tier
        }

    def get_customer_summary(self, customer_phone: str) -> Dict:
        """Get complete customer summary"""
        customer = self.customer_db.get_customer_by_phone(customer_phone)
        if not customer:
            return {'error': 'Customer not found'}

        transactions = self.transaction_engine.get_customer_transactions(
            customer['localkard_id'], limit=10
        )

        return {
            'customer': customer,
            'recent_transactions': transactions,
            'redemption_value': self.points_engine.calculate_redemption_value(
                customer.get('points_balance', 0)
            )
        }
