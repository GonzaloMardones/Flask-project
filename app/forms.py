from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField,SubmitField
from wtforms.validators import DataRequired # Me dira si falto el usuario y/o password
import unittest

class LoginForm(FlaskForm):
	#las formas tienen fields o campos que hay que completar
	#DataValidators es una lista de validadores que pasamos una instancia del validador
	username = StringField('Nombre de usuario', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Enviar')

class TodoForm(FlaskForm):
	descripcion = StringField('Descripción', validators=[DataRequired()])
	submit = SubmitField('Crear')

class DeleteTodoForm(FlaskForm):
	submit = SubmitField('Borrar')

class UpdateTodoForm(FlaskForm):
	submit = SubmitField('Actualizar')
	