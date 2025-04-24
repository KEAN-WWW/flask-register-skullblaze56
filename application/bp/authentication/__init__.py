"""Authentication blueprint"""
from flask import Blueprint

authentication = Blueprint('authentication', __name__, 
                         template_folder='templates')

# Import routes after blueprint creation to avoid circular imports
from application.bp.authentication import routes


