from flask import Blueprint, session, jsonify, request

start_bp = Blueprint('start', __name__)

@start_bp.route("/start", methods=["POST"])
def start():
    session["phase"] += 1
    return jsonify({}), 200
