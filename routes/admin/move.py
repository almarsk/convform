from flask import Blueprint, session, request, jsonify
from database import db
from datetime import datetime

move_bp = Blueprint('move', __name__)

@move_bp.route("/move", methods=["POST"])
def move():
    from app import Flow, Project, db
    item_type, name, destination = request.get_json().values()

    if item_type.strip() == "project":
        project = Project.query.filter_by(project_name=name).first()
        if project.id in [1,2] :
            return {"success": False, "message": "workspace and archived cant be moved"}
        # archived projects are found in project id 2
        project.is_archived = 1 if int(destination) == 2 else 0

        db.session.add(project)
        db.session.commit()

    elif item_type == "flow":
        flow = Flow.query.filter_by(flow_name=name).first()

        if destination is not None:
            flow.project_id = destination
        flow.is_archived = 1 if int(destination) == 2 else 0

        db.session.add(flow)
        db.session.commit()

    return jsonify({"success": True, "message": f"{item_type} {name} moved"})
