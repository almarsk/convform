from flask import Blueprint, session, request, jsonify
from database import db
import json

bot_bp = Blueprint('bot', __name__)

@bot_bp.route("/bot", methods=["POST"])
def bot():
    from app import app
    [user_speech, c_status_in, elapsed_time, run] = request.get_json()
    from convcore import reply, Flow
    cstatus_out = reply(user_speech, Flow(session["flow"] if not run else run), c_status_in)

    if not run:
        if cstatus_out.end:
            session["phase"] += 1

        from app import Reply

        reply = Reply(
            user_id=session["conversation_id"],
            reply=user_speech,
            reaction_ms=elapsed_time,
            cstatus=c_status_in,
            who="human")
        db.session.add(reply)

        reply = Reply(
            user_id=session["conversation_id"],
            reply=cstatus_out.say,
            reaction_ms=0, # todo
            cstatus=cstatus_out.__dict__,
            who="bot")

        db.session.add(reply)
        db.session.commit()

    return jsonify(cstatus_out.__dict__)
