from flask import current_app as app
from flask import render_template, Blueprint

page_blueprint = Blueprint("page", __name__)


@page_blueprint.route('/', defaults={'path': ''})
@page_blueprint.route('/<path:path>')
def index(path):
    return render_template("index.html")
