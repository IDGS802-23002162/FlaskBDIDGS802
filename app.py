from flask import Flask, render_template, request, redirect, url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask import g
import forms

from maestros.routes import maestros_bp
from alumnos.routes import alumnos_bp
from cursos.routes import cursos_bp
from flask_migrate import Migrate

from models import db

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

csrf=CSRFProtect()
db.init_app(app)
migrate=Migrate(app, db)
app.register_blueprint(alumnos_bp)
app.register_blueprint(maestros_bp)
app.register_blueprint(cursos_bp)

@app.route("/")
@app.route("/index")
def index():
	return render_template("index.html")



@app.errorhandler(404)
def page_not_fount(e):
	return render_template("404.html"),404	



if __name__ == '__main__':
	csrf.init_app(app)
	with app.app_context():
		db.create_all()
	app.run()
