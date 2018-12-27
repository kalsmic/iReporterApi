"""Contains function that creates the app"""
from flask import Flask, jsonify
from flask_cors import CORS

from api.helpers.responses import supported_end_points
from api.routes.admin import admin_flags_bp
from api.routes.auth import users_bp
from api.routes.delete_incident import delete_red_flag_bp
from api.routes.edit_incident import edit_red_flags_bp
from api.routes.get_incidents import get_red_flags_bp
from api.routes.incidents import red_flags_bp
from config import Config


def create_app(config="None"):
    """Set up Flask application in function"""
    app = Flask(__name__)
    CORS(app)

    @app.errorhandler(404)
    def page_not_found(e):
        return (
            jsonify(
                {
                    "error": "Endpoint for specified URL does not exist",
                    "supportedEndPoints": supported_end_points,
                }
            ),
            404,
        )

    app.config.from_object(Config)
    app.register_blueprint(users_bp)
    app.register_blueprint(red_flags_bp)
    app.register_blueprint(get_red_flags_bp)
    app.register_blueprint(edit_red_flags_bp)
    app.register_blueprint(delete_red_flag_bp)
    app.register_blueprint(admin_flags_bp)

    return app
