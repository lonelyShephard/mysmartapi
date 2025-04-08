from flask import Blueprint

# Create a blueprint for the routes
routes_bp = Blueprint('routes', __name__)

# Import the route modules
from .auth import *
from .historical import *
from .orders import *
from .streaming import *
from .exit import *

# Register the routes with the blueprint
def register_routes(app):
    app.register_blueprint(routes_bp)