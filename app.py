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
from sqlalchemy import JSON

import os
import secrets
from pathlib import Path
from datetime import datetime
import json

from convproof import validate_flow
from convcore import reply
from convform import convform

app = Flask(__name__, static_url_path='/assets', static_folder='assets')

secret_key = os.environ.get("CHATBOT_SECRET_KEY", secrets.token_bytes(32))
db_path = Path(__file__).parent / "chatbot.db"
app.config.update(
    TEMPLATES_AUTO_RELOAD=True,
    SECRET_KEY=secret_key,
    SESSION_COOKIE_SAMESITE="Lax",
    SQLALCHEMY_DATABASE_URI=f"sqlite:///{db_path}",
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    BOTS_PATH="bots"
)

from database import db
db.init_app(app)


# –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– Database


class Conversation(db.Model):
    __tablename__ = "conversation"
    id = db.Column(db.Integer, primary_key=True)
    nick = db.Column(db.Text, nullable=False)
    flow = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, default=None)
    abort = db.Column(db.Boolean, default=None)
    rating = db.Column(db.Integer, default=None)
    comment = db.Column(db.Text, default=None)
    __table_args__ = {'extend_existing': True}


class Reply(db.Model):
    __tablename__ = "reply"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("conversation.id"), nullable=False)
    reply = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    reaction_ms = db.Column(db.Integer) # chatbot replies have a NULL reaction_ms
    cstatus = db.Column(JSON)
    who = db.Column(db.Text, nullable=False)
    __table_args__ = {'extend_existing': True}

class Flow(db.Model):
    __tablename__ = "flow"
    id = db.Column(db.Integer, primary_key=True)
    flow_name = db.Column(db.Text, nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False, default=1)
    flow = db.Column(JSON)
    created_on = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    is_archived = db.Column(db.Integer, default=False)
    __table_args__ = {'extend_existing': True}


class Project(db.Model):
    __tablename__ = "project"
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.Text, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_archived = db.Column(db.Integer, nullable=False, default=False)
    default = db.Column(db.Integer, nullable=False, default=False)
    __table_args__ = {'extend_existing': True}


if not db_path.is_file():
    with app.app_context():
        db.create_all()

        db.session.add(Project(project_name="workspace", default=True))
        db.session.add(Project(project_name="archived", default=True))
        db.session.commit()


# –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– Handling Requests

@app.route('/', defaults={'path': ''}, methods=("GET", "POST"))
@app.route('/<path:path>')
def dispatcher(path):
    if path:
        session.clear()

    flow = request.args.get("flow") or None

    if flow is not None:
        session.clear()
        session["flow"] = flow
        session["phase"] = 0
        return redirect(url_for("dispatcher"))

    success, message = validate_flow(session["flow"] if "flow" in session else "").values()

    if "flow" not in session or not success:
        session["flow"] = ""
        session["phase"] = 0

    return render_template(
        "index.html",
        bot=session["flow"] if "flow" in session else "",
        phase=session["phase"] if "phase" in session else 0)


blueprint_paths = [
    "intro.intro_bp",
    "start.start_bp",
    "bot.bot_bp",
    "abort.abort_bp",
    "abort.is_aborted_bp",
    "outro.outro_bp",
    "admin.call_convform.convform_bp",
    "admin.list_bots.list_bot_bp",
    "admin.create.create_bp",
    "admin.list_projects.list_projects_bp",
    "admin.proof.proof_bp",
    "admin.login.login_bp",
    "admin.move.move_bp",
    "admin.copy.copy_flow_bp",
    "admin.export.export_flow_bp",
    "admin.rename.rename_bp",
    "admin.structure.structure_bp",
    "admin.stash.stash_bp"
]

for path in blueprint_paths:
    module_name, blueprint_name = path.rsplit('.', 1)
    module = __import__(f"routes.{module_name}", fromlist=[blueprint_name])
    blueprint = getattr(module, blueprint_name)
    app.register_blueprint(blueprint)

if __name__ == "__main__":
    app.run(debug=True)
