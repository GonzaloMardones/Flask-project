from flask import Blueprint

# Dentro de este Blueprint se crean views, template
# y las vistas de submit, logout, login y otras seran dirigidas aqui

auth = Blueprint('auth', __name__, url_prefix = '/auth') #__name__ porque aplico a este archivo, todas las rutas que tengan auth seran redirigidas a este Blueprint

from . import views
