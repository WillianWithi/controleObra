#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

from flask import Flask, render_template, request, url_for, redirect

from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db = SQLAlchemy(app)


class Imovel(db.Model):
	__tablename__ = 'imoveis'
	_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	endereco = db.Column(db.String)
	dimensoes = db.Column(db.Float)
	tipo = db.Column(db.String)
	responsavel = db.Column(db.String)
	qtd_comodos = db.Column(db.Integer)
	status = db.Column(db.String)
	data = db.Column(db.String)

	def __init__(self, endereco, dimensoes, tipo, responsavel, qtd_comodos, status, data):
		self.endereco = endereco
		self.dimensoes = dimensoes
		self.tipo = tipo
		self.responsavel = responsavel
		self.qtd_comodos = qtd_comodos
		self.status = status
		self.data = data

db.create_all()

@app.route("/")
@app.route("/home")
def home():
	return render_template("index.html")

@app.route("/")
@app.route("/cadastrar")
def cadastrar():
	return render_template("cadastro.html")

def voltar():
	return render_template("home")

@app.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
	if request.method == "POST":
		endereco = (request.form.get("endereco"))
		dimensoes = (request.form.get("dimensoes"))
		tipo = (request.form.get("tipo"))
		responsavel = (request.form.get("responsavel"))
		qtd_comodos = (request.form.get("qtd_comodos"))
		status = (request.form.get("status"))
		data = (request.form.get("data"))

		if endereco and dimensoes and tipo and responsavel and qtd_comodos and status and data:
			imovel = Imovel(endereco, dimensoes, tipo, responsavel, qtd_comodos, status, data)
			db.session.add(imovel)
			db.session.commit()

	return redirect(url_for("home"))

@app.route("/lista")
def lista():
	imoveis = Imovel.query.all()
	return render_template("lista.html", imoveis=imoveis)

@app.route("/atualizar/<int:id>", methods=['GET', 'POST'])
def atualizar(id):
	imovel = Imovel.query.filter_by(_id=id).first()
	if request.method == "POST":
		endereco = (request.form.get("endereco"))
		dimensoes = (request.form.get("dimensoes"))
		tipo = (request.form.get("tipo"))
		responsavel = (request.form.get("responsavel"))
		qtd_comodos = (request.form.get("qtd_comodos"))
		status = (request.form.get("status"))
		data = (request.form.get("data"))

		if endereco and dimensoes and tipo and responsavel and qtd_comodos and status and data:
			imovel.endereco  = endereco
			imovel.dimensoes = dimensoes
			imovel.tipo = tipo
			imovel.responsavel = responsavel
			imovel.qtd_comodos = qtd_comodos
			imovel.status = status
			imovel.data = data
			db.session.commit()

	return render_template("atualizar.html", imovel=imovel)

@app.route("/excluir/<int:id>")
def excluir(id):
	imovel = Imovel.query.filter_by(_id=id).first()
	db.session.delete(imovel)
	db.session.commit()

	imoveis = Imovel.query.all()
	return render_template("lista.html", imoveis=imoveis)


if __name__ == "__main__":
	app.run(debug=True)