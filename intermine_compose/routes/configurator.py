from flask import Blueprint, request, Response
from requests import request as rq
from flask_login import login_required, current_user
import os

configurator_bp = Blueprint("configurator", __name__, url_prefix='/api/v1/configurator')


@configurator_bp.route('/', defaults={'path': ''})
@configurator_bp.route('/<path:path>')
@login_required
def proxy(path):
    request.args["userId"] = current_user.get_id()
    resp = rq(
        method=request.method,
        # url=request.url.replace(request.host_url, 'new-domain.com'),
        url=f'{os.environ.get("CONFIGURATOR_URL")}{path}',
        params=request.args,
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data(),
        # cookies=request.cookies,
        allow_redirects=False
    )
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers] 
    response = Response(resp.content, resp.status_code, headers)
    return response
