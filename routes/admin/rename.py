from flask import Blueprint, request, jsonify
from database import db
from datetime import datetime

rename_bp = Blueprint('rename', __name__)

@rename_bp.route("/rename", methods=["POST"])
def rename():
    from app import db, Flow, Project
    try:
        name, new_name = request.get_json().values()
    except:
        return jsonify(), 400

    # print(name, new_name)

    if Flow.query.filter_by(flow_name=new_name).first():
        return jsonify({"success": False, "message": "there is a flow of that name already"})

    item = Flow.query.filter_by(flow_name=name).first()
    if item:
        item.flow_name = new_name

        db.session.add(item)
        db.session.commit()

        return jsonify({"success": True, "message": f"flow {name} renamed to {new_name}"}), 200
    else:
        return jsonify({"success": False, "message": "non existent flow"}), 400
