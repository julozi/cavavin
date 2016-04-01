# coding=utf-8

import json
from cavavin.models import Country, Region
from flask import Blueprint, make_response

countries_bp = Blueprint('countries', __name__)


@countries_bp.route('', methods=['GET'])
def get_all_countries():
    response = make_response(json.dumps([country.to_dict() for country in Country.query.all()]))
    response.status_code = 200
    response.mimetype = 'application/json'
    return response


@countries_bp.route('/<int:country_id>/regions', methods=['GET'])
def get_regions_in_country(country_id):
    response = make_response(json.dumps([region.to_dict() for region in Region.query.filter_by(country_id=country_id).all()]))
    response.status_code = 200
    response.mimetype = 'application/json'
    return response
