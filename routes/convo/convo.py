from flask import Blueprint, session, request, jsonify
from database import db

#unused
mock_convo = {
    "convo": [
        {
            "who": "bot",
            "text": "ahojky",
            "checked": False,
            "comment": "",
        },
        {
            "who": "human",
            "text": "čau",
            "checked": False,
            "comment": "",
        },
        {
            "who": "bot",
            "text": "jak se máš",
            "checked": False,
            "comment": "",
        },
        {
            "who": "human",
            "text": "blbě",
            "checked": False,
            "comment": "",
        },
        {
            "who": "bot",
            "text": "nojoo",
            "checked": False,
            "comment": "",
        },
    ]
}


convo_bp = Blueprint('convo', __name__)

@convo_bp.route("/convo", methods=["POST"])
def convo():
    from app import Reply
    convo_raw = Reply.query.filter_by(user_id=session["conversation_id"])
    convo = {
        "convo": [{"who": reply.who, "text": reply.reply, "checked": False, "comment": ""} for reply in convo_raw if reply.reply]
    }
    return jsonify(convo)
