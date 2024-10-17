from flask import Flask, request
from flask_cors import CORS
from .mongo import init_mongo
from config import Config

from .routes.student_routes import student_bp
from .routes.class_routes import class_bp
from .routes.grade_routes import grade_bp

def create_app():
    app = Flask(__name__)
    app.config["MONGO_URI"] = Config.MONGO_URI

    mongo = init_mongo(app)

    try:
        mongo.db.command("ping")
        print("Successfully connected to MongoDB!")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")

    # Allow CORS for all origins
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    # Register blueprints
    app.register_blueprint(student_bp, url_prefix='/student')
    app.register_blueprint(class_bp, url_prefix='/class')
    app.register_blueprint(grade_bp, url_prefix='/grade')

    # Handle preflight requests
    @app.before_request
    def handle_options_request():
        if request.method == "OPTIONS":
            response = app.make_default_options_response()
            response.headers.add("Access-Control-Allow-Origin", "*")
            response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
            response.headers.add("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS")
            response.headers.add("Access-Control-Allow-Credentials", "true")
            return response

    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
        response.headers.add("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS")
        response.headers.add("Access-Control-Allow-Credentials", "true")
        return response

    return app
