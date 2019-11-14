from . import auth #Desde este directorio importa auth
from flask import render_template, session, redirect, flash, url_for
from app.forms import LoginForm
from flask_login import login_user, login_required, logout_user

from werkzeug.security import generate_password_hash, check_password_hash #libreria de seguridad

from app.firestore_service import get_user, user_put
from app.models import UserData,UserModel

# En esta funcionn se renderea la funcion de loginn
@auth.route('/login', methods = ['GET','POST'])
def login():
    #Para mandar un submit, hay que agregarlo al contexto
	login_form = LoginForm()
	# La funcion debe retornar 200 y la app debe tener incluido el Blueprint
	context = {
		'login_form': LoginForm()
	}
	
	if login_form.validate_on_submit():
		#validemos que el usuario esta en la base de datos
		#Si la forma es valida, obtenemos el username y password
		username = login_form.username.data #es ua instancia de StringField
		password = login_form.password.data

		user_doc = get_user(username)

		if user_doc.to_dict () is not None:
			password_from_db = user_doc.to_dict()['password']

			if password == password_from_db:
				user_data = UserData(username, password)
				user = UserModel(user_data)

				login_user(user)

				flash('Bienvenido de nuevo')

				redirect(url_for('hello'))
			else:
				flash('La información no coincide')
		else:
			flash('El usuario no existe')
		#como ya obtenemos el username, lo guardamos en la sesion
		#para desplegar el username
		return redirect(url_for('index'))
	return render_template('login.html', **context) # se envia el contexto expandido

@auth.route('logout')
@login_required
def logout():
	logout_user()
	flash('Regresa pronto')
	return redirect(url_for('auth.login'))

@auth.route('signup', methods =['GET','POST'])
def signup():
	signup_form = LoginForm()

	context = {
		'signup_form': signup_form
	}

	#POST: buscamos al usuario si es que existe, ya es usuario, si no, lo creamos
	if signup_form.validate_on_submit():
		username = signup_form.username.data
		password = signup_form.password.data

		#vamos a buscar ese usuario en nuestra BD
		user_doc = get_user(username)
		if user_doc.to_dict() is None:
			#generamos un password hash del password que nos envia el usuario
			password_hash = generate_password_hash(password)
			#creamos una nueva instancia de user_data
			user_data = UserData(username, password_hash)

			#creamos una funcion desde firestore_service para que persista el dato del usuario
			user_put(user_data)
			#ya que creamos un nuevo usuario en la base de datos, creamos un usermodel para poder logearlo en la sesion
			user = UserModel(user_data)
			login_user(user)
			flash('Bienvenido')

			return redirect(url_for('hello'))

		else:
			flash('El usuario ya existe')
	return render_template('signup.html', **context)

