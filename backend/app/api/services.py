from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.schemas.service import ServiceCreate, ServiceResponse
from app.models.service import Service
from app.api.deps import get_current_admin
from app.models.user import User

router = APIRouter(prefix="/services", tags=["Logistics Offerings"])

@router.get("", response_model=List[ServiceResponse])
def get_all_services(db: Session = Depends(get_db)):
    """
    Get all active logistics and freight services. Open to public.
    """
    return db.query(Service).all()

@router.get("/{service_id}", response_model=ServiceResponse)
def get_service(service_id: int, db: Session = Depends(get_db)):
    """
    Get granular details about a specific logistical division. Open to public.
    """
    db_service = db.query(Service).filter(Service.id == service_id).first()
    if not db_service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Logistics service item does not exist."
        )
    return db_service

@router.post("", response_model=ServiceResponse, status_code=status.HTTP_201_CREATED)
def create_service(
    service_in: ServiceCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """
    Create a new logistics service listing category (Administrator privilege required).
    """
    db_service = Service(
        title=service_in.title,
        description=service_in.description
    )
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service
