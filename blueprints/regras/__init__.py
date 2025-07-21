from flask import Blueprint

regras_bp = Blueprint('regras', __name__, template_folder='../../templates')

from . import routes
