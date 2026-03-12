from wtforms import Form
from wtforms import StringField, IntegerField, PasswordField, SelectField
from wtforms import EmailField 
from wtforms import validators

class UserForm(Form):
    id=IntegerField('id')

    nombre=StringField('nombre', [
        validators.DataRequired(message="El campo es requerido"),
        validators.length(min=3, max=10, message='Ingrese nombre valido')])
    apellidos=StringField('apellidos', [
        validators.DataRequired(message="El campo es requerido")])
    telefono=StringField('telefono', [
        validators.DataRequired(message="El campo es requerido")])
    email=EmailField('email', [
        validators.Email(message="Ingrese un correo valido")])

class MaestroForm(Form):
    matricula=IntegerField('matricula')

    nombre=StringField('nombre', [
        validators.DataRequired(message="El campo es requerido"),
        validators.length(min=3, max=10, message='Ingrese nombre valido')])
    apellidos=StringField('apellidos', [
        validators.DataRequired(message="El campo es requerido")])
    email=EmailField('email', [
        validators.Email(message="Ingrese un correo valido")])
    especialidad=StringField('especialidad', [
        validators.DataRequired(message="El campo es requerido")])
    

class CursoForm(Form):
    id=IntegerField('id')
    
    nombre=StringField('nombre', [
        validators.DataRequired(message="El campo es requerido")])
    descripcion=StringField('descripcion', [
        validators.DataRequired(message="El campo es requerido")])
    maestro_id = SelectField('Maestro', coerce=int)
