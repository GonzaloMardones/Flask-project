from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

from .config import Config
from .auth import auth
from .models import UserModel
#La app que nos regresa la funcion

login_manager = LoginManager()
login_manager.login_view = 'auth.login' #ruta de login que maneje


@login_manager.user_loader
def load_user(username):
	return UserModel.query(username)


def create_app():
	app = Flask(__name__)

	# Inicializar una extension, que recibe una app de Flask
	bootstrap = Bootstrap(app)

	app.config.from_object(Config) #Aqui creamos la llave secreta desde la clase config

	#antes de registrar los blueprint, le diremos a LoginManager que inicialice la app
	#protegeremos la ruta con un decorador login_required
	login_manager.init_app(app)


	app.register_blueprint(auth)
	return app