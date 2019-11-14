import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


project_id = 'project-todo-258801'

credential = credentials.Certificate('./Project-ToDo-key.json') #creamos la credencial
firebase_admin.initialize_app(credential)

db = firestore.client() #conectar a los servicios de firestore


#obtiene la coleccion de usuarios
def get_users():
	return db.collection('users').get()

def get_user(user_id):
	return db.collection('users').document(user_id).get() #si no hacemos .get(), solo hacemos una referencia a ese elemento

def get_todos(user_id):
	return db.collection('users').document(user_id).collection('todos').get()

def user_put(user_data):
	user_ref = db.collection('users').document(user_data.username)
	user_ref.set({'password': user_data.password})

def put_todo(user_id, descripcion):
	#llamamos a la base de datos
	todos_collection_ref = db.collection('users').document(user_id).collection('todos')
	#le decimos a la base de datos que agregue un usuario con un random_id
	todos_collection_ref.add({'descripcion': descripcion, 'done': False})

def delete_todo(user_id, todo_id):
	#es posible agregar la ruta de la siguiente manera
	#todo_ref = db.document('users/{}/todos/{}'.format(user_id, todo_id))
	todo_fer = _get_todo_ref(user_id, todo_id)
	todo_ref.delete()

def update_todo(user_id, todo_id, done):
	#hay que cambiar el estado de done en BD porque lo envia como enterno y bd lo recibe como enterno 
	todo_done = not bool(done)
	todo_ref = _get_todo_ref(user_id, todo_id)
	print("DONE: ", todo_done)
	todo_ref.update({'done': todo_done})

def _get_todo_ref(user_id, todo_id):
	return db.collection('users').document(user_id).collection('todos').document(todo_id)
