from flask import Blueprint, request, current_app

from blueprints.extension.models import CommentExtension
from errors.base_errors import APIError
from routes import urls
from utils.response_json import make_json_response
from utils.base_utils import route_inject
from errors.general_errors import PermissionDenied
from utils.base_utils import verify_outer

bp_name = 'extension'

visit_api = [
    "{}.add_comment".format(bp_name),
    "{}.remove_comment".format(bp_name),
]
manage_api = [
    "{}.remove_batch_comments".format(bp_name),
    "{}.list_comment_groups".format(bp_name)
]

blueprint = Blueprint(bp_name, __name__)

route_inject(blueprint, urls)


@blueprint.before_app_first_request
def before_first_request():
    current_app.mongodb_database.register(CommentExtension)
    return


@blueprint.before_request
def before_request():
    if request.endpoint in visit_api:
        verify_outer()
    elif request.endpoint in mange_api:
        verify_jwt()
    return


@blueprint.errorhandler(APIError)
def comment_api_err(error):
    return make_json_response(error)
