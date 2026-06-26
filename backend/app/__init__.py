"""
Kaori Flask Backend - Application Factory
"""
from flask import Flask
from flask_cors import CORS
from supabase import create_client
from .config import Config


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Enable CORS for frontend
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Initialize Supabase client
    app.supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
    
    # Register blueprints
    from .routes.profile import profile_bp
    from .routes.questions import questions_bp
    from .routes.selfies import selfies_bp
    from .routes.wardrobe import wardrobe_bp
    from .routes.health import health_bp
    from .routes.activity import activity_bp
    from .routes.notifications import notifications_bp
    
    app.register_blueprint(profile_bp, url_prefix='/api')
    app.register_blueprint(questions_bp, url_prefix='/api')
    app.register_blueprint(selfies_bp, url_prefix='/api')
    app.register_blueprint(wardrobe_bp, url_prefix='/api')
    app.register_blueprint(health_bp, url_prefix='/api')
    app.register_blueprint(activity_bp, url_prefix='/api')
    app.register_blueprint(notifications_bp, url_prefix='/api')
    
    # Health check endpoint
    @app.route('/api/health')
    def health_check():
        return {'status': 'ok', 'app': 'Kaori API 💕'}
    
    return app
