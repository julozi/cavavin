# coding=utf-8

from flask import Blueprint


racks_bp = Blueprint('racks', __name__)


@racks_bp.route('', methods=['GET'])
def list():
    return "racks list"
