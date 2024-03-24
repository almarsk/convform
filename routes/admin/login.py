from flask import Blueprint, session, request, jsonify
from database import db
from datetime import datetime

login_bp = Blueprint('login', __name__)

@login_bp.route("/login", methods=["POST"])
def login():
    [nickname, password] = request.get_json()

    return jsonify({"success": nickname == "almarsk" and password == "Sl0nice!"})
