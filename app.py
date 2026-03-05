from flask import Flask, render_template, request, redirect, url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask import g
import forms
from maestros.routes import maestros_bp
from flask_migrate import Migrate

from models import db

from models import Alumnos

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

csrf=CSRFProtect()
db.init_app(app)
migrate=Migrate(app, db)
app.register_blueprint(maestros_bp)

@app.route("/")
@app.route("/index", methods=['GET','POST'])
def index():
	create_form=forms.UserForm(request.form)
	#tem=Alumnos.query('select * from alumnos')
	alumno= Alumnos.query.all()
	return render_template("index.html", form=create_form, alumno=alumno)

@app.route("/Alumnos", methods=['GET','POST'])
def alumnos():
	create_from=forms.UserForm(request.form)
	if request.method=='POST':
		alum=Alumnos(nombre=create_from.nombre.data,
					 apellidos=create_from.apellidos.data,
					 email=create_from.email.data,
					 telefono=create_from.telefono.data
					 )
		db.session.add(alum)
		db.session.commit()
		return redirect(url_for('index'))
	return render_template("Alumnos.html", form=create_from)

@app.route("/detalles", methods=['GET','POST'])
def detalles():
	create_from=forms.UserForm(request.form)
	if request.method=='GET':

		id=request.args.get('id')
		alum1=db.session.query(Alumnos).filter(Alumnos.id==id).first()
		id=request.args.get('id')
		nombre=alum1.nombre
		apellidos=alum1.apellidos
		email=alum1.email
		telefono=alum1.telefono

	return render_template("detalles.html", form=create_from, nombre=nombre,apellidos=apellidos,email=email,telefono=telefono)

@app.route("/modificar", methods=['GET','POST'])
def modificar():
	create_from=forms.UserForm(request.form)
	if request.method=='GET':
		id=request.args.get('id')
		alum1=db.session.query(Alumnos).filter(Alumnos.id==id).first()

		create_from.id.data=request.args.get('id')
		create_from.nombre.data=alum1.nombre
		create_from.apellidos.data=alum1.apellidos
		create_from.email.data=alum1.email
		create_from.telefono.data=alum1.telefono

	if request.method=='POST':
		alum1 = db.session.query(Alumnos).filter(Alumnos.id==id).first()
		alum1.id=id
		alum1.nombre=str.rstrip(create_from.nombre.data)
		alum1.apellidos=create_from.apellidos.data
		alum1.email=create_from.email.data
		alum1.telefono=create_from.telefono.data
		db.session.add(alum1)
		db.session.commit()
		return redirect(url_for('index'))
	return render_template("modificar.html", form=create_from)

@app.route("/eliminar", methods=['GET','POST'])
def eliminar():
	create_from=forms.UserForm(request.form)
	if request.method=='GET':
		id=request.args.get('id')
		alum1=db.session.query(Alumnos).filter(Alumnos.id==id).first()
		create_from.id.data=request.args.get('id')
		create_from.nombre.data=alum1.nombre
		create_from.apellidos.data=alum1.apellidos
		create_from.email.data=alum1.email
		create_from.telefono.data=alum1.telefono

	if request.method=='POST':
		alum1 = Alumnos.query.get(id)
		
		db.session.add(alum1)
		db.session.commit()
		return redirect(url_for('index'))
	return render_template("eliminar.html", form=create_from)	


@app.errorhandler(404)
def page_not_fount(e):
	return render_template("404.html"),404	



if __name__ == '__main__':
	csrf.init_app(app)
	with app.app_context():
		db.create_all()
	app.run()
