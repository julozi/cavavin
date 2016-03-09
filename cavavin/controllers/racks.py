# coding=utf-8

from flask import Blueprint
from cavavin.security import is_logged_in


racks_bp = Blueprint('racks', __name__)


@racks_bp.route('', methods=['GET'])
@is_logged_in()
def list():
    return "racks list"
