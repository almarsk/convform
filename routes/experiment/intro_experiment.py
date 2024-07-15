from flask import Blueprint, session, request, jsonify
from database import db

intro_experiment_bp = Blueprint('intro_experiment', __name__)

@intro_experiment_bp.route('/intro_experiment', methods=["POST"])
def intro_experiment():
    from app import Conversation
    nick = request.get_json()["nick"]
    convo = Conversation(nick=nick, flow=session["flow"])

    session["phase"] = 1
    session["experiment"] = True
    db.session.add(convo)
    db.session.commit()
    session["conversation_id"] = convo.id
    return jsonify({"nick": nick}), 200
