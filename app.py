from flask import Flask, render_template, request, redirect, url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask import g
import forms
from flask_migrate import Migrate

from models import db

from models import Alumnos

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf=CSRFProtect()
db.init_app(app)
migrate=Migrate(app,db)


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
					 apaterno=create_from.apaterno.data,
					 email=create_from.email.data)
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
		apaterno=alum1.apaterno
		email=alum1.email

	return render_template("detalles.html", form=create_from, nombre=nombre,apaterno=apaterno,email=email)

@app.route("/modificar", methods=['GET','POST'])
def modificar():
	create_from=forms.UserForm(request.form)
	if request.method=='GET':
		id=request.args.get('id')
		alum1=db.session.query(Alumnos).filter(Alumnos.id==id).first()

		create_from.id.data=request.args.get('id')
		create_from.nombre.data=alum1.nombre
		create_from.apaterno.data=alum1.apaterno
		create_from.correo.data=alum1.email

	if request.method=='POST':
		alum1 = db.session.query(Alumnos).filter(Alumnos.id==id).first()
		alum1.id=id
		alum1.nombre=str.rstrip(create_from.nombre.data)
		alum1.apaterno=create_from.email.data
		alum1.email=create_from.email.data
		db.session.add(alum1)
		db.session.commit()
		return redirect(url_for('index'))
	return render_template("modificar.html")

@app.route("/eliminar", methods=['GET','POST'])
def eliminar():
	create_from=forms.UserForm(request.form)
	if request.method=='GET':
		id=request.args.get('id')
		alum1=db.session.query(Alumnos).filter(Alumnos.id==id).first()
		create_from.id.data=request.args.get('id')
		create_from.nombre.data=alum1.nombre
		create_from.apaterno.data=alum1.apaterno
		create_from.email.data=alum1.email
	if request.method=='POST':
		alum1 = Alumnos.query.get(id)
		
		db.session.add(alum1)
		db.session.commit()
		return redirect(url_for('index'))
	return render_template("eliminar.html")	


@app.errorhandler(404)
def page_not_fount(e):
	return render_template("404.html"),404	

if __name__ == '__main__':
	csrf.init_app(app)
	with app.app_context():
		db.create_all()
	app.run()
