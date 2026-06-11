from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.schemas.contact import ContactMessageCreate, ContactMessageResponse
from app.models.contact import ContactMessage
from app.api.deps import get_current_admin
from app.models.user import User

router = APIRouter(prefix="/contact", tags=["Contact Inquiry Messages"])

@router.post("", response_model=ContactMessageResponse, status_code=status.HTTP_201_CREATED)
def submit_contact_message(
    message_in: ContactMessageCreate, 
    db: Session = Depends(get_db)
):
    """
    Submit a customer inquiry message via contact form. Open to public.
    """
    db_msg = ContactMessage(
        name=message_in.name,
        email=message_in.email,
        message=message_in.message
    )
    db.add(db_msg)
    db.commit()
    db.refresh(db_msg)
    return db_msg

@router.get("", response_model=List[ContactMessageResponse])
def get_contact_messages(
    db: Session = Depends(get_db), 
    admin: User = Depends(get_current_admin)
):
    """
    List all recorded customer contact messages (Administrator privilege required).
    """
    return db.query(ContactMessage).all()
