from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.services.auth_service import AuthService
from app.core.config import settings
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    """
    Extracts the JWT token from the Authorization header, decodes it,
    and returns the fully validated DB User instance.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new customer or administrator account.
    """
    return AuthService.register_user(db, user_data)

@router.post("/login", response_model=Token)
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate account credentials and issue a signed JSON Web Token (JWT).
    """
    return AuthService.authenticate_user(db, login_data)

@router.get("/me", response_model=UserResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    """
    Retrieve the current authenticated user's profile information.
    """
    return current_user


# --- Security & Access Control Dependencies ---

def check_admin_privilege(current_user: User = Depends(get_current_user)) -> User:
    """
    Dependency that enforces administrator role status in order to access
    sensitive operational datasets and admin console dashboard charts.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: Administrator credentials required to query this operational dataset."
        )
    return current_user


def check_user_shipment_access(
    tracking_number: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Dependency to restrict tracking information retrieval of specific consignments.
    Allows administrator access, or limits customers to their designated shipments matches.
    """
    from app.models.shipment import Shipment
    shipment = db.query(Shipment).filter(Shipment.tracking_number == tracking_number).first()
    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Shipment matching tracking number '{tracking_number}' does not exist."
        )

    # Authorization Guard: Validate administrator role or confirm shipment recipient ownership match
    if current_user.role != "admin" and current_user.name.lower() != shipment.customer_name.lower():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: You do not possess clearance privileges for this shipment record."
        )
    return shipment

