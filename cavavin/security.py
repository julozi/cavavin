# coding=utf-8

from cavavin.models import User
from flask import current_app, flash, g, redirect, request, session, url_for
from functools import update_wrapper


def is_logged_in(roles=[]):
    def decorator(f):
        def wrapped_function(*args, **kwargs):

            if 'user' in session:
                g.user = User.query.filter_by(email=session['user']['email']).first()
                return f(*args, **kwargs)

            session.pop('previous_url', None)

            current_app.logger.debug(url_for('racks.list'))

            if not request.url.endswith(url_for('racks.list')):
                session['previous_url'] = request.url
                flash(u"Veuillez-vous connecter avant d'accéder à cette page", 'warning')

            return redirect(url_for('users.login_form'))

        return update_wrapper(wrapped_function, f)
    return decorator
