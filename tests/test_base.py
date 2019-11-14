from flask_testing import TestCase
from flask import current_app, url_for
from main import app

class MainTest(TestCase):
	def create_app(self):
		#ahora sabemos que estamos enn ambiente de testing
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
		return app

	def test_app_exists(self):
		#Existe una app (Si o No)
		self.assertIsNotNone(current_app)

	#Si la app se encuentra en modo testing
	def test_app_in_test_mode(self):
		self.assertTrue(current_app.config['TESTING'])

	#nuestro index nos redirige a hello?
	def test_index_redirects(self):
		response = self.client.get(url_for('index'))

		self.assertRedirects(response, url_for('hello'))

	#Hello nos response 200 cuando hacemos un get
	def test_hello_get(self):
		response = self.client.get(url_for('hello'))
		self.assert200(response)

	#Como hacer un post, hacemos un redirect a index
	def test_hello_post(self):
		response = self.client.post(url_for('hello'))
		self.assertTrue(response.status_code, 405 )

	#Test para saber si estamos importando nuestro Blueprint que debe existir en __init__ de app
	def test_auth_blueprint_exists(self):
		self.assertIn('auth',self.app.blueprints)

	#Debe retornar 200, se crea un nuevo objeto response
	def test_auth_login_get(self):
		response = self.client.get(url_for('auth.login')) #vamos al blueprint de auth y buscamos login
		self.assert200(response)
		#queremos responder un template de login

	#Debe retornar 200, se crea un nuevo objeto response
	def test_auth_login_template(self):
		self.client.get(url_for('auth.login')) #vamos al blueprint de auth y buscamos login
		self.assertTemplateUsed('login.html')
		#queremos responder un template de login

	def test_auth_login_post(self):
		#espera un user y un pass
		fake_form = {
			'username': 'fake',
			'password':  'fake-password'
		}
		response = self.client.post(url_for('auth.login'), data=fake_form)
		self.assertRedirects(response, url_for('index'))