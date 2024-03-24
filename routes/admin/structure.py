from convcore import structure
from flask import Blueprint, jsonify

structure_bp = Blueprint('structure', __name__)

@structure_bp.route('/structure', methods=['POST'])
def get_structure():

    states_ordered, intent_ordered, flow_ordered = structure()

    return jsonify({
        "states": states_ordered,
        "intents": intent_ordered,
        "flow": flow_ordered
    })
