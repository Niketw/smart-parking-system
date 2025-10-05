from flask import Blueprint, request, Response
from twilio.twiml.messaging_response import MessagingResponse
from ..controllers.sms_controller import build_sms_response_text


sms_bp = Blueprint("sms", __name__)


@sms_bp.post("")
def incoming_sms():
    # Twilio will POST x-www-form-urlencoded with Body, From, To, etc.
    body = (request.form.get("Body") or "").strip()
    resp = MessagingResponse()
    resp.message(build_sms_response_text(body))
    xml = str(resp)
    return Response(xml, mimetype="application/xml")


