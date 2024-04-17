from flask import Blueprint, session, request, jsonify
from database import db
from datetime import datetime

login_bp = Blueprint('login', __name__)

@login_bp.route("/login", methods=["POST"])
def login():
    login = request.get_json()

    login_ok = True # todo actual auth

    return jsonify({"success": login_ok})
