"""
Security utilities for ezy_forms app
"""
import secrets
import string
from datetime import datetime, timedelta


def generate_secure_token(length=32):
    """
    Generate a cryptographically secure random token.

    Args:
        length: Length of the token in bytes (default 32 = 256 bits)

    Returns:
        str: URL-safe token string
    """
    return secrets.token_urlsafe(length)


def generate_secure_alphanumeric_token(length=16):
    """
    Generate a cryptographically secure alphanumeric token.

    Args:
        length: Length of the token in characters (default 16)

    Returns:
        str: Alphanumeric token string
    """
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))
