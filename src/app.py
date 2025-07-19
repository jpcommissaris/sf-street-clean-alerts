from flask import Flask
from config import Config
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.logger.setLevel("INFO")

    from routes import api_bp

    app.register_blueprint(api_bp)
    return app


app = create_app()

if __name__ == "__main__":
    print("App Start")
    app.run(debug=app.config["DEBUG"], port=8080)
