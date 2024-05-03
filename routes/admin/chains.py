from flask import Blueprint, request, jsonify
import sqlite3
import os
from convproof import validate_flow
from registered_chains import registered_chains

chains_bp = Blueprint('chains', __name__)

@chains_bp.route("/chains", methods=["POST"])
def chains():
    try:
        item_type, = request.get_json()

        if item_type == "intent":
            return jsonify([]), 200
        else:
            return jsonify(registered_chains), 200

    except Exception as e:
        return jsonify([]), 400
