import bcrypt


def hash_password(password):
    """
    Hash a password using bcrypt.
    
    Args:
        password: Plain text password string
    
    Returns:
        Hashed password string
    """
    # Convert password to bytes
    password_bytes = password.encode('utf-8')
    # Generate salt and hash
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    # Return as string
    return hashed.decode('utf-8')


def verify_password(password, hashed):
    """
    Verify a password against a bcrypt hash.
    
    Args:
        password: Plain text password to verify
        hashed: Bcrypt hashed password
    
    Returns:
        True if password matches, False otherwise
    """
    # Convert to bytes
    password_bytes = password.encode('utf-8')
    hashed_bytes = hashed.encode('utf-8')
    # Verify
    return bcrypt.checkpw(password_bytes, hashed_bytes)
