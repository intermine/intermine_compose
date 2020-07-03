from flask import Blueprint, jsonify, abort, request, make_response
from flask_login import login_required, current_user
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from http import HTTPStatus
from uuid import UUID, uuid4
import os

# did relative imports here (Make sure to change this during refactoring )
from ..models.mine import Mine, MineSchema, MineStateSchema, MineCheckNameSchema

mine_bp = Blueprint("mine", __name__, url_prefix='/api/v1/mine')

@mine_bp.route("/", methods=["GET", "DELETE"])
@login_required
def getMine():
    mine_id = request.args.get('mineId', default=None)
    # check if mineId query parameter is given
    if mine_id is None:
        # return early if fileId is not available
        abort(HTTPStatus.BAD_REQUEST, str("NO MINE_ID GIVEN"))
    
    # query mine from database
    try:
        mine = Mine.query.filter_by(id=mine_id, user_id=current_user.get_id()).one()
    except NoResultFound:
        abort(HTTPStatus.BAD_REQUEST, str("UNKNOWN MINEID"))
    except:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, str("FAILED TO QUERY MINE"))
    
    if request.method == "GET":
        # return mine info
        mine_schema_instance = MineSchema()
        return jsonify(mine_schema_instance.dump(mine).data)
    if request.method == "DELETE":
        try:
            db.session.delete(mine)
            db.session.commit()
        except:
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, str("FAILED TO DELETE MINE"))
        return "Mine successfully deleted"

@mine_bp.route("/all", methods=["GET"])
@login_required
def getMines():

    mine_schema_instance = MineSchema(many=True)
    # query mine from database
    try:
        mines = mine_schema_instance.dump(
            Mine.query.filter_by(user_id=current_user.get_id()).all()
        )
    except:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, str("FAILED TO QUERY MINES"))
    
    return jsonify(mines.data)

@mine_bp.route("/nameAvailability", methods=["POST"])
@login_required
def checkMineName():

    # validate user input
    mine_check_name_schema_instance = MineCheckNameSchema()
    errors = mine_check_name_schema_instance.validate(request.json)
    if errors:
        response = make_response(jsonify(errors), HTTPStatus.BAD_REQUEST)
        return response

    # load request data into mine_check_name_schema_instance
    # Note: we are re using the variable here!!
    mine_check_name_schema_instance = mine_check_name_schema_instance.load(request.json)
    
    # query db for mine with same name
    try:
        Mine.query.filtery_by(
            name=mine_check_name_schema_instance.data["mineName"]
        ).one()
    except NoResultFound:
        # return true if no mine is found with same name
        mine_check_name_schema_instance.data["isAvailable"] = "true"
        return jsonify(mine_check_name_schema_instance.data)
    
    # return false if a mine is found with same name
    mine_check_name_schema_instance.data["isAvailable"] = "false"
    return jsonify(mine_check_name_schema_instance.data)

@mine_bp.route("/state/", methods=["GET","POST"])
@login_required
def getOrSetMineState():
    mine_id = request.args.get('mineId', default=None)
    # check if mineId query parameter is given
    if mine_id is None:
        # return early if fileId is not available
        abort(HTTPStatus.BAD_REQUEST, str("NO MINE_ID GIVEN"))
    
    # query mine from database
    try:
        mine = Mine.query.filter_by(id=mine_id, user_id=current_user.get_id()).one()
    except NoResultFound:
        abort(HTTPStatus.BAD_REQUEST, str("UNKNOWN MINEID"))
    except:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, str("FAILED TO QUERY MINE"))
    
    mine_state_schema_instance = MineStateSchema()
    
    if request.method == "GET":
        # return mine info
        return jsonify(mine_state_schema_instance.dump(mine).data)
    if request.method == "POST":
        # validate user input
        errors = mine_state_schema_instance.validate(request.json)
        if errors:
            response = make_response(jsonify(errors), HTTPStatus.BAD_REQUEST)
            return response

        mine_state_schema_instance = mine_state_schema_instance.load(request.json)
        # load mine data into mine_state_schema_instance
        # Note: we are re using the variable here!!
        mine_schema_instance = MineSchema()
        mine_schema_instance = mine_schema_instance.dump(mine)
        mine_schema_instance.data["mineStatus"] = mine_state_schema_instance.data["mineStatus"]
        try:
            mine.update(mine_schema_instance.data)
            db.session.commit()
        except:
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, str("FAILED TO UPDATE MINE STATUS"))
        return jsonify(mine_state_schema_instance.data)