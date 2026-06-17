from datetime import datetime, timedelta, timezone
from typing import Any

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

# Đối tượng dùng để hash password
pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")

# Hàm hash password, tham số truyền vào là password của người dùng
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Hàm để xác thực mật khẩu, tham số đầu tiên là mật khẩu gốc, tham số thứ 2 là mk đã hash
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# Tạo access token
def create_access_token(subject: str | Any, expires_delta: timedelta | None = None) -> str:
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    expire = datetime.now(timezone.utc) + expires_delta

    to_encode = {
        "sub": str(subject),
        "exp": expire,
    }

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    return encoded_jwt