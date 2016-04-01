# coding=utf-8

from cavavin.models import Wine
from cavavin.security import is_logged_in
from flask import Blueprint, g, render_template

wines_bp = Blueprint('wines', __name__)


@wines_bp.route('', methods=['GET'])
@is_logged_in()
def list():
    wines = Wine.query.filter_by(user=g.user).all()
    return render_template('wines.html', wines=wines)


def render_new_wine_form(wine_data={}, errors={}):
    return render_template('new_wine.html',
                           wine_data=wine_data,
                           errors=errors)


@wines_bp.route('/new', methods=['GET'])
@is_logged_in()
def new():
    return render_new_wine_form()
