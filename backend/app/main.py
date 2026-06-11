from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.database.database import engine, Base, SessionLocal
from app.models.user import User
from app.models.shipment import Shipment
from app.models.service import Service
from app.models.project import Project

# Import Router Endpoints
from app.api.auth import router as auth_router
from app.api.tracking import router as tracking_router
from app.api.quotes import router as quotes_router
from app.api.contact import router as contact_router
from app.api.newsletter import router as newsletter_router
from app.api.services import router as services_router
from app.api.dashboard import router as dashboard_router
from app.api.projects import router as projects_router

# Initialize Database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="GeoPort Logistics REST API",
    description="Production-grade FastAPI backend demo for freight and shipping tracking with JWT security and Redis caching.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration for Frontend Connectivity
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production alignment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Validation Exception Override for unified JSON error presentation
@app.exception_handler(RequestValidationError)
async def val_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation Error",
            "details": exc.errors()
        }
    )

# Register Segment Routers
app.include_router(auth_router, prefix="/api")
app.include_router(tracking_router, prefix="/api")
app.include_router(quotes_router, prefix="/api")
app.include_router(contact_router, prefix="/api")
app.include_router(newsletter_router, prefix="/api")
app.include_router(services_router, prefix="/api")
app.include_router(dashboard_router, prefix="/api")
app.include_router(projects_router, prefix="/api")

@app.get("/", tags=["Root"])
def root_endpoint():
    return {
        "status": "online",
        "message": "Welcome to the GeoPort Logistics Backend API Engine.",
        "documentation": "/docs"
    }

# Live Seeding Routine
def seed_initial_state():
    db = SessionLocal()
    try:
        # 1. Seed default administrator credentials
        admin_email = "admin@geoportlogistics.com"
        existing_admin = db.query(User).filter(User.email == admin_email).first()
        if not existing_admin:
            from app.core.security import get_password_hash
            admin_user = User(
                name="System Administrator",
                email=admin_email,
                hashed_password=get_password_hash("admin123"),
                role="admin"
            )
            db.add(admin_user)
            db.commit()
            print("Successfully seeded standard admin credentials.")

        # 2. Seed default tracking records
        track_no = "GP123456"
        existing_shipment = db.query(Shipment).filter(Shipment.tracking_number == track_no).first()
        if not existing_shipment:
            shipping_record = Shipment(
                tracking_number=track_no,
                customer_name="East African Wholesales Ltd",
                status="In Transit",
                current_location="Nairobi Inland Container Depot",
                expected_delivery="Tomorrow morning of next cycle"
            )
            db.add(shipping_record)
            db.commit()
            print(f"Successfully seeded shipment tracking ID: {track_no}")

        # 3. Seed original Logistics offerings description
        available_services = [
            {
                "title": "Road Freight Carrier",
                "description": "Secure overland containerized distribution trucking systems tailored for inter-state commercial cargo."
            },
            {
                "title": "Sea Ocean Clearance",
                "description": "Port handling clearances and transoceanic multi-vessel shipping structures for bulk products."
            },
            {
                "title": "Logistics Storage Depot",
                "description": "Consolidated warehousing spaces with real-time payload position reporting and thermal regulates."
            }
        ]
        for service_to_add in available_services:
            matching_service = db.query(Service).filter(
                Service.title == service_to_add["title"]
            ).first()
            if not matching_service:
                srv = Service(
                    title=service_to_add["title"],
                    description=service_to_add["description"]
                )
                db.add(srv)
                db.commit()
                print(f"Successfully seeded logistics listing: {service_to_add['title']}")
                
        # 4. Seed original Logistics projects showcase list
        available_projects = [
            {
                "title": "Express Highway Hauler",
                "category": "freight",
                "tag": "Freight",
                "description": "Cross-state machinery delivery completed with absolute precision.",
                "image_url": "https://images.unsplash.com/photo-1601584115197-04ecc0da31d7?q=80&w=600&auto=format&fit=crop"
            },
            {
                "title": "Fulfillment Depot",
                "category": "warehousing",
                "tag": "Warehousing",
                "description": "Fully automated barcode scanning and thermal stock management solutions.",
                "image_url": "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?q=80&w=600&auto=format&fit=crop"
            },
            {
                "title": "Safe Port Hub",
                "category": "shipping",
                "tag": "Shipping",
                "description": "Transoceanic shipping coordination covering complex custom lines.",
                "image_url": "https://images.unsplash.com/photo-1494412574643-ff11b0a5c1c3?q=80&w=600&auto=format&fit=crop"
            },
            {
                "title": "Inter-State Dispatch",
                "category": "distribution",
                "tag": "Distribution",
                "description": "Overland fleet scheduling ensuring 24-hour turnaround deadlines.",
                "image_url": "https://images.unsplash.com/photo-1508974239320-0a029497e820?q=80&w=600&auto=format&fit=crop"
            }
        ]
        for proj_to_add in available_projects:
            matching_project = db.query(Project).filter(
                Project.title == proj_to_add["title"]
            ).first()
            if not matching_project:
                proj = Project(
                    title=proj_to_add["title"],
                    category=proj_to_add["category"],
                    tag=proj_to_add["tag"],
                    description=proj_to_add["description"],
                    image_url=proj_to_add["image_url"]
                )
                db.add(proj)
                db.commit()
                print(f"Successfully seeded project showcase: {proj_to_add['title']}")
                
    except Exception as e:
        print(f"Seeding error: {e}")
    finally:
        db.close()

seed_initial_state()
