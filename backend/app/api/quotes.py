from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.schemas.quote import QuoteCreate, QuoteResponse
from app.models.quote import Quote
from app.api.deps import get_current_admin
from app.models.user import User

router = APIRouter(prefix="/quotes", tags=["Quote Requests"])

@router.post("", response_model=QuoteResponse, status_code=status.HTTP_201_CREATED)
def create_quote(quote_in: QuoteCreate, db: Session = Depends(get_db)):
    """
    Submit a freight shipment rate/quote request. Open to all users.
    Generates a real tracking number and creates a corresponding shipment tracker.
    """
    import random
    from app.models.shipment import Shipment

    # Generate unique 6-digit tracking number prefixed with GP
    tracking_number = f"GP{random.randint(100000, 999999)}"

    db_quote = Quote(
        name=quote_in.name,
        email=quote_in.email,
        service=quote_in.service,
        cargo_weight=quote_in.cargo_weight,
        tracking_number=tracking_number
    )
    db.add(db_quote)

    # Automatically provision a real shipment record linked to this booking quote
    db_shipment = Shipment(
        tracking_number=tracking_number,
        customer_name=quote_in.name,
        status="Booked / Processing",
        current_location="Awaiting Handling (Departure Terminal)",
        expected_delivery="Est. 3-5 Business Days upon Dispatch"
    )
    db.add(db_shipment)

    db.commit()
    db.refresh(db_quote)
    return db_quote

@router.get("", response_model=List[QuoteResponse])
def get_all_quotes(
    db: Session = Depends(get_db), 
    admin: User = Depends(get_current_admin)
):
    """
    Retrieve all submitted quote requests (Administrator privilege required).
    """
    return db.query(Quote).all()

@router.get("/{quote_id}", response_model=QuoteResponse)
def get_quote_by_id(
    quote_id: int, 
    db: Session = Depends(get_db), 
    admin: User = Depends(get_current_admin)
):
    """
    Get detailed metrics of a specific quote request (Administrator privilege required).
    """
    db_quote = db.query(Quote).filter(Quote.id == quote_id).first()
    if not db_quote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Quote request not found."
        )
    return db_quote
