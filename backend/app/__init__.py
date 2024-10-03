from flask import Flask
from flask_cors import CORS
from .mongo import init_mongo
from config import Config
# from .firebase import get_firebase_db, printAuth

from .routes.student_routes import student_bp
from .routes.class_routes import class_bp
from .routes.grade_routes import grade_bp

def create_app():
    app = Flask(__name__)

    app.config["MONGO_URI"] = Config.MONGO_URI
    # app.config["SECRET_KEY"] = "your_secret_key"

    mongo = init_mongo(app)
    # firebase_db = get_firebase_db()

    # printAuth()

    try:
        mongo.db.command("ping")
        print("Successfully connected to MongoDB!")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")


    CORS(app)

    # Import and register blueprints

    app.register_blueprint(student_bp, url_prefix='/student')
    app.register_blueprint(class_bp, url_prefix='/class')
    app.register_blueprint(grade_bp, url_prefix='/grade')

    return app
