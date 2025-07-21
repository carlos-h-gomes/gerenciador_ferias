from flask import Blueprint

times_bp = Blueprint('times', __name__, template_folder='templates')

from . import routes
