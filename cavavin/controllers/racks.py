# coding=utf-8

from cavavin.app import db
from cavavin.models import Rack
from cavavin.security import is_logged_in
from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from voluptuous import MultipleInvalid

racks_bp = Blueprint('racks', __name__)


@racks_bp.route('', methods=['GET'])
@is_logged_in()
def list():
    racks = Rack.query.filter_by(user=g.user).all()
    return render_template('racks.html', racks=racks)


def render_new_rack_form(rack_data={}, errors={}):
    return render_template('new_rack.html',
                           rack_data=rack_data,
                           errors=errors)


@racks_bp.route('/new', methods=['GET'])
@is_logged_in()
def new():
    return render_new_rack_form()


@racks_bp.route('', methods=['POST'])
@is_logged_in()
def add():
    try:
        rack = Rack.from_dict(request.form)
    except MultipleInvalid as multiple_invalid:
        errors = {}
        for error in multiple_invalid.errors:
            if error.path[0] in errors:
                errors[error.path[0]].append(error.msg)
            else:
                errors[error.path[0]] = [error.msg]

        flash(u"Impossible d'enregister ce casier<br/>Veuillez corriger les erreurs ci-dessous", "danger")
        return render_new_rack_form(request.form, errors)

    rack.user = g.user
    try:
        db.session.add(rack)
        db.session.commit()
    except:
        flash(u"""Une erreur innatendue s'est produite lors de l'enregistrement du casier.<br/>
                  Si le problème persiste, merci d'envoyer un mail à julien.seiler@gmail.com""",
              "danger")
        return render_new_rack_form(request.form)

    flash(u"Le casier %s a été enregistré avec succès" % rack.name, "success")
    return redirect(url_for("racks.list"))
