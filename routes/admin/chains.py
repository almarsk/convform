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

        return jsonify(registered_chains[item_type]), 200

    except Exception as e:
        return jsonify([]), 400
