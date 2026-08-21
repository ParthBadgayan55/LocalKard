"""
LocalKard Configuration
Centralized configuration for all system settings
"""

import os
from pathlib import Path

# ============================================================================
# DIRECTORY CONFIGURATION
# ============================================================================

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / 'merchant_data'
CENTRAL_DATA_DIR = BASE_DIR / 'central_data'
BACKUP_DIR = BASE_DIR / 'backups'

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
CENTRAL_DATA_DIR.mkdir(exist_ok=True)
BACKUP_DIR.mkdir(exist_ok=True)

# ============================================================================
# SECURITY CONFIGURATION
# ============================================================================

# Password hashing rounds (higher = more secure but slower)
BCRYPT_ROUNDS = 12

# Session configuration
SESSION_TIMEOUT_MINUTES = 30
REMEMBER_ME_DAYS = 30

# ============================================================================
# PHONE NUMBER VALIDATION
# ============================================================================

# Indian phone number pattern (10 digits, starts with 6-9)
PHONE_PATTERN = r'^[6-9]\d{9}$'
PHONE_ERROR_MESSAGE = "Phone number must be 10 digits starting with 6-9"

# ============================================================================
# TRANSACTION CONFIGURATION
# ============================================================================

# Use UUID for transaction IDs instead of counter
USE_UUID_FOR_TRANSACTIONS = True

# Transaction ID prefix
TRANSACTION_ID_PREFIX = "TXN"
CUSTOMER_ID_PREFIX = "LK"

# ============================================================================
# LOYALTY CONFIGURATION
# ============================================================================

# Points calculation
DEFAULT_EARNING_RATE = {
    'amount': 100,  # Spend ₹100
    'points': 5     # Get 5 points
}

DEFAULT_REDEMPTION_RATE = {
    'points': 100,   # Redeem 100 points
    'value': 10      # Worth ₹10
}

# Tier thresholds
TIER_THRESHOLDS = {
    'bronze': 0,
    'silver': 500,
    'gold': 2000,
    'platinum': 5000
}

# Tier multipliers
TIER_MULTIPLIERS = {
    'bronze': 1.0,
    'silver': 1.25,
    'gold': 1.5,
    'platinum': 2.0
}

# ============================================================================
# FRAUD DETECTION CONFIGURATION
# ============================================================================

# Maximum transactions per hour per customer
MAX_TRANSACTIONS_PER_HOUR = 5

# Maximum transaction amount multiplier (vs average)
ABNORMAL_AMOUNT_MULTIPLIER = 10

# Duplicate transaction window (minutes)
DUPLICATE_TRANSACTION_WINDOW = 5

# ============================================================================
# BACKUP CONFIGURATION
# ============================================================================

# Automatic backup frequency
BACKUP_ENABLED = True
BACKUP_FREQUENCY_HOURS = 24

# Number of backups to keep
BACKUP_RETENTION_COUNT = 7

# ============================================================================
# UI CONFIGURATION
# ============================================================================

# Color palette
COLORS = {
    'primary': '#6366F1',      # Indigo
    'success': '#10B981',      # Emerald
    'warning': '#F59E0B',      # Amber
    'danger': '#EF4444',       # Rose
    'info': '#3B82F6',         # Blue
    'purple': '#8B5CF6',       # Purple
    'gold': '#F59E0B',         # Gold
    'silver': '#94A3B8',       # Silver
    'bronze': '#CD7F32',       # Bronze
    'light_bg': '#F9FAFB',     # Almost white
    'card_bg': '#FFFFFF',      # Pure white
    'border': '#E5E7EB',       # Light border
    'text_dark': '#111827',    # Almost black
    'text_muted': '#6B7280'    # Gray
}

# Tier colors
TIER_COLORS = {
    'bronze': COLORS['bronze'],
    'silver': COLORS['silver'],
    'gold': COLORS['gold'],
    'platinum': COLORS['purple']
}

