from flask import Blueprint

squads_bp = Blueprint('squads', __name__, template_folder='../../templates')

from . import routes
