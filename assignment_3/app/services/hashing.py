import bcrypt

def hash_password(password: str) -> bytes:
    encoded = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(encoded, salt)

    return hashed

def verify_password(hashed: bytes, password: str) -> bool:
    encoded = password.encode("utf-8")
    return bcrypt.checkpw(encoded, hashed)
