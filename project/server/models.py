# project/server/models.py

"""
Models to add:

Comment
OntologySource
OntologyAnnotation
Publication
Person


"""

import datetime

from flask import current_app

import os

import pymodm
from pymodm import MongoModel, fields

from project.server import db, bcrypt


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, password, admin=False):
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, current_app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode('utf-8')
        self.registered_on = datetime.datetime.now()
        self.admin = admin

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User {0}>'.format(self.email)


class NMR_LitData(db.Model):
    """Database for literature nmr data points.
    """
    __tablename__ = 'nmr_lit_data'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    doi = db.Column(db.String(255), nullable=True)
    Al_concentration = db.Column(db.Numeric(), nullable=True)
    OH_concentration = db.Column(db.Numeric(), nullable=True)
    CI_concentration = db.Column(db.Numeric(), nullable=True)
    Al_ppm = db.Column(db.Numeric(), nullable=True)
    counter_ion = db.Column(db.String(255), nullable=True)
    Al_source = db.Column(db.String(255), nullable=True)


# ----------------------------------
# MongoDB Models for Metadata
# ----------------------------------

# class DemoModel(MongoModel):
    # name = fields.CharField()



# ----------------------------------
# Abstract Level
# ----------------------------------


class Ontology(MongoModel):
    name = fields.CharField()
    descriptor = fields.CharField()


class Quantitative(MongoModel):
    factor_name = fields.ReferenceField(Ontology)
    single_value = fields.FloatField()
    mult_values = fields.ListField()


class Qualitatives(MongoModel):
    factor_name = fields.ReferenceField(Ontology)
    single_value = fields.FloatField()
    multi_values = fields.ListField()


class Species(MongoModel):
    factor_name = fields.ReferenceField(Ontology)
    sub_species = fields.DictField()
    qualitators = fields.ReferenceField(Qualitatives)


# ----------------------------------
# Sample Level
# ----------------------------------


class MaterialSource(MongoModel):
    factor_name = fields.ReferenceField(Ontology)
    qual_properties = fields.ReferenceField(Ontology)
    quant_properties = fields.ReferenceField(Quantitative)


class Sample(MongoModel):
    name = fields.CharField()
    sources = fields.ListField()
    species = fields.ListField()


# ----------------------------------
# Protocol Level
# ----------------------------------


class Protocol(MongoModel):
    factor_name = fields.CharField()
    unit_measured = fields.ReferenceField(Ontology)
    instrument = fields.CharField()


# ----------------------------------
# Data Level
# ----------------------------------


class DataFile(MongoModel):
    data_file = fields.FileField()


# ----------------------------------
# Experiment Level
# ----------------------------------

class Experiment(MongoModel):
    name = fields.CharField()
    sample_list = fields.ListField()
    protocol = fields.ReferenceField(Protocol)
    data_set = fields.ReferenceField(DataFile)
