from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
import uuid
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE, REFRESH_TOKEN_EXPIRE

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_ctx.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_ctx.verify(plain, hashed)

def create_access_token(subject: str) -> str:
    expire = datetime.utcnow() + ACCESS_TOKEN_EXPIRE
    to_encode = {"sub": subject, "type": "access", "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(subject: str) -> tuple[str, str]:
    jti = str(uuid.uuid4())
    expire = datetime.utcnow() + REFRESH_TOKEN_EXPIRE
    to_encode = {"sub": subject, "type": "refresh", "jti": jti, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM), jti

def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError as e:
        raise e
