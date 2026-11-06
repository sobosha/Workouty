from pwdlib import PasswordHash

password_hasher = PasswordHash.recommended()

def hash_password(password: str) -> str:
    """Hash a password using Argon2."""
    return password_hasher.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return password_hasher.verify(password, hashed_password)

def verify_email_format(email: str) -> bool:
    """Verify if the email format is valid."""
    import re
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None