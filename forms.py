from wtforms import Form
from wtforms import StringField, IntegerField, PasswordField
from wtforms import EmailField 
from wtforms import validators

class UserForm(Form):
    id=IntegerField('id')

    nombre=StringField('nombre', [
        validators.DataRequired(message="El campo es requerido"),
        validators.length(min=3, max=10, message='Ingrese nombre valido')])
    apaterno=StringField('apaterno', [
        validators.DataRequired(message="El campo es requerido")])
    amaterno=StringField('amaterno', [
        validators.DataRequired(message="El campo es requerido")])
    correo=EmailField('correo', [
        validators.Email(message="Ingrese un correo valido")])

