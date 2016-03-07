# coding=utf-8

from cavavin.app import db

__all__ = ['User', 'Wine', 'Bottle', 'Country', 'Region', 'Rack']


class User(db.Model):
    """ Utilisateur """

    __tablename__ = u'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.Unicode, unique=True, nullable=False)
    firstname = db.Column(db.Unicode, nullable=False)
    lastname = db.Column(db.Unicode, nullable=False)
    password = db.Column(db.Unicode, nullable=False)

    def to_dict(self):

        return {
            u'id': self.id,
            u'email': self.email,
            u'firstname': self.firstname,
            u'lastname': self.lastname
        }


class Wine(db.Model):
    """ Vin """

    __tablename__ = u'wine'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Unicode, nullable=False)
    cuvee = db.Column(db.Unicode, nullable=True)
    vintage = db.Column(db.Integer, nullable=True)  # millesime
    category = db.Column(db.Unicode, nullable=False)
    type = db.Column(db.Unicode, nullable=False)

    country_id = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False)
    country = db.relationship('Country')

    region_id = db.Column(db.Integer, db.ForeignKey('region.id'), nullable=True)
    region = db.relationship('Region')

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User')


class Bottle(db.Model):
    """ Bouteille """

    __tablename__ = u'bottle'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    entrance_date = db.Column(db.Date, nullable=False)
    exit_date = db.Column(db.Date, nullable=True)
    size = db.Column(db.Unicode, nullable=False)
    purchase_location = db.Column(db.Unicode, nullable=True)
    price = db.Column(db.Float, nullable=True)
    row = db.Column(db.Integer, nullable=True)
    column = db.Column(db.Integer, nullable=True)

    wine_id = db.Column(db.Integer, db.ForeignKey('wine.id'), nullable=False)
    wine = db.relationship('Wine')

    rack_id = db.Column(db.Integer, db.ForeignKey('rack.id'), nullable=True)
    rack = db.relationship('Rack')


class Country(db.Model):
    """ Pays """

    __tablename__ = u'country'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Unicode, nullable=False)


class Region(db.Model):

    __tablename__ = u'region'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Unicode, nullable=False)

    country_id = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False)
    country = db.relationship('Country')


class Rack(db.Model):
    """ Casier """

    __tablename__ = u'rack'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Unicode, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    width = db.Column(db.Integer, nullable=False)
