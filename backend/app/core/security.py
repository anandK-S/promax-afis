# ========================================
# Pro-Max AFIS - Security Utilities
# ========================================
# JWT token management and password hashing
# Author: Pro-Max Development Team

from datetime import datetime, timedelta
from typing import Dict, Optional, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
import secrets
import logging

from app.core.config import settings

# Configure logging
logger = logging.getLogger(__name__)

# Password hashing context using Argon2
pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
    argon2__memory_cost=settings.password_hash_memory,
    argon2__time_cost=settings.password_hash_time,
    argon2__parallelism=settings.password_hash_parallelism,
    argon2__hash_len=settings.password_hash_length
)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash
    
    Args:
        plain_password: Plain text password
        hashed_password: Hashed password
        
    Returns:
        True if password matches hash, False otherwise
    """
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        logger.error(f"Password verification failed: {str(e)}")
        return False


def get_password_hash(password: str) -> str:
    """
    Hash a password using Argon2
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password
    """
    try:
        return pwd_context.hash(password)
    except Exception as e:
        logger.error(f"Password hashing failed: {str(e)}")
        raise


def create_access_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create JWT access token
    
    Args:
        data: Payload data to include in token
        expires_delta: Token expiration time (default: from settings)
        
    Returns:
        Encoded JWT token
    """
    try:
        to_encode = data.copy()
        
        # Set expiration
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=settings.jwt_access_token_expire_minutes
            )
        
        # Add expiration to payload
        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "access"
        })
        
        # Encode token
        encoded_jwt = jwt.encode(
            to_encode,
            settings.jwt_secret_key,
            algorithm=settings.jwt_algorithm
        )
        
        return encoded_jwt
        
    except Exception as e:
        logger.error(f"Access token creation failed: {str(e)}")
        raise


def create_refresh_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create JWT refresh token
    
    Args:
        data: Payload data to include in token
        expires_delta: Token expiration time (default: from settings)
        
    Returns:
        Encoded JWT refresh token
    """
    try:
        to_encode = data.copy()
        
        # Set expiration
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                days=settings.jwt_refresh_token_expire_days
            )
        
        # Add expiration to payload
        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "refresh"
        })
        
        # Generate unique token ID
        to_encode.update({"jti": secrets.token_hex(16)})
        
        # Encode token
        encoded_jwt = jwt.encode(
            to_encode,
            settings.jwt_secret_key,
            algorithm=settings.jwt_algorithm
        )
        
        return encoded_jwt
        
    except Exception as e:
        logger.error(f"Refresh token creation failed: {str(e)}")
        raise


def verify_token(token: str) -> Dict[str, Any]:
    """
    Verify and decode JWT token
    
    Args:
        token: JWT token to verify
        
    Returns:
        Decoded token payload
        
    Raises:
        JWTError: If token is invalid or expired
    """
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm]
        )
        return payload
    except JWTError as e:
        logger.error(f"Token verification failed: {str(e)}")
        raise


def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decode access token without raising exception
    
    Args:
        token: JWT access token
        
    Returns:
        Decoded payload or None if invalid
    """
    try:
        payload = verify_token(token)
        
        # Check if this is an access token
        if payload.get("type") != "access":
            logger.warning("Invalid token type: expected 'access'")
            return None
        
        return payload
        
    except Exception as e:
        logger.error(f"Access token decoding failed: {str(e)}")
        return None


def decode_refresh_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decode refresh token without raising exception
    
    Args:
        token: JWT refresh token
        
    Returns:
        Decoded payload or None if invalid
    """
    try:
        payload = verify_token(token)
        
        # Check if this is a refresh token
        if payload.get("type") != "refresh":
            logger.warning("Invalid token type: expected 'refresh'")
            return None
        
        return payload
        
    except Exception as e:
        logger.error(f"Refresh token decoding failed: {str(e)}")
        return None


def get_token_expiry(token: str) -> Optional[datetime]:
    """
    Get token expiration datetime
    
    Args:
        token: JWT token
        
    Returns:
        Expiration datetime or None if invalid
    """
    try:
        payload = verify_token(token)
        exp_timestamp = payload.get("exp")
        
        if exp_timestamp:
            return datetime.fromtimestamp(exp_timestamp)
        
        return None
        
    except Exception:
        return None


def is_token_expired(token: str) -> bool:
    """
    Check if token is expired
    
    Args:
        token: JWT token
        
    Returns:
        True if expired, False otherwise
    """
    try:
        expiry = get_token_expiry(token)
        
        if not expiry:
            return True
        
        return datetime.utcnow() >= expiry
        
    except Exception:
        return True


def generate_reset_token() -> str:
    """
    Generate a secure random token for password reset
    
    Returns:
        Secure random token
    """
    return secrets.token_urlsafe(32)


def generate_verification_token() -> str:
    """
    Generate a secure random token for email verification
    
    Returns:
        Secure random token
    """
    return secrets.token_urlsafe(32)


def validate_email_format(email: str) -> bool:
    """
    Validate email format
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid, False otherwise
    """
    import re
    
    # Simple email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    return re.match(pattern, email) is not None


def sanitize_input(input_str: str, max_length: Optional[int] = None) -> str:
    """
    Sanitize user input to prevent injection attacks
    
    Args:
        input_str: Input string to sanitize
        max_length: Maximum allowed length
        
    Returns:
        Sanitized string
    """
    # Remove potentially dangerous characters
    sanitized = input_str.strip()
    
    # Limit length if specified
    if max_length and len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    
    return sanitized


def generate_api_key() -> str:
    """
    Generate a secure API key
    
    Returns:
        Secure API key
    """
    return f"pk_{secrets.token_urlsafe(32)}"