"""Contains function that creates the app"""
from flask import Flask, jsonify
from flask_cors import CORS

from api.views.auth import users_bp
from api.views.create_incident import create_incident_bp
from api.views.get_incidents import get_inc_bp
from api.views.edit_incident import edit_bp
from instance.config import Config


def create_app(config=None):
    """Set up Flask application in function"""
    app = Flask(__name__)
    CORS(app)

    @app.route('/')
    @app.route('/api/v1')
    def _hello_ireporter():
        return (
            jsonify(
                {
                    "message": "Welcome to iReporter API V2",
                    "status": 200
                }
            ),
            200,
        )

    @app.errorhandler(400)
    def _page_not_found(e):
        return (
            jsonify(
                {
                    "error": "Bad JSON format data",
                    "status": 400
                }
            ),
            400,
        )
    @app.errorhandler(401)
    def _not_authorized(e):
        return (
            jsonify({"error": "You are not authorized to access this resource"}),
            401,
        )

    @app.errorhandler(404)
    def _page_not_found(e):
        return (
            jsonify(
                {"error": "Endpoint for specified URL does not exist"}
            ),
            404,
        )

    @app.errorhandler(405)
    def _method_not_allowed(e):
        return (
            jsonify({"error": "Method not allowed"}),
            405,
        )

    app.config.from_object(Config)
    app.register_blueprint(users_bp)
    app.register_blueprint(create_incident_bp)
    app.register_blueprint(get_inc_bp)
    app.register_blueprint(edit_bp)

    return app
