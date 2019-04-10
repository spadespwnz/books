from flask import current_app as app
from flask import render_template, Blueprint

page_blueprint = Blueprint("page", __name__)


@page_blueprint.route("/")
@page_blueprint.route("/index")
def index():
    return render_template("index.html")
