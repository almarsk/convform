from flask import Blueprint, request, jsonify, request
import os
from convproof import validate_flow

stash_bp = Blueprint('stash', __name__)

@stash_bp.route("/stash", methods=["POST"])
def stash():
    from app import db, Flow, Project

    flows_to_delete = Flow.query.filter_by(is_archived=True).all()
    projects_to_delete = Project.query.filter_by(is_archived=True).all()

    for row in flows_to_delete:
        db.session.delete(row)
    for row in projects_to_delete:
        db.session.delete(row)

    # Commit the transaction
    db.session.commit()

    return jsonify({"success": True, "message": "stashed archived"})
