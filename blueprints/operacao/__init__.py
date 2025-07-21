from flask import Blueprint

operacao_bp = Blueprint('operacao', __name__, template_folder='../../templates')

from . import routes