# ============================================================================
# NOTIFICATION CONFIGURATION (For future use)
# ============================================================================

# SMS/WhatsApp settings (placeholder)
SMS_ENABLED = False
WHATSAPP_ENABLED = False

# Email settings (placeholder)
EMAIL_ENABLED = False
EMAIL_FROM = "noreply@localkard.com"

# ============================================================================
# ANALYTICS CONFIGURATION
# ============================================================================

# Dashboard refresh interval (seconds)
DASHBOARD_REFRESH_INTERVAL = 60

# Chart colors
CHART_COLORS = [
    COLORS['primary'],
    COLORS['success'],
    COLORS['warning'],
    COLORS['purple'],
    COLORS['info']
]

# ============================================================================
# COMPLIANCE CONFIGURATION (India)
# ============================================================================

# GST configuration
GST_ENABLED = False  # Enable when merchant has GST
GST_RATE_PERCENT = 18

# Data retention (as per Indian regulations)
DATA_RETENTION_DAYS = 2555  # 7 years

# ============================================================================
# FEATURE FLAGS
# ============================================================================

# Enable/disable features
FEATURES = {
    'customer_portal': False,     # TODO: Build customer portal
    'redemption_flow': False,     # TODO: Implement redemption
    'sms_notifications': False,   # TODO: Add SMS integration
    'whatsapp_notifications': False,  # TODO: Add WhatsApp
    'referral_program': False,    # TODO: Build referrals
    'campaigns': False,           # TODO: Campaign management
    'multi_currency': False,      # Only INR for now
    'coalition_network': False,   # Disabled (no license yet)
}

# ============================================================================
# DEVELOPMENT/DEBUG SETTINGS
# ============================================================================

DEBUG_MODE = False
LOG_LEVEL = 'INFO'  # DEBUG, INFO, WARNING, ERROR

# ============================================================================
# ENVIRONMENT-SPECIFIC OVERRIDES
# ============================================================================

# Check for environment variables
if os.getenv('LOCALKARD_ENV') == 'production':
    DEBUG_MODE = False
    BACKUP_ENABLED = True
    SESSION_TIMEOUT_MINUTES = 15  # Shorter in production

if os.getenv('LOCALKARD_ENV') == 'development':
    DEBUG_MODE = True
    BACKUP_ENABLED = False
    SESSION_TIMEOUT_MINUTES = 120  # Longer in dev

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_data_path(merchant_phone: str, filename: str) -> Path:
    """Get full path for merchant data file"""
    merchant_dir = DATA_DIR / merchant_phone
    merchant_dir.mkdir(exist_ok=True)
    return merchant_dir / filename

def get_central_data_path(filename: str) -> Path:
    """Get full path for central data file"""
    return CENTRAL_DATA_DIR / filename

def get_backup_path(filename: str) -> Path:
    """Get full path for backup file"""
    return BACKUP_DIR / filename

# ============================================================================
# EXPORT ALL
# ============================================================================

__all__ = [
    'BASE_DIR', 'DATA_DIR', 'CENTRAL_DATA_DIR', 'BACKUP_DIR',
    'BCRYPT_ROUNDS', 'SESSION_TIMEOUT_MINUTES',
    'PHONE_PATTERN', 'PHONE_ERROR_MESSAGE',
    'USE_UUID_FOR_TRANSACTIONS', 'TRANSACTION_ID_PREFIX', 'CUSTOMER_ID_PREFIX',
    'DEFAULT_EARNING_RATE', 'DEFAULT_REDEMPTION_RATE',
    'TIER_THRESHOLDS', 'TIER_MULTIPLIERS',
    'MAX_TRANSACTIONS_PER_HOUR', 'ABNORMAL_AMOUNT_MULTIPLIER',
    'BACKUP_ENABLED', 'BACKUP_FREQUENCY_HOURS',
    'COLORS', 'TIER_COLORS',
    'FEATURES', 'DEBUG_MODE',
    'get_data_path', 'get_central_data_path', 'get_backup_path'
]
