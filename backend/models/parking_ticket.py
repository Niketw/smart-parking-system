from datetime import datetime
from typing import Optional

from . import db


class ParkingTicket(db.Model):
    __tablename__ = "parking_tickets"

    id = db.Column(db.Integer, primary_key=True)
    ticket_number = db.Column(db.String(32), unique=True, nullable=False, index=True)
    license_plate = db.Column(db.String(32), nullable=False, index=True)
    vehicle_make = db.Column(db.String(64), nullable=True)
    vehicle_model = db.Column(db.String(64), nullable=True)
    parking_spot = db.Column(db.String(16), nullable=False, index=True)
    check_in_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    check_out_time = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True, index=True)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "ticketNumber": self.ticket_number,
            "licensePlate": self.license_plate,
            "vehicleMake": self.vehicle_make,
            "vehicleModel": self.vehicle_model,
            "parkingSpot": self.parking_spot,
            "checkInTime": (self.check_in_time.isoformat() if self.check_in_time else None),
            "checkOutTime": (self.check_out_time.isoformat() if self.check_out_time else None),
            "isActive": self.is_active,
        }


