# project/server/user/views.py


from flask import render_template, Blueprint, url_for, \
    redirect, flash, request
from flask_login import login_user, logout_user, login_required
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from bokeh.embed import server_document
import pandas as pd
import redis
import os

from wtforms import StringField
from wtforms.validators import DataRequired

from project.server import bcrypt, db, BOKEH_PORTS
from project.server.models import User, NMR_LitData
from project.server.user.forms import LoginForm, RegisterForm


user_blueprint = Blueprint('user', __name__,)


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()

        login_user(user)

        flash('Thank you for registering.', 'success')
        return redirect(url_for("user.members"))

    return render_template('user/register.html', form=form)


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(
                user.password, request.form['password']):
            login_user(user)
            flash('You are logged in. Welcome!', 'success')
            return redirect(url_for('user.members'))
        else:
            flash('Invalid email and/or password.', 'danger')
            return render_template('user/login.html', form=form)
    return render_template('user/login.html', title='Please Login', form=form)


@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were logged out. Bye!', 'success')
    return redirect(url_for('main.home'))


@user_blueprint.route('/members')
@login_required
def members():
    return render_template('user/members.html')


@user_blueprint.route('/success')
@login_required
def success():
    return render_template('user/success.html')


class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    csv = FileField(validators=[FileRequired()])


@user_blueprint.route('/nmr_lit_submit', methods=('GET', 'POST'))
@login_required
def nmr_lit_submit():
    form = MyForm()
    if form.validate_on_submit():
        nmr_form = NMR_LitData()
        form.populate_obj(nmr_form)
        db.session.add(nmr_form)
        db.session.commit()

        return redirect('/success')
    return render_template('user/nmr_lit_submit.html', form=form)


def create_data():
    """Creates sample data."""
    db.drop_all()
    db.create_all()
    # Read from some local cvs.
    base_path = "project/tests/demodata/"
    demo_lit_csvs = {
        "sipos_2006_talanta_fig_2.csv": {
            "counter_ion": "Na+",
            "doi": "10.1016/j.talanta.2006.02.008"
        }
    }

    # Get the sql column names.
    sql_col_names = {c for c in NMR_LitData.__table__.columns}

    # Read their associated metadata json files.
    # Create the entries in the appropriate databases.
    # Al_concentration,OH_concentration,Al_ppm
    for path, prop_dict in demo_lit_csvs.items():
        df = pd.read_csv(base_path + path)

        # Get the column names.
        col_names = set(df)

        # Get the matching columns.
        matching_col_names = col_names.intersection(sql_col_names)

        # Get the matching keys from the prop dict.
        match_prop_dict = sql_col_names.intersection(prop_dict.keys())

        # Iterate through a zip of the matched values, and
        # populate them.
        for idx, row in df.iterrows():

            # Create a dictionary of the matching names: values.
            csv_vals = {c: row[c] for c in matching_col_names}
            prop_vals = {m: prop_dict[m] for m in match_prop_dict}

            nmr_entry = NMR_LitData(
                **csv_vals,
                **prop_vals
            )
            db.session.add(nmr_entry)
    db.session.commit()


@user_blueprint.route('/demo/', methods=['GET'])
# @login_required
def bokeh_demo():
    # Generate the demo data.
    create_data()

    # Pull all nmr data.
    my_data = pd.read_sql('nmr_lit_data', db)
    print(my_data)
    # Write this to redis with a hash.
    my_hash = "?hash=T35TH45H"
    rd = redis.from_url(os.environ.get("REDIS_URL"))

    # Save the data to the redis server with the hash as a key.
    rd.set(my_hash, my_data)

    url = "https://secret-cove-20095.herokuapp.com/app"

    script = server_document(url=url + my_hash)
    return render_template('user/bokeh_demo.html', script=script)
