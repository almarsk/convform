from flask import Blueprint, session, request, jsonify
from database import db

intro_bp = Blueprint('intro', __name__)

@intro_bp.route('/intro', methods=["POST"])
def intro():
    from app import Conversation
    convo = Conversation(nick=request.get_json()["nick"], flow=session["flow"])
    session["phase"] = 1
    db.session.add(convo)
    db.session.commit()
    session["conversation_id"] = convo.id
    return jsonify({}), 200
