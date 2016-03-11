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
