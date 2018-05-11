# project/server/user/forms.py


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from flask_wtf.file import FileField
from wtforms import (IntegerField, RadioField, StringField, PasswordField,
    SelectField, DecimalField, FormField, FieldList)
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional


from project.server.ontologies import (
    ONTOLOGY_ANNOTATIONS,
    UNIT_FACTORS,
    FACTOR_FACTORS,
    DATA_TYPES,
)


class LoginForm(FlaskForm):
    email = StringField('Email Address', [DataRequired(), Email()])
    password = PasswordField('Password', [DataRequired()])


class RegisterForm(FlaskForm):
    email = StringField(
        'Email Address',
        validators=[
            DataRequired(),
            Email(message=None),
            Length(min=6, max=40)
        ]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        'Confirm password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )


class OntologySourceForm(FlaskForm):
    name = StringField('Name', [DataRequired()])
    description = StringField(
        'Description', [DataRequired()], widget=TextArea())
