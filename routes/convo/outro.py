from flask import Blueprint, session, request, jsonify
from database import db
from datetime import datetime

outro_bp = Blueprint('outro', __name__)

@outro_bp.route("/outro", methods=["POST"])
def outro():
    from app import Conversation
    [grade, user_annotation] = request.get_json()
    convo = Conversation.query.filter_by(id=session["conversation_id"]).first()
    convo.end_date = datetime.utcnow()
    convo.abort = session.get("abort", False)
    convo.rating = int(grade)
    convo.comment = ""
    convo.user_annotation = user_annotation
    db.session.add(convo)
    db.session.commit()

    session["phase"] = 4
    return jsonify({})
