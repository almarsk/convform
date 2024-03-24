from flask import Blueprint, request, jsonify
from database import db
from datetime import datetime

export_flow_bp = Blueprint('export_flow', __name__)

@export_flow_bp.route("/export_flow", methods=["POST"])
def export_flow():
    from app import db, Flow, Project
    try:
        name, = request.get_json().values()
    except:
        return jsonify({}), 400

    source_flow = Flow.query.filter_by(flow_name=name).first()
    if not source_flow:
        return jsonify({"success": False, "message": "there is no such flow"})

    return jsonify({"success": True, "flow": source_flow.flow}), 200
