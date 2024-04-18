from flask import Blueprint, session, request, jsonify
from database import db

instructions_bp = Blueprint('instructions', __name__)

@instructions_bp.route('/instructions', methods=["POST"])
def instructions():
    from app import Flow
    try:
        flow, = request.get_json().values()
    except:
        return jsonify({"success": False}), 400
    convo = Flow.query.filter_by(flow_name=flow).first()

    if hasattr(Flow, 'flow') and "instructions" in convo.flow and convo.flow["instructions"]:
        user_instructions = convo.flow["instructions"]
        return jsonify({"success": True, "message": user_instructions}), 200
    else:
        return jsonify({"success": False}), 400
