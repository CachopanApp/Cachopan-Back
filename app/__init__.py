from flask import Flask
from flask_smorest import Api
from werkzeug.exceptions import HTTPException
from flask import jsonify
from datetime import timedelta

from .extensions import *
from .config import Config
from app.models import * # Import all models
from app.routes.user import user_blp 
from app.routes.client import client_blp
from app.routes.article import article_blp
from app.routes.sale import sale_blp

def create_app():

    app = Flask(__name__)
    
    # Swagger confguration
    app.config['API_TITLE'] = Config.API_TITLE
    app.config['API_VERSION'] = Config.API_VERSION
    app.config['OPENAPI_VERSION'] = Config.OPENAPI_VERSION
    app.config['OPENAPI_URL_PREFIX'] = Config.OPENAPI_URL_PREFIX
    app.config['OPENAPI_SWAGGER_UI_PATH'] = Config.OPENAPI_SWAGGER_UI_PATH
    app.config['OPENAPI_SWAGGER_UI_URL'] = Config.OPENAPI_SWAGGER_UI_URL

    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Config.SQLALCHEMY_TRACK_MODIFICATIONS

    # JWT configuration
    app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY
    app.config['API_SPEC_OPTIONS'] = {
        'security':[{"bearerAuth": []}],
        'components':{
            "securitySchemes":
                {
                    "bearerAuth": {
                        "type":"http",
                        "scheme": "bearer",
                        "bearerFormat": "JWT",
                        "description": "Type in the *'Value'* input box below: **'Bearer &lt;JWT&gt;'**, where JWT is the token",
                    }
                }
        }
    }

    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=180) 
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)  # TO-DO: Implementar la lógica para refrescar el token

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)

    # Initialize the API
    with app.app_context(): # This is necessary to avoid the following error: RuntimeError: application not registered on db instance and no application bound to current context
        
        try:
            db.create_all()
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()

        api = Api(app) # Initialize the API 

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            "code": 401,
            "status": "Unauthorized",
            "description": "The token has expired. Please refresh your token."
        }), 401
    
    # Error handler
    @app.errorhandler(HTTPException)
    def handle_exception(e):
        """Return JSON instead of HTML for HTTP errors."""
        response = e.get_response()
        response.data = jsonify({
            "code": e.code,
            "status": e.name,
            "description": e.description,
        }).data
        response.content_type = "application/json"
        return response

    api.register_blueprint(user_blp) # Register the user blueprint
    api.register_blueprint(client_blp) # Register the client blueprint
    api.register_blueprint(article_blp) # Register the article blueprint
    api.register_blueprint(sale_blp) # Register the sale blueprint

    return app