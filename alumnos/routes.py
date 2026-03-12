from flask import Flask, render_template, request, redirect, url_for
from flask import Blueprint
import forms

from models import db
from models import Alumnos
from models import Cursos


alumnos_bp=Blueprint('alumnos',__name__)

@alumnos_bp.route("/alumnos", methods=['GET','POST'])
def alumnos():
	create_form=forms.UserForm(request.form)
	#tem=Alumnos.query('select * from alumnos')
	alumno= Alumnos.query.all()
	return render_template("alumnos/Alumnos.html", form=create_form, alumno=alumno)

@alumnos_bp.route("/insertarAlumnos", methods=['GET','POST'])
def insertarAlumnos():
	create_from=forms.UserForm(request.form)
	if request.method=='POST':
		alum=Alumnos(nombre=create_from.nombre.data,
					 apellidos=create_from.apellidos.data,
					 email=create_from.email.data,
					 telefono=create_from.telefono.data
					 )
		db.session.add(alum)
		db.session.commit()
		return redirect(url_for('alumnos.alumnos'))
	return render_template("alumnos/insertarAlumnos.html", form=create_from)

@alumnos_bp.route("/detalles", methods=['GET','POST'])
def detalles():
	
	if request.method=='GET':

		id=request.args.get('id')
		alum1=db.session.query(Alumnos).filter(Alumnos.id==id).first()
		id=request.args.get('id')
		alumno = Alumnos.query.get(id)
		cursos = alumno.cursos

		nombre=alum1.nombre
		apellidos=alum1.apellidos
		email=alum1.email
		telefono=alum1.telefono

	return render_template("detalles.html", nombre=nombre,apellidos=apellidos,email=email,telefono=telefono, cursos=cursos)

@alumnos_bp.route("/modificar", methods=['GET','POST'])
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
		id = create_from.id.data 
		alum1 = db.session.query(Alumnos).filter(Alumnos.id==id).first()
		alum1.id=id
		alum1.nombre=str.rstrip(create_from.nombre.data)
		alum1.apellidos=create_from.apellidos.data
		alum1.email=create_from.email.data
		alum1.telefono=create_from.telefono.data
		db.session.add(alum1)
		db.session.commit()
		return redirect(url_for('alumnos.alumnos'))
	return render_template("alumnos/modificar.html", form=create_from)

@alumnos_bp.route("/eliminar", methods=['GET','POST'])
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
		id = create_from.id.data
		alum1 = Alumnos.query.get(id)
		
		db.session.delete(alum1)
		db.session.commit()
		return redirect(url_for('alumnos.alumnos'))
	return render_template("alumnos/eliminar.html", form=create_from)	

@alumnos_bp.route("/registrar", methods=['GET','POST'])
def registrar():
    alumno_id = request.args.get('id')
    alumno = Alumnos.query.get(alumno_id)
    cursos = Cursos.query.all()

    create_from=forms.UserForm(request.form)
	
    if request.method == 'POST':

        curso_id = request.form.get('curso_id')
        curso = Cursos.query.get(curso_id)
        if curso not in alumno.cursos:
            alumno.cursos.append(curso)
        db.session.commit()

        return redirect(url_for('alumnos.alumnos'))
    return render_template("alumnos/registrar.html", cursos=cursos, alumno=alumno, form=create_from)	