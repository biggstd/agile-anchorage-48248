# project/server/main/views.py

from flask import render_template, Blueprint
from bokeh.embed import server_document


# from project.server.models import Ontology
# from project.server.ontologies import generate_demo_entries


main_blueprint = Blueprint('main', __name__,)


@main_blueprint.route('/')
def home():
    return render_template('main/home.html')


@main_blueprint.route("/about/")
def about():
    return render_template("main/about.html")


@main_blueprint.route('/bokeh_demo/', methods=['GET'])
def bokeh_demo():
    # Generate the demo data.
    url = "https://secret-cove-20095.herokuapp.com/NMRDemo"
    script = server_document(url=url)
    return render_template('main/bokeh_demo.html', script=script)

# @main_blueprint.route("/data/")
# def data():
#     generate_demo_entries()
#     text = str()
#     for exp in Ontology.objects.all():
#         text += exp.name
#         text += exp.sample_list
#
#     return render_template("main/data.html", text=text)
