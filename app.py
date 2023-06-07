import os
import secrets
from pathlib import Path
from importlib import import_module
from datetime import datetime

from flask import (
    Flask,
    abort,
    render_template,
    session,
    redirect,
    request,
    url_for,
)
from flask_sqlalchemy import SQLAlchemy

# –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– Configuration
app = Flask(__name__)
secret_key = os.environ.get("CHATBOT_SECRET_KEY", secrets.token_bytes(32))
db_path = Path(__file__).parent / "chatbot.db"
app.config.update(
    TEMPLATES_AUTO_RELOAD=True,
    SECRET_KEY=secret_key,
    SESSION_COOKIE_HTTPONLY = False,
    SESSION_COOKIE_SAMESITE="None",
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
    # chatbot replies have a NULL reaction_ms
    reaction_ms = db.Column(db.Integer)


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
@app.route("/", methods=("GET", "POST"))
def dispatcher():
    url_flow = request.args.get("flow") or None
    # print(session)

    if url_flow is not None:
        # a flow was set via the URL's query string -> start a new conversation
        session.clear()
        session["flow"] = url_flow
        try:
            import_module("flows."+url_flow)
        except ImportError:
            session["page"] = "not_found"
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
    if request.method == "GET":
        return render_template("intro.html", flow=session["flow"].capitalize())
    elif request.method == "POST":
        user = User(nick=request.form.get("nick"), flow=session["flow"])  # nick isn't set up yet
        db.session.add(user)
        db.session.commit()
        # the user only has a valid ID after they've been committed to
        # the database
        session["user_id"] = user.id
        session["page"] = "chat"
        return redirect(url_for("dispatcher"))


def chat():
    user = User.query.filter_by(id=session["user_id"]).first()
    user_reply = request.form.get("answer")
    if request.method == "POST":
        db.session.add(
            Reply(
                user_id=user.id,
                content=user_reply,
                reaction_ms=request.form.get("reaction-ms"),
            )
        )
    cs = session.setdefault("cs", {})  # conversation state
    flow = import_module("flows."+session["flow"])
    bot_reply = flow.reply(user_reply, cs)
    session.modified = True
    if bot_reply is None:
        session["page"] = "outro"
        response = redirect(url_for("dispatcher"))
    else:
        db.session.add(Reply(user_id=user.id, content=str(bot_reply)))
        response = render_template(
            "chat.html", bot_reply=bot_reply, flow=flow.__name__.capitalize()
        )

    db.session.commit()
    return response


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
