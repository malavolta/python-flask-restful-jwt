import os

import flask_jwt_extended
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_jwt_extended.exceptions import NoAuthorizationError
from flask_restful import Api
from flask_jwt import JWTError

from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.user import UserRegister, User, UserLogin, UserLogout, TokenRefresh

app = Flask(__name__)

app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL',
                                                       'postgres://afczbzvi:h5TlgTZobP_QaaEBmyVjadPiUTlt08SB@motty.db.elephantsql.com:5432/afczbzvi')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'Malavolta'
app.config['JWT_DEFAULT_REALM'] = "ftp-sender"

api = Api(app)

jwt = JWTManager(app)  # /auth
app.config['PROPAGATE_EXCEPTIONS'] = True

api.add_resource(UserRegister, '/register')
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserLogout, "/logout")
api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')



@app.errorhandler(NoAuthorizationError)
def handle_auth_error(e):
    return jsonify({'menssage': 'Could no authorize. Did you include a valid Authorization in header'}), 401


if __name__ == '__main__':
    from db import db

    db.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()

    app.run(port=5000)
