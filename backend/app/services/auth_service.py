from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserLogin, Token
from app.core.security import get_password_hash, verify_password, create_access_token

class AuthService:
    @staticmethod
    def register_user(db: Session, user_data: UserCreate):
        # 1. Check if email already registered
        existing_user = UserRepository.get_by_email(db, user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email address already registered."
            )
        # 2. Hash sensitive password
        hashed_password = get_password_hash(user_data.password)
        # 3. Create record in repository
        return UserRepository.create(db, user_data, hashed_password)

    @staticmethod
    def authenticate_user(db: Session, login_data: UserLogin) -> Token:
        user = UserRepository.get_by_email(db, login_data.email)
        if not user or not verify_password(login_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email address or password.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Build access token with claims
        access_token = create_access_token(data={"sub": user.email, "role": user.role})
        return Token(access_token=access_token, token_type="bearer")
