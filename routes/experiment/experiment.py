from flask import Blueprint, session, render_template, redirect, url_for

experiment_bp = Blueprint('experiment', __name__)

@experiment_bp.route("/experiment", methods=["GET"])
def experiment():
    session.clear()
    session["flow"] = ""

    from app import Project
    experiment = Project.query.filter_by(project_name="experiment").first()
    if not experiment or experiment.is_archived:
        return redirect(url_for("dispatcher"))

    return render_template(
        "index.html",
        bot="",
        phase=-1)
