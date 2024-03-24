from flask import Blueprint, request, jsonify
import sqlite3
import os
from convproof import validate_flow

list_bot_bp = Blueprint('list_bots', __name__)

@list_bot_bp.route("/list-bots", methods=["POST"])
def list_bots():
    from app import app, db, Flow, db_path
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Flow")
        flows = cursor.fetchall()
        flow_names = [[row[1], row[2], row[4], row[5]] for row in flows]
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"db issues: {e}")
        return jsonify([])

    files = [
        [name, validate_flow(name), project, date, archived]
        for [name, date, project, archived]
        in flow_names
    ]
    return jsonify(files)
