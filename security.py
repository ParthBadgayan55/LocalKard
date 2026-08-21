"""
LocalKard Security Module
Handles authentication, password hashing, and security utilities
"""

import bcrypt
import re
import uuid
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import config

# ============================================================================
# PASSWORD HASHING
# ============================================================================

def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt

    Args:
        password: Plain text password

    Returns:
        Hashed password as string
    """
    # Convert password to bytes
    password_bytes = password.encode('utf-8')

    # Generate salt and hash
    salt = bcrypt.gensalt(rounds=config.BCRYPT_ROUNDS)
    hashed = bcrypt.hashpw(password_bytes, salt)

    # Return as string
    return hashed.decode('utf-8')


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash

    Args:
        password: Plain text password to verify
        hashed_password: Stored hashed password

    Returns:
        True if password matches, False otherwise
    """
    try:
        password_bytes = password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception as e:
        print(f"Password verification error: {e}")
        return False


# ============================================================================
# PHONE NUMBER VALIDATION
# ============================================================================

def validate_phone_number(phone: str) -> tuple[bool, Optional[str]]:
    """
    Validate Indian phone number format

    Args:
        phone: Phone number string

    Returns:
        Tuple of (is_valid, error_message)
    """
    # Remove any spaces or dashes
    phone = phone.strip().replace(' ', '').replace('-', '')

    # Check if matches pattern
    if not re.match(config.PHONE_PATTERN, phone):
        return False, config.PHONE_ERROR_MESSAGE

    return True, None


def sanitize_phone_number(phone: str) -> str:
    """
    Sanitize phone number by removing non-digits

    Args:
        phone: Phone number string

    Returns:
        Sanitized phone number (digits only)
    """
    return re.sub(r'\D', '', phone)


# ============================================================================
# UNIQUE ID GENERATION
# ============================================================================

def generate_transaction_id() -> str:
    """
    Generate unique transaction ID using UUID

    Returns:
        Transaction ID string (e.g., "TXN-a1b2c3d4")
    """
    if config.USE_UUID_FOR_TRANSACTIONS:
        # Use first 8 characters of UUID
        unique_id = str(uuid.uuid4())[:8]
        return f"{config.TRANSACTION_ID_PREFIX}-{unique_id}"
    else:
        # Fallback to timestamp-based
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        return f"{config.TRANSACTION_ID_PREFIX}-{timestamp}"


def generate_customer_id(phone: str) -> str:
    """
    Generate customer ID (LocalKard ID)

    Args:
        phone: Customer phone number

    Returns:
        Customer ID string (e.g., "LK00000001")
    """
    # For now, use counter-based system
    # In production, would query database for next available number
    # This is just a placeholder - actual implementation in payback_engine
    return f"{config.CUSTOMER_ID_PREFIX}00000001"


# ============================================================================
# INPUT SANITIZATION
# ============================================================================

def sanitize_string(input_str: str, max_length: int = 200) -> str:
    """
    Sanitize user input string

    Args:
        input_str: Input string to sanitize
        max_length: Maximum allowed length

    Returns:
        Sanitized string
    """
    # Remove leading/trailing whitespace
    sanitized = input_str.strip()

    # Truncate to max length
    sanitized = sanitized[:max_length]

    # Remove any null bytes
    sanitized = sanitized.replace('\x00', '')

    return sanitized


def sanitize_amount(amount: Any) -> float:
    """
    Sanitize and validate amount

    Args:
        amount: Amount value (can be string or number)

    Returns:
        Sanitized amount as float

    Raises:
        ValueError: If amount is invalid
    """
    try:
        # Convert to float
        amount_float = float(amount)

        # Must be positive
        if amount_float <= 0:
            raise ValueError("Amount must be positive")

        # Round to 2 decimal places
        return round(amount_float, 2)
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid amount: {amount}") from e


# ============================================================================
# SESSION MANAGEMENT
# ============================================================================

def create_session_token() -> str:
    """
    Create a secure session token

    Returns:
        Session token string
    """
    return str(uuid.uuid4())


def is_session_expired(login_time: datetime, timeout_minutes: int = None) -> bool:
    """
    Check if session has expired

    Args:
        login_time: When user logged in
        timeout_minutes: Session timeout in minutes (uses config default if None)

    Returns:
        True if expired, False otherwise
    """
    if timeout_minutes is None:
        timeout_minutes = config.SESSION_TIMEOUT_MINUTES

    timeout_delta = timedelta(minutes=timeout_minutes)
    return datetime.now() > (login_time + timeout_delta)


# ============================================================================
# DATA VALIDATION
# ============================================================================

def validate_email(email: str) -> tuple[bool, Optional[str]]:
    """
    Validate email format

    Args:
        email: Email address string

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not email:
        return True, None  # Email is optional

    # Basic email regex
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if not re.match(email_pattern, email):
        return False, "Invalid email format"

    return True, None


def validate_points(points: Any) -> tuple[bool, Optional[str]]:
    """
    Validate points value

    Args:
        points: Points value to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        points_float = float(points)

        if points_float < 0:
            return False, "Points cannot be negative"

        if points_float > 1000000:
            return False, "Points value too large"

        return True, None
    except (ValueError, TypeError):
        return False, "Invalid points value"


# ============================================================================
# SECURITY HELPERS
# ============================================================================

def mask_phone_number(phone: str) -> str:
    """
    Mask phone number for display (show last 4 digits)

    Args:
        phone: Full phone number

    Returns:
        Masked phone number (e.g., "******1234")
    """
    if len(phone) <= 4:
        return phone

    return '*' * (len(phone) - 4) + phone[-4:]


def is_strong_password(password: str) -> tuple[bool, Optional[str]]:
    """
    Check if password meets strength requirements

    Args:
        password: Password to check

    Returns:
        Tuple of (is_strong, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters"

    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"

    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"

    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"

    return True, None


# ============================================================================
# EXPORT ALL
# ============================================================================

__all__ = [
    'hash_password',
    'verify_password',
    'validate_phone_number',
    'sanitize_phone_number',
    'generate_transaction_id',
    'generate_customer_id',
    'sanitize_string',
    'sanitize_amount',
    'create_session_token',
    'is_session_expired',
    'validate_email',
    'validate_points',
    'mask_phone_number',
    'is_strong_password'
]
