from flask import Blueprint

bp = Blueprint('main', __name__)

from app.main import routes, reference_routes, ajax_routes, activity_routes
