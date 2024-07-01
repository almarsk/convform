from flask import Blueprint, session, render_template

experiment_bp = Blueprint('experiment', __name__)

@experiment_bp.route("/experiment", methods=["GET"])
def experiment():
    session.clear()
    session["flow"] = ""
    return render_template(
        "index.html",
        bot="",
        phase=-1)
