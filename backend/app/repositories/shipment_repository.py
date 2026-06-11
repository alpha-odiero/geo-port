from sqlalchemy.orm import Session
from app.models.shipment import Shipment
from app.schemas.shipment import ShipmentCreate

class ShipmentRepository:
    @staticmethod
    def get_by_tracking_number(db: Session, tracking_number: str) -> Shipment:
        return db.query(Shipment).filter(Shipment.tracking_number == tracking_number).first()

    @staticmethod
    def create(db: Session, shipment: ShipmentCreate) -> Shipment:
        db_shipment = Shipment(
            tracking_number=shipment.tracking_number,
            customer_name=shipment.customer_name,
            status=shipment.status,
            current_location=shipment.current_location,
            expected_delivery=shipment.expected_delivery
        )
        db.add(db_shipment)
        db.commit()
        db.refresh(db_shipment)
        return db_shipment
