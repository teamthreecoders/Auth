import re

from app.exception.exception import EmailFormatError,PasswordFormatError


# ====================
# Validators
# ====================
def validate_email(email: str) -> None:
    """Validate email format"""
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(regex, email):
        raise EmailFormatError(" Invalid email format ")


def validate_password(password: str) -> None:
    """Validate password strength"""
    if len(password) < 8:
        raise PasswordFormatError("Password must be at least 8 characters long")
    if not re.search(r'[A-Z]', password):
        raise PasswordFormatError("Password must contain at least one uppercase letter")
    if not re.search(r'[a-z]', password):
        raise PasswordFormatError("Password must contain at least one lowercase letter")
    if not re.search(r'\d', password):
        raise PasswordFormatError("Password must contain at least one digit")
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise PasswordFormatError("Password must contain at least one special character")
