from flask import Blueprint, session, request, jsonify

abort_bp = Blueprint('abort', __name__)
is_aborted_bp = Blueprint('is_aborted', __name__)

@abort_bp.route("/abort", methods=["POST"])
def abort():
    session["abort"] = True
    session["phase"] += 1
    return jsonify({})

@abort_bp.route("/is_aborted", methods=["POST"])
def isAborted():
    return jsonify({"aborted": session["abort"] if "abort" in session else False})
