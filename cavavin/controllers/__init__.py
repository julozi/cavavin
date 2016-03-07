# coding=utf-8

from flask import redirect, url_for


def register_all_blueprints(app):
    """ Register all blueprints
    """
    from .login import login_bp
    from .racks import racks_bp

    app.register_blueprint(login_bp, url_prefix='/login')
    app.register_blueprint(racks_bp, url_prefix='/racks')

    @app.route('/', methods=['GET'])
    def home():
        return redirect(url_for('racks.list'))
