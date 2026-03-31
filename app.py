"""
SRISHTI AI OS - Main Backend Application
Complete AI Operating System with Multi-Brain Intelligence
"""

import os
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///srishti.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Initialize Database
db = SQLAlchemy(app)

# Enable CORS
CORS(app, resources={r"/api/*": {"origins": os.getenv('CORS_ORIGINS', '*')}})

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/srishti.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Import models
from backend.models import User, Message, Action, Log, Agent, Notification, CRM, Workflow, Analytics

# Import routes
from backend.routes import chat_routes, image_routes, video_routes, audio_routes
from backend.routes import code_routes, agent_routes, reason_routes, vision_routes
from backend.routes import crm_routes, analytics_routes

# Register blueprints
app.register_blueprint(chat_routes.bp)
app.register_blueprint(image_routes.bp)
app.register_blueprint(video_routes.bp)
app.register_blueprint(audio_routes.bp)
app.register_blueprint(code_routes.bp)
app.register_blueprint(agent_routes.bp)
app.register_blueprint(reason_routes.bp)
app.register_blueprint(vision_routes.bp)
app.register_blueprint(crm_routes.bp)
app.register_blueprint(analytics_routes.bp)

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    """System health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0',
        'environment': os.getenv('ENVIRONMENT', 'development')
    }), 200

# Root endpoint
@app.route('/', methods=['GET'])
def root():
    """Root endpoint with API information"""
    return jsonify({
        'name': 'SRISHTI AI OS',
        'tagline': 'The New Dimension of Creation',
        'version': '1.0.0',
        'status': 'operational',
        'endpoints': {
            'chat': '/api/chat',
            'image': '/api/image',
            'video': '/api/video',
            'audio': '/api/audio',
            'code': '/api/code',
            'agents': '/api/agents',
            'reason': '/api/reason',
            'vision': '/api/vision',
            'crm': '/api/crm',
            'analytics': '/api/analytics',
            'health': '/health'
        },
        'powered_by': 'YUGA Foundation - A New ERA Of Intelligence'
    }), 200

# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'status': 'error',
        'message': 'Endpoint not found',
        'code': 404
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f'Internal server error: {error}')
    return jsonify({
        'status': 'error',
        'message': 'Internal server error',
        'code': 500
    }), 500

@app.errorhandler(400)
def bad_request(error):
    """Handle 400 errors"""
    return jsonify({
        'status': 'error',
        'message': 'Bad request',
        'code': 400
    }), 400

# Request logging middleware
@app.before_request
def log_request():
    """Log incoming requests"""
    logger.info(f'{request.method} {request.path} - {request.remote_addr}')

@app.after_request
def log_response(response):
    """Log outgoing responses"""
    logger.info(f'Response: {response.status_code}')
    return response

# Database initialization
@app.cli.command()
def init_db():
    """Initialize the database"""
    db.create_all()
    logger.info('Database initialized successfully')

@app.cli.command()
def seed_db():
    """Seed the database with initial data"""
    # Create default user
    user = User(username='admin', email='admin@srishti.ai')
    db.session.add(user)
    db.session.commit()
    logger.info('Database seeded with initial data')

if __name__ == '__main__':
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Run the application
    port = int(os.getenv('PORT', 10000))
    debug = os.getenv('FLASK_DEBUG', 'False') == 'True'
    
    logger.info(f'Starting SRISHTI AI OS on port {port}')
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug,
        use_reloader=debug
    )
