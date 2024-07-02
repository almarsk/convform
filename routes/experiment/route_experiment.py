from flask import Blueprint, redirect, url_for, request, session
from convproof.main import validate_flow
from database import db
import json

route_experiment_bp = Blueprint('route_experiment', __name__)

@route_experiment_bp.route("/route_experiment", methods=["GET"])
def route_experiment():
    from database import db
    from app import Project, Flow, Conversation

    username = request.args.get("username") or None
    user_conversations = Conversation.query.filter_by(nick=username).all()
    user_flows = set()
    for conversation in user_conversations:
        user_flows.add(conversation.flow)

    try:
        experiment = Project.query.filter_by(project_name="experiment").first()
        if not experiment or experiment.is_archived:
            return redirect(url_for("dispatcher"))
        experiment_id = experiment.id
        experimental_flows = Flow.query.filter_by(project_id=experiment_id).all()
        flows_usage: dict[str, int] = dict()
        for flow in experimental_flows:
            name = flow.flow_name

            if flow.flow_name not in user_flows and validate_flow(name)["success"]:
                convos = [convo for convo in Conversation.query.filter_by(flow=name).all()]
                flows_usage[name] = len(convos)
        bot_name: str = min(flows_usage, key=flows_usage.get)

        current_conversation = Conversation.query.filter_by(id=session["conversation_id"]).first()
        current_conversation.flow = bot_name
        db.session.add(current_conversation)
        db.session.commit()

        session["flow"] = bot_name
        url = url_for("dispatcher")

        return redirect(url)
    except:
        return redirect(url_for("dispatcher"))
