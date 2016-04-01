# coding=utf-8

from flask import redirect, url_for


def register_all_blueprints(app):
    """ Register all blueprints
    """
    from .countries import countries_bp
    from .racks import racks_bp
    from .users import users_bp
    from .wines import wines_bp

    app.register_blueprint(countries_bp, url_prefix='/countries')
    app.register_blueprint(racks_bp, url_prefix='/racks')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(wines_bp, url_prefix='/wines')

    @app.route('/', methods=['GET'])
    def home():
        return redirect(url_for('racks.list'))
