import os
import secrets
from pathlib import Path
from importlib import import_module
from datetime import datetime
import json
import cstatus
from bot_reply import reply

from flask import (
    Flask,
    abort,
    render_template,
    session,
    redirect,
    request,
    url_for,
    jsonify
)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import JSON

# –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– Configuration
app = Flask(__name__)
secret_key = os.environ.get("CHATBOT_SECRET_KEY", secrets.token_bytes(32))
db_path = Path(__file__).parent / "chatbot.db"
app.config.update(
    TEMPLATES_AUTO_RELOAD=True,
    SECRET_KEY=secret_key,
    SESSION_COOKIE_SAMESITE="Lax",
    SQLALCHEMY_DATABASE_URI=f"sqlite:///{db_path}",
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    REPLY_DELAY_MS=int(os.environ.get("CHATBOT_REPLY_DELAY_MS", 1600)),
)
db = SQLAlchemy(app)



# –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– Database


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nick = db.Column(db.Text, nullable=False)
    flow = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, default=None)
    abort = db.Column(db.Boolean, default=None)
    rating = db.Column(db.Integer, default=None)
    comment = db.Column(db.Text, default=None)


class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    reaction_ms = db.Column(db.Integer) # chatbot replies have a NULL reaction_ms
    cstatus = db.Column(JSON)


if not db_path.is_file():
    with app.app_context():
        db.create_all()

# –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– Handling Requests


# There's technically only one route, so as to prevent the user from
# easily navigating the interaction with the chatbot. The state of the
# app is instead held in session["page"], based on which the request is
# dispatched to an appropriate handler.
#
# The flow can be set via query parameters in the URL
# (?flow=...). Once set, it's stored in session["flow"]. Setting
# the flow clears the session, as it's taken as a signal of a new
# conversation starting. Trying to use the app without setting a
# flow shows an error.
@app.route("/fetch_string", methods=["GET"])
async def fetch_string():
    if "user_id" not in session:
        return jsonify({
            "error": "no access"
        })
    print("sesh user id:"+str(session["user_id"]))
    csi = cstatus.get_csi(str(session["user_id"]), session["user_reply"])
    cso = await reply(csi)
    print("cso.show():")
    print(cso.show())
    session.modified = True
    if cso is None:
        session["page"] = "outro"
        return redirect(url_for("dispatcher"))
    else:
        repl = Reply(user_id=session["user_id"], content=str(cso.bot_reply), cstatus=cstatus.to_json(cso))
        print(vars(repl))
        db.session.add(repl)
        db.session.commit()
        return jsonify({
            "fetched_string": cso.bot_reply
        })


@app.route("/", methods=("GET", "POST"))
def dispatcher():
    app.logger.info("flask: dispatcher")
    url_flow = request.args.get("flow") or None

    if url_flow is not None:
        # a flow was set via the URL's query string -> start a new conversation
        session.clear()
        if os.path.exists(f"convform/bots/{url_flow}.json"):
            session["flow"] = url_flow
            try:
                with open(f"convform/bots/{session['flow']}.json", "r") as file:
                    json.load(file)
            except ValueError:
                return render_template("json_issue.html", flow=session["flow"].capitalize()), 500
        else:
            session["page"] = "not_found"
            return render_template("not_found.html", flow=url_flow.capitalize()), 404
        return redirect(url_for("dispatcher"))
    elif session.get("flow") is None:
        # starting a conversation without setting a flow is forbidden -> 403 error
        session["page"] = "no_access"
        return render_template("no_access.html"), 403

    if request.args.get("abort"):
        session["page"] = "outro"
        session["abort"] = True
        return redirect(url_for("dispatcher"))

    page = session.setdefault("page", "intro")
    handler = globals().get(page)
    if handler is None:
        abort(404)
    return handler()


def not_found():
    return render_template("not_found.html", flow=session["flow"].capitalize()), 404


def intro():
    app.logger.info("flask: intro")
    if request.method == "GET":
        return render_template("intro.html", flow=session["flow"].capitalize())
    elif request.method == "POST":
        user = User(nick=request.form.get("nick"), flow=session["flow"])
        db.session.add(user)
        db.session.commit()
        # the user only has a valid ID after they've been committed to
        # the database
        session["user_id"] = user.id
        session["page"] = "chat"
        return redirect(url_for("dispatcher"))


def chat():
    app.logger.info("flask: chat")
    user = User.query.filter_by(id=session["user_id"]).first()
    session["user_reply"] = request.form.get("answer")
    if request.method == "POST":
        db.session.add(
            Reply(
                user_id=user.id,
                content=session["user_reply"],
                reaction_ms=request.form.get("reaction-ms"),
            )
        )
        db.session.commit()
    cState = session.setdefault("state", {"flow" : session["flow"], "user_id":session["user_id"]})  # conversation state

    return render_template(
        "chat.html", flow=session["flow"].capitalize()
    )


def outro():

    if request.method == "GET":
        return render_template("outro.html", aborted=session.get('abort', None))

    elif request.method == "POST":
        rating_verbal = request.form.get("ratingVerbal")
        rating_num = request.form.get("ratingNum") or 0

        user = User.query.filter_by(id=session["user_id"]).first()
        user.end_date = datetime.utcnow()
        user.abort = session.get("abort", False)
        user.rating = int(rating_num)
        user.comment = rating_verbal
        db.session.add(user)
        db.session.commit()

        session.clear()
        return render_template("thanks.html")


if __name__ == "__main__":
    app.run(debug=True)
