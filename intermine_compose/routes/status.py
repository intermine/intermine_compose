from flask import Blueprint

status_bp = Blueprint("status", __name__, url_prefix='/api/v1/status')

@status_bp.route("/", methods=["GET"])
def status():
    return "OK"