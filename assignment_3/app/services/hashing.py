import bcrypt

def hash_password(password: str) -> bytes:
    encoded = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(encoded, salt)
    return hashed

def verify_password(hashed: bytes, password: str) -> bool:
    encoded = password.encode("utf-8")
    return bcrypt.checkpw(encoded, hashed)

def password_strong(password: str) -> bool:
    if len(password) < 8:
        return False
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)

    return has_upper and has_lower and has_digit and has_special