from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.api.deps import get_current_admin
from app.models.user import User
from app.models.shipment import Shipment
from app.models.quote import Quote
from app.models.newsletter import NewsletterSubscriber

router = APIRouter(prefix="/dashboard", tags=["Admin Dashboard Metrics"])

@router.get("/stats")
def get_dashboard_stats(
    db: Session = Depends(get_db), 
    admin: User = Depends(get_current_admin)
):
    """
    Consolidated live metrics count of database states across all models.
    (Administrator privilege required).
    """
    users_count = db.query(User).count()
    shipments_count = db.query(Shipment).count()
    quotes_count = db.query(Quote).count()
    subscribers_count = db.query(NewsletterSubscriber).count()
    
    return {
        "users": users_count,
        "shipments": shipments_count,
        "quotes": quotes_count,
        "subscribers": subscribers_count
    }
