# from flask import Blueprint, jsonify, make_response, abort, request
# from flask_login import login_required, current_user
# from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
# from http import HTTPStatus
# from uuid import UUID, uuid4
# import os

# # did relative imports here (Make sure to change this during refactoring )
# from ..models.mine import Mine, MineSchema, MineStateSchema, MineCheckNameSchema
# from ..models.build import Build, BuildStatusSchema, BuildTriggerSchema

# build_bp = Blueprint("build", __name__, url_prefix='/api/v1/build')

# @build_bp.route("/", methods=["POST"])
# @login_required
# def buildTrigger():
#     mine_id = request.args.get('mineId', default=None)
#     # check if mineId query parameter is given
#     if mine_id is None:
#         # return early if fileId is not available
#         abort(HTTPStatus.BAD_REQUEST, str("NO MINE_ID GIVEN"))

#     # query mine from database
#     try:
#         mine = Mine.query.filter_by(id=mine_id, user_id=current_user.get_id()).one()
#     except NoResultFound:
#         abort(HTTPStatus.BAD_REQUEST, str("UNKNOWN MINEID"))
#     except:
#         abort(HTTPStatus.INTERNAL_SERVER_ERROR, str("FAILED TO QUERY MINE"))

#     return jsonify({"mineId": mine.id})

# @build_bp.route("/status/", methods=["GET"])
# @login_required
# def getbuildStatus():
#     mine_id = request.args.get('mineId', default=None)
#     # check if mineId query parameter is given
#     if mine_id is None:
#         # return early if fileId is not available
#         abort(HTTPStatus.BAD_REQUEST, str("NO MINE_ID GIVEN"))

#     # query mine from database
#     try:
#         mine = Mine.query.filter_by(id=mine_id, user_id=current_user.get_id()).one()
#     except NoResultFound:
#         abort(HTTPStatus.BAD_REQUEST, str("UNKNOWN MINEID"))
#     except:
#         abort(HTTPStatus.INTERNAL_SERVER_ERROR, str("FAILED TO QUERY MINE"))

#     return jsonify(
#         {
#             "mineId": mine.id,
#             "buildStatus": "pending",
#             "errorDetails": ""
#         }
#     )
