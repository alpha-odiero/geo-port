from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.services.tracking_service import TrackingService
from app.api.deps import get_current_admin
from app.models.user import User
from app.schemas.shipment import ShipmentCreate, ShipmentResponse, ShipmentUpdate
from app.models.shipment import Shipment
from app.utils.cache import cache_service

router = APIRouter(prefix="/tracking", tags=["Shipment Tracking"])

@router.get("/{tracking_number}")
def get_tracking(tracking_number: str, db: Session = Depends(get_db)):
    """
    Retrieve current coordinates and status of a shipment.
    Queries are cached inside Redis for 300 seconds on hit.
    """
    return TrackingService.get_shipment_status(db, tracking_number)

@router.post("", response_model=ShipmentResponse, status_code=status.HTTP_201_CREATED)
def create_shipment(
    shipment_in: ShipmentCreate, 
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """
    Create a new shipment record (Administrator privilege required).
    """
    db_shipment = Shipment(
        tracking_number=shipment_in.tracking_number,
        customer_name=shipment_in.customer_name,
        status=shipment_in.status,
        current_location=shipment_in.current_location,
        expected_delivery=shipment_in.expected_delivery
    )
    db.add(db_shipment)
    db.commit()
    db.refresh(db_shipment)
    return db_shipment

@router.put("/{tracking_number}", response_model=ShipmentResponse)
def update_shipment(
    tracking_number: str,
    shipment_in: ShipmentUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """
    Update shipment status or location (Administrator privilege required). Invalidates Redis caches.
    """
    db_shipment = db.query(Shipment).filter(Shipment.tracking_number == tracking_number).first()
    if not db_shipment:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Shipment not found")
        
    for var, value in vars(shipment_in).items():
        if value is not None:
            setattr(db_shipment, var, value)
            
    db.commit()
    db.refresh(db_shipment)
    
    # Invalidate Cache
    cache_service.delete(f"shipment:{tracking_number}")
    
    return db_shipment
