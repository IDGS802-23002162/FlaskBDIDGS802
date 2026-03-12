from flask import Flask, render_template, request, redirect, url_for
from flask import Blueprint
import forms

from models import db
from models import Maestros

maestros_bp=Blueprint('maestros',__name__)


@maestros_bp.route('/maestros', methods=['GET','POST'])
def maestros():
    create_form=forms.MaestroForm(request.form)
    #tem=Maestros.query('select * from maestros')
    maestro=Maestros.query.all()
    return render_template("maestros/Maestros.html", form=create_form, maestro=maestro)

@maestros_bp.route("/insertarMaestros", methods=['GET','POST'])
def alumnos():
	create_from=forms.MaestroForm(request.form)
	if request.method=='POST':
		mae=Maestros(nombre=create_from.nombre.data,
					 apellidos=create_from.apellidos.data,
					 email=create_from.email.data,
					 especialidad=create_from.especialidad.data
					 )
		db.session.add(mae)
		db.session.commit()
		return redirect(url_for('maestros.maestros'))
	return render_template("maestros/insertarMaestros.html", form=create_from)

@maestros_bp.route("/detallesMaestros", methods=['GET','POST'])
def detalles():
	if request.method=='GET':

		matricula=request.args.get('matricula')
		maestro1=db.session.query(Maestros).filter(Maestros.matricula==matricula).first()
		matricula=request.args.get('matricula')
		
		nombre=maestro1.nombre
		apellidos=maestro1.apellidos
		email=maestro1.email
		especialidad=maestro1.especialidad

	return render_template("detalles.html", nombre=nombre, apellidos=apellidos, email=email, especialidad=especialidad)

@maestros_bp.route("/modificarMaestros", methods=['GET','POST'])
def modificar():
	create_from=forms.MaestroForm(request.form)
	if request.method=='GET':
		matricula=request.args.get('matricula')
		mae1=db.session.query(Maestros).filter(Maestros.matricula==matricula).first()

		create_from.matricula.data=request.args.get('matricula')
		create_from.nombre.data=mae1.nombre
		create_from.apellidos.data=mae1.apellidos
		create_from.email.data=mae1.email
		create_from.especialidad.data=mae1.especialidad

	if request.method=='POST':
		matricula = create_from.matricula.data 
		mae1=db.session.query(Maestros).filter(Maestros.matricula==matricula).first()
		mae1.matricula=matricula
		mae1.nombre=str.rstrip(create_from.nombre.data)
		mae1.apellidos=create_from.apellidos.data
		mae1.email=create_from.email.data
		mae1.especialidad=create_from.especialidad.data
		db.session.add(mae1)
		db.session.commit()
		return redirect(url_for('maestros.maestros'))
	return render_template("maestros/modificarMaestros.html", form=create_from)

@maestros_bp.route("/eliminarMaestros", methods=['GET','POST'])
def eliminarMaestros():
	create_from=forms.MaestroForm(request.form)
	if request.method=='GET':
		matricula=request.args.get('matricula')
		mae1=db.session.query(Maestros).filter(Maestros.matricula==matricula).first()
		create_from.matricula.data=request.args.get('matricula')
		create_from.nombre.data=mae1.nombre
		create_from.apellidos.data=mae1.apellidos
		create_from.email.data=mae1.email
		create_from.especialidad.data=mae1.especialidad

	if request.method=='POST':
		matricula = create_from.matricula.data 
		mae1 = Maestros.query.get(matricula)
		
		db.session.delete(mae1)
		db.session.commit()
		return redirect(url_for('maestros.maestros'))
	return render_template("maestros/eliminarMaestros.html", form=create_from)	