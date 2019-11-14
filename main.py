from flask import request, make_response, redirect, render_template, session, url_for, flash
import unittest

from flask_login import login_required, current_user

from app import create_app
from app.forms import LoginForm, TodoForm, DeleteTodoForm, UpdateTodoForm
from app.firestore_service import get_users, get_todos, put_todo, delete_todo, update_todo

#creamos una instancia de Flask
app = create_app()


todos = ['TODO 1', 'TODO 2', 'TODO 3']

'''creamos ruta donde desplegaremos 'Hello World'
la app tiene una funcion llamada route que vamos
a sobreescribir, que recibe el nombre de la ruta 
donde queremos que se ejecute la funcion y 
retorne lo que encuentre en su archivo raiz
'''

@app.cli.command()
def test():
	tests = unittest.TestLoader().discover('tests')
	unittest.TextTestRunner().run(tests)

@app.errorhandler(404)
def not_found(error):
	return render_template('404.html', error=error)


@app.route('/')
def index():
    
    user_ip = request.remote_addr #obtengo la ip del usuario
    response = make_response(redirect('/hello')) #redirecciono a /hello
    session['user_ip'] = user_ip
    #response.set_cookie('user_ip',user_ip) #guardo la IP enn cookie

    return response

@app.route('/hello', methods=['GET', 'POST'])
@login_required
def hello():
	#obtenemos la ip del usuario
    #obtener la ip desde las cookie y no desde el response
    user_ip = session.get('user_ip')

    #para poder desplegar el username, lo obtendremos y lo agregaremos al contexto
    username = current_user.id

    todo_form = TodoForm()
    delete_form = DeleteTodoForm()
    update_form = UpdateTodoForm()

    context = {
    	'user_ip': user_ip, 
    	'todos': get_todos(user_id = username),
    	'username': username,
    	'todo_form': todo_form,
    	'delete_form': delete_form,
    	'update_form': update_form,
    }

    if todo_form.validate_on_submit():
    	put_todo(user_id=username, descripcion=todo_form.descripcion.data)

    	flash('Tu tarea se creo con éxito')
    	return redirect(url_for('hello'))
    #validate_on_submit: recibe los datos de la forma y los valida
    #la ruta detecta cuando se envia un POST y valida la forma (form)
    #partimos la funcion en 2
    #si se hace un POST validamos la info, si hace un GET envia un contexto

    return render_template('hello.html', **context)
 
'''
Las rutas dinamicas pueden recibir un string o un entero y obtener esos valores en la funcion
para procesarlas de la manera que necesitemos
'''
@app.route('/todos/delete/<todo_id>', methods=['POST']) #ruta dinamica 
def delete(todo_id):
	user_id = current_user.id
	delete_todo(user_id = user_id, todo_id = todo_id)
	return redirect(url_for('hello'))


	
@app.route('/todos/update/<todo_id>/<int:done>', methods=['POST']) #ruta dinamica 
def update(todo_id, done):
	user_id = current_user.id
	update_todo(user_id=user_id, todo_id=todo_id, done=done)

	return redirect(url_for('hello'))


