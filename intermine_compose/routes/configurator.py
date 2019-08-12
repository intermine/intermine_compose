from flask import Blueprint, request, Response, abort
from requests import request as rq
from flask_login import login_required, current_user
import os
from http import HTTPStatus

# did relative imports here (Make sure to change this during refactoring )
from ..utils import custom_logger

configurator_bp = Blueprint("configurator", __name__, url_prefix='/api/v1/configurator')


@configurator_bp.route('/', defaults={'path': ''}, methods=["GET", "POST", "DELETE"])
@configurator_bp.route('/<path:path>', methods=["GET", "POST", "DELETE"])
@login_required
def proxy(path):
    args = request.args.to_dict(flat=False)
    args["userId"] = current_user.get_id()

    try:
        resp = rq(
        method=request.method,
        # url=request.url.replace(request.host_url, 'new-domain.com'),
        url=f'{os.environ.get("CONFIGURATOR_URL")}{path}',
        params=args,
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data(),
        # cookies=request.cookies,
        allow_redirects=False
        )
    except:
        custom_logger.handle.error("FAILED TO REACH CONFIGURATOR")
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, str("FAILED TO REACH CONFIGURATOR"))
    
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers] 
    response = Response(resp.content, resp.status_code, headers)
    return response
