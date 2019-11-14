from flask_login import UserMixin #implementa los 4 metodos de UserModel solicitado por Flask Login


from app.firestore_service import get_user
#para asegurar que siempre tendremos la data que necesitamos
class UserData:
	def __init__(self, username, password):
		self.username = username
		self.password = password

class UserModel(UserMixin):
	# cada vez que creo un usuario le paso un user y un pass
	def __init__(self, user_data): #userdata de la clase UserData
		
		self.id = user_data.username #usamos el username como ID
		self.password = user_data.password

	# Busca a los usuarios en la base de datos y si existe lo devuelve como UserModel
	@staticmethod
	def query(user_id):
		user_doc = get_user(user_id)
		user_data = UserData(
			username = user_doc.id,
			password = user_doc.to_dict()['password']
			)
		return UserModel(user_data)

