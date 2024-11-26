from flask import Flask, request, jsonify
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

    # Allow CORS for specific origins, including localhost for development
    CORS(app, resources={r"/*": {"origins": ["https://vandytime.vercel.app", "http://localhost:3000"]}})

    @app.route('/')
    def index():
        return jsonify({"message": "Welcome to the Flask App!"})

    # Register blueprints
    app.register_blueprint(student_bp, url_prefix='/student')
    app.register_blueprint(class_bp, url_prefix='/class')
    app.register_blueprint(grade_bp, url_prefix='/grade')

    # Handle OPTIONS requests globally
    @app.before_request
    def handle_options_request():
        if request.method == "OPTIONS":
            response = app.make_default_options_response()
            response.headers["Access-Control-Allow-Origin"] = request.headers.get("Origin")
            response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
            response.headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS"
            response.headers["Access-Control-Allow-Credentials"] = "true"
            return response

    @app.after_request
    def after_request(response):
        # Allow origin dynamically based on the incoming request's origin
        origin = request.headers.get("Origin")
        if origin in ["https://vandytime.vercel.app", "http://localhost:3000"]:
            response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
        response.headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        return response

    return app
