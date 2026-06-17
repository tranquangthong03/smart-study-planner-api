from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.core.security import create_access_token, hash_password, verify_password
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.user import UserCreate, UserResponse

router = APIRouter(prefix="/auth", tags=["Auth"])
@router.post("/register", response_model= UserResponse, status_code=status.HTTP_201_CREATED)
def register(
  user_data: UserCreate, # Dữ liệu đầu vào
  db: Session = Depends(get_db) # Tạo phiên đăng nhập
):
  existing_user = db.query(User).filter(User.email == user_data.email).first()
  # Nếu tìm thấy email đã đăng kí rồi thì trả ra lỗi
  if existing_user:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="Email already registered",
    )
  
  # nếu chưa đăng kí thì tạo user mới
  new_user = User(
    email=user_data.email,
    full_name=user_data.full_name,
    hashed_password=hash_password(user_data.password)
  )
  db.add(new_user)
  db.commit()
  db.refresh(new_user)

  return new_user


@router.post("/login", response_model=TokenResponse)
def login(
  login_data: LoginRequest,
  db: Session = Depends(get_db)
):
  user = db.query(User).filter(User.email == login_data.email).first()
  if user is None:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Incorrect email or password",
      headers={"WWW-Authenticate": "Bearer"},
    )

  # Băm mật khẩu 1 lần nữa và so sánh
  if not verify_password(login_data.password, user.hashed_password):
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Incorrect email or password",
      headers={"WWW-Authenticate": "Bearer"},
    )
  access_token = create_access_token(subject=user.id)
  return TokenResponse(access_token=access_token)

# Get current user
@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
  return current_user