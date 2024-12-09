from flask.views import MethodView
from flask_smorest import Blueprint
from app.schemas.user import *
from app.services.user import *

user_blp = Blueprint('User', 'user', url_prefix='/user', description='User related operations')

class UserResource(MethodView):

    @user_blp.route('/create', methods=['POST'])
    @user_blp.arguments(UserSchema)
    @user_blp.response(201, UserSchema)
    def post(user):
        """Create a new user"""
        return create_user(user)
    
    @user_blp.route('/login', methods=['POST'])
    @user_blp.arguments(UserLoginSchema)
    @user_blp.response(200, UserTokenSchema)
    def login(user):
        """Authenticate a user"""
        return authenticate_user(user)