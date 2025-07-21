from flask import Blueprint

analitica_bp = Blueprint('analitica', __name__, template_folder='../../templates')

from . import routes
