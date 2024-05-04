import pprint
from flask import Blueprint, request, jsonify
from database import db
from datetime import datetime
import pprint

convos_bp = Blueprint('convos', __name__)

@convos_bp.route("/convos", methods=["POST"])
def convos():
    from app import db, Conversation, Reply, Flow
    try:
        flow, = request.get_json().values()

    except:
        return jsonify({}), 400



    conversations = [{
        "id": c.id,
        "nick": c.nick,
        "start": c.start_date.strftime("%Y-%m-%d %H:%M:%S.%f") if c.start_date else "",
        "end": c.end_date.strftime("%Y-%m-%d %H:%M:%S.%f") if c.end_date else "",
        "aborted": c.abort,
        "rating": c.rating,
        "comment": c.comment,
        "conversation": [{
            "id": r.id,
            "reply": r.reply,
            "date": r.date,
            "reaction_ms": r.reaction_ms,
            "cstatus": r.cstatus,
            "who": r.who
        } for r in Reply.query.filter_by(user_id=c.id)]
    } for c in Conversation.query.filter_by(flow=flow)]



    return jsonify({"success": True, "data": conversations}), 200
