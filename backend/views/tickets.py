from flask import Blueprint, request, jsonify
from ..controllers import tickets_controller as ctrl


tickets_bp = Blueprint("tickets", __name__)


@tickets_bp.post("")
def create_ticket():
    data = request.get_json(force=True, silent=True) or {}
    try:
        ticket = ctrl.create_ticket(data)
        return jsonify(ticket.to_dict()), 201
    except ValueError as e:
        msg = str(e)
        status = 409 if "exists" in msg else 400
        return jsonify({"error": msg}), status


@tickets_bp.get("")
def list_tickets():
    is_active = request.args.get("isActive")
    license_plate = request.args.get("licensePlate")
    ticket_number = request.args.get("ticketNumber")
    tickets = ctrl.list_tickets(
        is_active=(is_active.lower() == "true") if is_active is not None else None,
        license_plate=license_plate,
        ticket_number=ticket_number,
    )
    return jsonify([t.to_dict() for t in tickets])


@tickets_bp.get("/<int:ticket_id>")
def get_ticket(ticket_id: int):
    ticket = ctrl.get_ticket(ticket_id)
    return jsonify(ticket.to_dict())


@tickets_bp.patch("/<int:ticket_id>")
def update_ticket(ticket_id: int):
    data = request.get_json(force=True, silent=True) or {}
    ticket = ctrl.update_ticket(ticket_id, data)
    return jsonify(ticket.to_dict())


@tickets_bp.post("/<int:ticket_id>/checkout")
def checkout_ticket(ticket_id: int):
    try:
        ticket = ctrl.checkout_ticket(ticket_id)
        return jsonify(ticket.to_dict())
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@tickets_bp.get("/search")
def search_ticket():
    q = request.args.get("q", "")
    try:
        tickets = ctrl.search_tickets(q)
        return jsonify([t.to_dict() for t in tickets])
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


