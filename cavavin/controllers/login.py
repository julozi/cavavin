# coding=utf-8

import hashlib
from cavavin.models import User
from flask import Blueprint, flash, redirect, render_template, request, session, url_for

login_bp = Blueprint('login', __name__)


@login_bp.route('', methods=['GET'])
def form():
    if 'user' in session:
        return redirect(url_for('racks.list'))

    return render_template('login.html')


@login_bp.route('', methods=['POST'])
def login():

    email = request.form.get('email', None)
    password = request.form.get('password', u'')

    user = User.query.filter_by(email=email).filter_by(password=unicode(hashlib.md5(password).hexdigest())).first()
    if user is None:
        flash('Email ou mot de passe invalide')
        return redirect(url_for('.form'))

    session['user'] = user.to_dict()
    return redirect(url_for('racks.list'))
