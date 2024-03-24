from flask import Blueprint, request, jsonify
from database import db
from datetime import datetime

copy_flow_bp = Blueprint('copy_flow', __name__)

@copy_flow_bp.route("/copy_flow", methods=["POST"])
def copy_flow():
    from app import db, Flow, Project
    try:
        name, = request.get_json().values()
    except:
        return jsonify({}), 400


    source_flow = Flow.query.filter_by(flow_name=name).first()
    if source_flow:
        split = name.split("_")
        if len(split) > 1 and split[-1].isdigit():
            new_name = "_".join(split[0:-1])
        else:
            new_name = source_flow.flow_name

        index = 1
        while Flow.query.filter_by(flow_name=new_name).first():
            index += 1
            if len(split) > 1 and split[-1].isdigit():
                base = "_".join(split[0:-1])
            else:
                base = source_flow.flow_name
            new_name = f"{base}_{str(index)}"

        item = Flow(
            flow_name=new_name,
            flow=source_flow.flow,
            project_id=source_flow.project_id,
            is_archived = 1 if int(source_flow.project_id) == 2 else 0
        )
        db.session.add(item)
        db.session.commit()
        return jsonify({}), 200

    else:
        return jsonify({"success": False, "message": "there is a flow of that name already"})
