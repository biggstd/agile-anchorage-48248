# project/server/user/views.py


from flask import render_template, Blueprint, url_for, \
    redirect, flash, request
from flask_login import login_user, logout_user, login_required
# from flask_wtf import FlaskForm
# from flask_wtf.file import FileField, FileRequired
# import pandas as pd
import redis
# import os

# from wtforms import StringField
# from wtforms.validators import DataRequired
# from werkzeug.utils import secure_filename

from project.server import bcrypt, db, BOKEH_APP_URL
from project.server.models import User
from project.server.user.forms import LoginForm, RegisterForm
# import redis


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


# @user_blueprint.route('/upload/', methods=('GET', 'POST'))
# # @login_required
# def upload():
#     form = CSVupload()
#     url = BOKEH_APP_URL + "/upload"
#
#     if request.method == 'POST':
#
#         data = form.csv.data
#         df = pd.read_csv(data)
#         redisConn = redis.from_url(os.environ.get("REDIS_URL"))
#         redisConn.set("user_upload", df.to_msgpack(compress='zlib'))
#         script = server_document(url=url)
#         return render_template(
#             "user/upload.html",
#             form=form, script=script)
#
#     script = server_document(url=url)
#     return render_template('user/upload.html', form=form, script=script)


# def create_data():
#     """Creates sample data."""
#     db.drop_all()
#     db.create_all()
#     # Read from some local cvs.
#     base_path = "project/tests/demodata/"
#     demo_lit_csvs = {
#         "sipos_2006_talanta_fig_2.csv": {
#             "counter_ion": "Na+",
#             "doi": "10.1016/j.talanta.2006.02.008"
#         },
#         "sipos_2006_talanta_fig_3_KOH.csv": {
#             "counter_ion": "K+",
#             "doi": "10.1016/j.talanta.2006.02.008",
#             "Al_concentration": 0.005
#         },
#         "sipos_2006_talanta_fig_3_LiOH.csv": {
#             "counter_ion": "Li+",
#             "doi": "10.1016/j.talanta.2006.02.008",
#             "Al_concentration": 0.005
#         },
#         "sipos_2006_talanta_fig_3_NaOH.csv": {
#             "counter_ion": "Na+",
#             "doi": "10.1016/j.talanta.2006.02.008",
#             "Al_concentration": 0.005
#         },
#         "sipos2006_RSC_table_1.csv": {
#             "counter_ion": "Cs+",
#             "doi": "10.1039/b513357b",
#             "Al_concentration": 3.0
#         },
#     }
#
#     # Create the entries in the appropriate databases.
#     # Al_concentration,OH_concentration,Al_ppm
#     for path, prop_dict in demo_lit_csvs.items():
#         df = pd.read_csv(base_path + path)
#         # Iterate through a zip of the matched values, and
#         # populate them.
#         for idx, row in df.iterrows():
#             row = row.to_dict()
#             nmr_entry = NMR_LitData(**row, **prop_dict)
#             db.session.add(nmr_entry)
#         db.session.commit()


# @user_blueprint.route('/bokeh_demo/', methods=['GET'])
# # @login_required
# def bokeh_demo():
#     # Generate the demo data.
#     url = "https://secret-cove-20095.herokuapp.com/NMRDemo"
#     script = server_document(url=url)
#     return render_template('user/bokeh_demo.html', script=script)


# @user_blueprint.route('/nmrdemo/', methods=['GET'])
# # @login_required
# def nmrdemo():
#     url = "https://secret-cove-20095.herokuapp.com/nmrapp"
#     script = server_document(url=url)
#     return render_template('user/bokeh_demo.html', script=script)


# @user_blueprint.route('/nmrsql/', methods=['GET'])
# # @login_required
# def nmrsql():
#     # Generate the demo data.
#     create_data()
#     # url = "https://secret-cove-20095.herokuapp.com/nmrsql"
#     url = BOKEH_APP_URL + "/nmrsql"
#
#     script = server_document(url=url)
#     return render_template('user/bokeh_demo.html', script=script)
