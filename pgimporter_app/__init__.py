from flask import Flask
from .views import main_blueprint
from .config import Config

def create_app():
    # Create object app type Flask
    app = Flask(__name__)
    # Load Configuration variables
    app.config.from_object(Config)
        
    # Register Blueprints for better modularity
    app.register_blueprint(main_blueprint)
    
    # Continue to application
    return app