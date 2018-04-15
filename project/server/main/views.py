# project/server/main/views.py

from flask import render_template, Blueprint


from project.server.models import Ontology
from project.server.ontologies import generate_demo_entries


main_blueprint = Blueprint('main', __name__,)


@main_blueprint.route('/')
def home():
    return render_template('main/home.html')


@main_blueprint.route("/about/")
def about():
    return render_template("main/about.html")


@main_blueprint.route("/data/")
def data():
    generate_demo_entries()
    text = str()
    for exp in Ontology.objects.all():
        text += exp.name
        text += exp.sample_list

    return render_template("main/data.html", text=text)
