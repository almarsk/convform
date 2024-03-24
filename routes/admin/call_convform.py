from flask import Blueprint, request, jsonify
from convform import convform

convform_bp = Blueprint('convform', __name__)

@convform_bp.route("/convform", methods=["POST"])
def call_convform():
    instruction = request.get_json()
    success = convform(instruction)
    return jsonify(success)
