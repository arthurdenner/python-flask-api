import os

from flask import Flask
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from resources.errors import errors


class CustomApi(Api):
    def handle_error(self, e):
        for val in self.app.error_handler_spec.values():
            for handler in val.values():
                registered_error_handlers = list(
                    filter(lambda x: isinstance(e, x), handler.keys()))
                if len(registered_error_handlers) > 0:
                    raise e
        return super().handle_error(e)


app = Flask(__name__)
app.config.from_envvar('ENV_FILE_LOCATION')

api = CustomApi(app, errors=errors)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
mail = Mail(app)
