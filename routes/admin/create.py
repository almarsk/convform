from flask import Blueprint, request, jsonify
from database import db
from datetime import datetime

create_bp = Blueprint('create', __name__)

@create_bp.route("/create", methods=["POST"])
def create():
    from app import db, Flow, Project
    try:
        item_type, name, destination = request.get_json().values()
    except:
        return jsonify({}), 400

    if item_type == "flow":
        if Flow.query.filter_by(flow_name=name).first():
            return jsonify({"success": False, "message": "there is a flow of that name already"})

        item = Flow(
            flow_name=name,
            flow=default_item(),
            project_id=destination,
            is_archived = 1 if int(destination) == 2 else 0
        )
        db.session.add(item)
        db.session.commit()

    elif item_type == "project":
        if Project.query.filter_by(project_name=name).first():
            return jsonify({"success": False, "message": "there is a flow of that name already"})
        item = Project(project_name=name)
        db.session.add(item)
        db.session.commit()

    return jsonify({}), 200


def default_item():
    from convcore import Flow
    return Flow("", structure=True).__dict__
