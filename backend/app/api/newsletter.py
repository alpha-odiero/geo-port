from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.schemas.newsletter import NewsletterSubscribe, NewsletterSubscriberResponse
from app.models.newsletter import NewsletterSubscriber
from app.api.deps import get_current_admin
from app.models.user import User

router = APIRouter(prefix="/newsletter", tags=["Newsletter Marketing"])

@router.post("/subscribe", response_model=NewsletterSubscriberResponse, status_code=status.HTTP_201_CREATED)
def subscribe_newsletter(
    subscriber_in: NewsletterSubscribe, 
    db: Session = Depends(get_db)
):
    """
    Onboard a new reader to the email newsletter. Checks for duplicate registration.
    """
    existing_sub = db.query(NewsletterSubscriber).filter(
        NewsletterSubscriber.email == subscriber_in.email
    ).first()
    if existing_sub:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This email address is already subscribed to our newsletter."
        )
        
    db_sub = NewsletterSubscriber(email=subscriber_in.email)
    db.add(db_sub)
    db.commit()
    db.refresh(db_sub)
    return db_sub

@router.get("", response_model=List[NewsletterSubscriberResponse])
def get_subscribers(
    db: Session = Depends(get_db), 
    admin: User = Depends(get_current_admin)
):
    """
    List all active newsletter email subscribers (Administrator privilege required).
    """
    return db.query(NewsletterSubscriber).all()
