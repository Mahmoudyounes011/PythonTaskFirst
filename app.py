from flask import Flask
from config import Config
from models.db import init_db
from routes.api import api

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize database
    init_db(app)
    
    # Register blueprint
    app.register_blueprint(api, url_prefix='/api')
    
    # Basic health check
    @app.route('/health')
    def health_check():
        return 'API is running'
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)