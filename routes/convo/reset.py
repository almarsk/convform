from flask import Blueprint, session, jsonify, request

reset_bp = Blueprint('reset', __name__)

@reset_bp.route("/reset", methods=["POST"])
def reset():
    session.pop("flow", None)
    return jsonify({}), 200
