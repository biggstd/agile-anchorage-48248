# project/server/user/views.py


from flask import render_template, Blueprint, url_for, \
    redirect, flash, request, session, make_response
from flask_login import login_user, logout_user, login_required
import bokeh
import bokeh.client
import bokeh.embed

import json

from project.server import bcrypt, db, BOKEH_APP_URL, REDIS
from project.server.models import User
from project.server.user.forms import LoginForm, RegisterForm
# from project.server import bcrypt, db
from project.server.models import User



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


@user_blueprint.route('/create_sample/', methods=('GET', 'POST'))
def create_sample():
    '''Allows a user to create a sample and sumbit it to the MongoDB.'''

    # Build the URI for the Bokeh server.
    url = BOKEH_APP_URL + 'sample_creator/'
    print(url)

    def get_bokeh_values(bokeh_session):
        '''Pulls user submitted values and selections from the bokeh
        interface.
        '''
        # Get all the information from the variable number of fields.
        output_dict = dict()

        target_layout = bokeh_session.document.roots[0].children[3].children

        # The column of sample rows.
        for rc, sample_row in enumerate(target_layout):
            # The widgetboxes containing bokeh inputs.
            for bc, widgetbox in enumerate(sample_row.children):
                # The individual bokeh inputs.
                for ic, input_widget in enumerate(widgetbox.children):
                    dict_label = f'{rc}.{bc}.{ic}.{input_widget.name}'
                    output_dict[dict_label] = input_widget.value

        return json.dumps(output_dict)

    # Check if this is a submission. If so render the submitted object.
    if request.method == 'POST':

        # Get the Bokeh apps session id.
        curr_session_id = request.cookies.get('user_session_id')

        # Pull the bokeh session by this id.
        curr_session = bokeh.client.pull_session(
            session_id=curr_session_id, url=url)

        # Build the script with the session id.
        script = bokeh.embed.server_session(
            model=None, session_id=curr_session_id, url=url)

        # Read the values therin.
        sample_json = get_bokeh_values(curr_session)

        # print(vars(request))
        return render_template('user/create_sample.html', script=script,
                               sample_json=sample_json)

    # Build / get the bokeh session.
    curr_session = bokeh.client.pull_session(url=url)

    # Save the current session id as a key.
    curr_session_id = curr_session.id

    # Build the script for rendering.
    script = bokeh.embed.server_session(
        model=None, session_id=curr_session_id, url=url)

    # Build the response that will render a template and set a cookie value.
    response = make_response(
        render_template('user/create_sample.html', script=script))
    response.set_cookie('user_session_id', curr_session_id)

    return response
