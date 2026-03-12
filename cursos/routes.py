from flask import Flask, render_template, request, redirect, url_for
from flask import Blueprint
import forms

from models import db
from models import Maestros
from models import Cursos


cursos_bp=Blueprint('cursos',__name__)


@cursos_bp.route("/cursos", methods=['GET','POST'])
def cursos():
	create_form=forms.CursoForm(request.form)
	#tem=Cursos.query('select * from cursos')
	curso= Cursos.query.all()
	return render_template("cursos/cursos.html", form=create_form, curso=curso)

@cursos_bp.route("/insertarCursos", methods=['GET','POST'])
def insertarCursos():
	create_from=forms.CursoForm(request.form)
	maestros = Maestros.query.all()
	create_from.maestro_id.choices= [
		(m.matricula, f"{m.nombre} {m.apellidos}")
        for m in maestros
    ]

	if request.method=='POST':
		cur=Cursos(nombre=create_from.nombre.data,
					 descripcion=create_from.descripcion.data,
					 maestro_id = create_from.maestro_id.data
					 )
		db.session.add(cur)
		db.session.commit()
		return redirect(url_for('cursos.cursos'))
	return render_template("cursos/insertarCursos.html", form=create_from)

@cursos_bp.route("/detallesCurso")
def detallesCurso():

	if request.method == 'GET':

		id = request.args.get('id')
		curso = Cursos.query.get(id)
		alumnos = curso.alumnos

		return render_template("cursos/detalles.html",curso=curso,alumnos=alumnos
		)

@cursos_bp.route("/modificarCurso", methods=['GET','POST'])
def modificarCurso():
	create_from=forms.CursoForm(request.form)
	maestros = Maestros.query.all()
	create_from.maestro_id.choices= [
		(m.matricula, f"{m.nombre} {m.apellidos}")
        for m in maestros
    ]
	
	if request.method=='GET':
		id=request.args.get('id')
		cur1=db.session.query(Cursos).filter(Cursos.id==id).first()

		create_from.id.data=request.args.get('id')
		create_from.nombre.data=cur1.nombre
		create_from.descripcion.data=cur1.descripcion
		create_from.maestro_id.data=cur1.maestro_id

	if request.method=='POST':
		id = create_from.id.data 
		cur1 = db.session.query(Cursos).filter(Cursos.id==id).first()
		cur1.id=id
		cur1.nombre=str.rstrip(create_from.nombre.data)
		cur1.descrpicion=create_from.descripcion.data
		cur1.maestro_id=create_from.maestro_id.data
	
		db.session.add(cur1)
		db.session.commit()
		return redirect(url_for('cursos.cursos'))
	return render_template("cursos/modificarCursos.html", form=create_from)

@cursos_bp.route("/eliminarCurso", methods=['GET','POST'])
def eliminarCurso():
	create_from=forms.CursoForm(request.form)
	maestros = Maestros.query.all()
	create_from.maestro_id.choices= [
		(m.matricula, f"{m.nombre} {m.apellidos}")
        for m in maestros
    ]

	if request.method=='GET':
		id=request.args.get('id')
		cur1=db.session.query(Cursos).filter(Cursos.id==id).first()
		create_from.id.data=request.args.get('id')
		create_from.nombre.data=cur1.nombre
		create_from.descripcion.data=cur1.descripcion
		create_from.maestro_id.data=cur1.maestro_id

	if request.method=='POST':
		id = create_from.id.data
		cur1 = Cursos.query.get(id)
		
		db.session.delete(cur1)
		db.session.commit()
		return redirect(url_for('cursos.cursos'))
	return render_template("cursos/eliminarCursos.html", form=create_from)