# project/server/main/views.py

from flask import render_template, Blueprint
from bokeh.embed import server_document


main_blueprint = Blueprint('main', __name__,)


@main_blueprint.route('/')
def home():
    return render_template('main/home.html')


@main_blueprint.route("/about/")
def about():
    return render_template("main/about.html")


@main_blueprint.route("/bokeh-demo/", methods=['GET'])
# @login_required
def bokeh_demo():
    # url = 'localhost:{0}/bokehDemo'.format(port)
    url = "localhost:5006/bokehDemo"
    # url = "https://agile-anchorage-48248.herokuapp.com/bokehDemo"
    script = server_document(url=url)
    # print('Bokeh route called.', url)
    # print(script)
    return render_template("main/bokeh_app.html", script=script)
