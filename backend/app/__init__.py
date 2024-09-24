from flask import Flask
from flask_cors import CORS
from .mongo import init_mongo
from config import Config
from .firebase import get_firebase_db, printAuth

def create_app():
    app = Flask(__name__)

    app.config["MONGO_URI"] = Config.MONGO_URI
    # app.config["SECRET_KEY"] = "your_secret_key_here"

    mongo = init_mongo(app)
    firebase_db = get_firebase_db()

    printAuth()

    try:
        mongo.db.command("ping")
        print("Successfully connected to MongoDB!")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")


    CORS(app)

    # Import and register blueprints
    # from .routes.user_routes import user_bp
    # from .routes.course_routes import course_bp

    # app.register_blueprint(user_bp, url_prefix='/api/users')
    # app.register_blueprint(course_bp, url_prefix='/api/courses')

    return app
