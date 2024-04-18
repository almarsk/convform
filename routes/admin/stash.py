from flask import Blueprint, request, jsonify, request
import os
from convproof import validate_flow

stash_bp = Blueprint('stash', __name__)

@stash_bp.route("/stash", methods=["POST"])
def stash():
    from app import db, Flow, Project

    flows_to_delete = Flow.query.filter_by(is_archived=True).all()
    projects_to_delete = Project.query.filter_by(is_archived=True).all()
    archived_project_ids = [project.id for project in projects_to_delete]
    flows_in_projects_to_delete = Flow.query.filter(Flow.project_id.in_(archived_project_ids)).all()

    for group in [flows_to_delete, projects_to_delete, flows_in_projects_to_delete]:
        for row in group:
            db.session.delete(row)


    # Commit the transaction
    db.session.commit()

    return jsonify({"success": True, "message": "stashed archived"})
