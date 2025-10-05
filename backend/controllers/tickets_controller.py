from datetime import datetime
from typing import List, Optional

from sqlalchemy import or_

from ..models import db
from ..models.parking_ticket import ParkingTicket


def create_ticket(data: dict) -> ParkingTicket:
    required_fields = ["ticketNumber", "licensePlate", "parkingSpot"]
    missing = [f for f in required_fields if not data.get(f)]
    if missing:
        raise ValueError(f"Missing fields: {', '.join(missing)}")

    if ParkingTicket.query.filter_by(ticket_number=data["ticketNumber"]).first():
        raise ValueError("Ticket number already exists")

    ticket = ParkingTicket(
        ticket_number=str(data["ticketNumber"]).strip(),
        license_plate=str(data["licensePlate"]).strip().upper(),
        vehicle_make=(data.get("vehicleMake") or None),
        vehicle_model=(data.get("vehicleModel") or None),
        parking_spot=str(data["parkingSpot"]).strip().upper(),
    )
    db.session.add(ticket)
    db.session.commit()
    return ticket


def list_tickets(is_active: Optional[bool] = None, license_plate: Optional[str] = None, ticket_number: Optional[str] = None) -> List[ParkingTicket]:
    query = ParkingTicket.query
    if is_active is not None:
        query = query.filter(ParkingTicket.is_active == is_active)
    if license_plate:
        query = query.filter(ParkingTicket.license_plate.ilike(f"%{license_plate}%"))
    if ticket_number:
        query = query.filter(ParkingTicket.ticket_number.ilike(f"%{ticket_number}%"))
    return query.order_by(ParkingTicket.check_in_time.desc()).all()


def get_ticket(ticket_id: int) -> ParkingTicket:
    return ParkingTicket.query.get_or_404(ticket_id)


def update_ticket(ticket_id: int, data: dict) -> ParkingTicket:
    ticket = ParkingTicket.query.get_or_404(ticket_id)
    if "licensePlate" in data and data["licensePlate"] is not None:
        ticket.license_plate = str(data["licensePlate"]).strip().upper()
    if "vehicleMake" in data:
        ticket.vehicle_make = data.get("vehicleMake") or None
    if "vehicleModel" in data:
        ticket.vehicle_model = data.get("vehicleModel") or None
    if "parkingSpot" in data and data["parkingSpot"] is not None:
        ticket.parking_spot = str(data["parkingSpot"]).strip().upper()
    db.session.commit()
    return ticket


def checkout_ticket(ticket_id: int) -> ParkingTicket:
    ticket = ParkingTicket.query.get_or_404(ticket_id)
    if not ticket.is_active:
        raise ValueError("Ticket already checked out")
    ticket.is_active = False
    ticket.check_out_time = datetime.utcnow()
    db.session.commit()
    return ticket


def search_tickets(q: str) -> List[ParkingTicket]:
    q = (q or "").strip()
    if not q:
        raise ValueError("Query parameter q is required")
    return (
        ParkingTicket.query.filter(
            or_(
                ParkingTicket.ticket_number.ilike(f"%{q}%"),
                ParkingTicket.license_plate.ilike(f"%{q}%"),
                ParkingTicket.parking_spot.ilike(f"%{q}%"),
            )
        )
        .order_by(ParkingTicket.check_in_time.desc())
        .all()
    )


