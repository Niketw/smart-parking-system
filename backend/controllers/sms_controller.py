from sqlalchemy import or_

from ..models.parking_ticket import ParkingTicket


def build_sms_response_text(body_text: str) -> str:
  query = (body_text or "").strip()
  if not query:
    return "Smart Parking: Send your ticket number or license plate to find your spot."

  ticket = (
    ParkingTicket.query.filter(ParkingTicket.is_active.is_(True))
    .filter(
      or_(
        ParkingTicket.ticket_number.ilike(f"%{query}%"),
        ParkingTicket.license_plate.ilike(f"%{query}%"),
      )
    )
    .order_by(ParkingTicket.check_in_time.desc())
    .first()
  )

  if not ticket:
    return "No active ticket found for that query. Check your ticket number or plate."

  return (
    f"Ticket {ticket.ticket_number} – Plate {ticket.license_plate} – Spot {ticket.parking_spot}."
    " Reply STOP to opt-out."
  )


