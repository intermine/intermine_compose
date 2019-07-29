from flask import Blueprint, request, abort, jsonify, send_file
from flask_login import login_required, current_user
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from http import HTTPStatus
from uuid import UUID, uuid4
from werkzeug.utils import secure_filename
import pathlib
import os

# did relative imports here (Make sure to change this during refactoring )
from ..models.data import DataFile, DataFileRemoteUploadSchema, DataFileSchema, DataFileUploadSchema
from ..models.mine import Mine
from ..models import db

data_bp = Blueprint("data", __name__, url_prefix='/api/v1/data')

@data_bp.route("/files", methods=["GET"])
@login_required
def getDataFiles():
    # Initialize a data file schema instance 
    # (many is to true because we may have many data files for a single user)
    data_file_schema_instance = DataFileSchema(many=True)

    # Do database calls inside a try block to catch errors
    try:
        data_files = data_file_schema_instance.dump(
            DataFile.query.filter_by(user_id=current_user.get_id()).all()
        )
    except:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, str("FAILED TO QUERY DATA_FILES"))
    return jsonify(data_files.data)

@data_bp.route("/file/", methods=["GET", "DELETE"])
@login_required
def getOrDelDataFile():
    
    fileID = request.args.get('fileId', default=None)
    # check if fileID query parameter is given
    if fileID is None:
        # return early if fileId is not available
        abort(HTTPStatus.BAD_REQUEST, str("NO FILEID GIVEN"))

    # validate if the fileID is a valid uuidv4 string
    if not validate_uuid4(fileID):
        # return early if validation fails
        abort(HTTPStatus.BAD_REQUEST, str("BAD FILEID"))
    
    # check if the file info exists in the database
    try:
        data_file_info = DataFile.query.filter_by(
            fileId=fileID, user_id=current_user.get_id()
        ).one()
    except NoResultFound:
        abort(HTTPStatus.BAD_REQUEST, str("UNKNOWN FILEID"))
    except:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, str("FAILED TO QUERY DATA_FILE"))
    
    # construct path to file
    data_file_path = os.path.join(
        os.environ.get('IM_DATA_DIR'),
        current_user.get_id(),
        data_file_info.mine_id,
        "data",
        data_file_info.fileId
    )

    if request.method == "GET":
        # return data file
        return send_file(data_file_path)
    if request.method == "DELETE":
        # delete data file
        try:
            os.remove(data_file_path)
            db.session.delete(data_file_info)
            db.session.commit()
        except:
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, str("FAILED TO DELETE DATA_FILE"))
        return jsonify({"message":"File successfully deleted"})

@data_bp.route("/file/upload/remote", methods=["POST"])
@login_required
def remoteUploadDataFile():
    pass

@data_bp.route("/file/upload/", methods=["POST"])
@login_required
def uploadDataFile():
    
    # mine_id = request.args.get('mineId', default=None)
    # # check if mineId query parameter is given
    # if mine_id is None:
    #     # return early if fileId is not available
    #     abort(HTTPStatus.BAD_REQUEST, str("NO MINE_ID GIVEN"))
    
    # check if mine exist and belongs to user
    # try:
    #     mine_info = Mine.query.filter_by(id=mine_id, user_id=current_user.get_id()).one()
    # except NoResultFound:
    #     abort(HTTPStatus.BAD_REQUEST, str("UNKNOWN MINEID"))
    # except:
    #     abort(HTTPStatus.INTERNAL_SERVER_ERROR, str("FAILED TO QUERY MINE"))
    
    # check if data file is uploaded
    if not request.files:
        abort(HTTPStatus.BAD_REQUEST, str("DATA UPLOAD FAILED, TRY AGAIN"))
    
    data_file = request.files["dataFile"]
    
    # generate a uuid for data file
    data_file_uuid = uuid4()

    # construct path to save file
    data_file_path = os.path.join(
        os.environ.get('IM_DATA_DIR'),
        str(current_user.get_id()),
        "data"
    )

    # create dir structure if not already present
    pathlib.Path(data_file_path).mkdir(parents=True, exist_ok=True) 

    # save file
    data_file.save(
        os.path.join(data_file_path, str(data_file_uuid))
    )

    # create file info instance for database
    data_file_db_instance = DataFile(
        fileId=data_file_uuid,
        name=secure_filename(data_file.filename),
        user_id=current_user.get_id(),
    )

    # add file info to database
    try:
        db.session.add(data_file_db_instance)
        db.session.commit()
    except:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, str("FAILED TO ADD DATA_FILE INFO"))
    
    return str(data_file_uuid)








###########################################################
################## Helper functions #######################
###########################################################

def validate_uuid4(uuid_string):
    try:
        UUID(uuid_string, version=4)
    except ValueError:
        return False
    return True