from flask import Blueprint
from .feedback_routes import feedback_bp
from .analysis_routes import analysis_bp

api_bp = Blueprint("api", __name__)
api_bp.register_blueprint(feedback_bp, url_prefix="/feedback")
api_bp.register_blueprint(analysis_bp, url_prefix="/analysis")