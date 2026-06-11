from sqlalchemy.orm import Session
from app.models.quote import Quote
from app.schemas.quote import QuoteCreate

class QuoteService:
    @staticmethod
    def create_quote(db: Session, quote_in: QuoteCreate) -> Quote:
        # Business estimate: e.g. base Rate $50 + $2.5 per kg
        db_quote = Quote(
            name=quote_in.name,
            email=quote_in.email,
            service=quote_in.service,
            cargo_weight=quote_in.cargo_weight
        )
        db.add(db_quote)
        db.commit()
        db.refresh(db_quote)
        return db_quote
