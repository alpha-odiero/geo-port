import json
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.shipment_repository import ShipmentRepository
from app.utils.cache import cache_service

class TrackingService:
    @staticmethod
    def get_shipment_status(db: Session, tracking_number: str) -> dict:
        cache_key = f"shipment:{tracking_number}"
        
        # 1. Check Redis cache first
        cached_data = cache_service.get(cache_key)
        if cached_data:
            try:
                return json.loads(cached_data)
            except Exception:
                pass  # Parse error fallback
                
        # 2. DB read on cache miss
        shipment = ShipmentRepository.get_by_tracking_number(db, tracking_number)
        if not shipment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Shipment with tracking number '{tracking_number}' not found."
            )
            
        # 3. Assemble response representation
        shipment_payload = {
            "tracking_number": shipment.tracking_number,
            "status": shipment.status,
            "current_location": shipment.current_location,
            "expected_delivery": shipment.expected_delivery
        }
        
        # 4. Save to Cache for 300 seconds
        cache_service.set(cache_key, json.dumps(shipment_payload), expire=300)
        return shipment_payload
