from flask import Blueprint

authentication = Blueprint('authentication', __name__, template_folder='templates')
#testing
# Import routes at the bottom to avoid circular imports
from application.bp.authentication import routes


