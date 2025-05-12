from flask import Flask
from config import Config
from models.db import init_db
from routes.api import api
from flask_jwt_extended import JWTManager
from routes.auth import auth_bp, init_mail
from models.revoked_token import RevokedToken
from flask_mail import Mail
from routes.todos import todos

mail = Mail() 

def create_app():
    app = Flask(__name__)
    
    app.config.from_object(Config)
    
    init_db(app)
    
    app.register_blueprint(api, url_prefix='/api')
    
    # Basic health check
    @app.route('/health')
    def health_check():
        return 'API is running'
    
    jwt = JWTManager(app)
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        return RevokedToken.is_jti_blacklisted(jti)

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(todos, url_prefix='/api')


    mail.init_app(app)   
    init_mail(mail) 
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)