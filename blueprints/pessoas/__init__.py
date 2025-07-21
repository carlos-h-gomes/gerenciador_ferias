from flask import Blueprint

pessoas_bp = Blueprint('pessoas', __name__, template_folder='../../templates')

from . import routes
