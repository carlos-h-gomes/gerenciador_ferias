from flask import Blueprint

datas_bp = Blueprint('datas', __name__, template_folder='../../templates')

from . import routes
