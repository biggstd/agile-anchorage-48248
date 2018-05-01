# project/server/user/forms.py


from flask_wtf import FlaskForm
<<<<<<< Updated upstream
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from flask_wtf.file import FileField
=======
from wtforms import IntegerField, RadioField, StringField, PasswordField, SelectField, DecimalField, FormField, FieldList
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional


from project.server.ontologies import (
    ONTOLOGY_ANNOTATIONS,
    UNIT_FACTORS,
    FACTOR_FACTORS,
    DATA_TYPES,
)
>>>>>>> Stashed changes


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


class OntologyAnnotationForm(FlaskForm):
    term = StringField('Term', validators=[Optional()])
    options = [(o.get('type'), o.get('short_display')) for o in ONTOLOGY_ANNOTATIONS]
    annotation = SelectField(label='Ontology', choices=options,
                             validators=[Optional()])


class StudyUnitFactorForm(FlaskForm):
    options = [
        (o.get('type'), o.get('short_display')) for o in UNIT_FACTORS]
    factor_type = SelectField(
        'Factor', choices=options, validators=[Optional()])
    factor_value = DecimalField('Value')


class CombinedFactorForm(FlaskForm):
    decimal_factors = FieldList(FormField(StudyUnitFactorForm), min_entries=1)


class NMRUploadForm(FlaskForm):
    """Form for user upload of NMR data."""
    choices = [(o.get('type'), o.get('short_display')) for o in DATA_TYPES]
    data_type = RadioField('Data Type', choices=choices)
    decimal_factors = IntegerField('Numerical Factors')
    categorical_factors = IntegerField('Categorical Factors')
