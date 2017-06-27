#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
from flask import Flask, render_template, request, url_for, redirect
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)

# cadastro de imoveis
class Imovel(db.Model):
	__tablename__ = 'imoveis'
	_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	nome = db.Column(db.String)
	endereco = db.Column(db.String)
	dimensoes = db.Column(db.Float)
	tipo = db.Column(db.String)
	responsavel = db.Column(db.String)
	qtd_comodos = db.Column(db.Integer)
	status = db.Column(db.String)
	data = db.Column(db.String)

	def __init__(self,nome, endereco, dimensoes, tipo, responsavel, qtd_comodos, status, data):
		self.nome = nome
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

@app.route("/insumo")
def insumo():
	return render_template("insumo.html")


def voltar():
	return render_template("home")

@app.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
	if request.method == "POST":
		nome = (request.form.get("nome"))
		endereco = (request.form.get("endereco"))
		dimensoes = (request.form.get("dimensoes"))
		tipo = (request.form.get("tipo"))
		responsavel = (request.form.get("responsavel"))
		qtd_comodos = (request.form.get("qtd_comodos"))
		status = (request.form.get("status"))
		data = (request.form.get("data"))

		if nome and endereco and dimensoes and tipo and responsavel and qtd_comodos and status and data:
			imovel = Imovel(nome, endereco, dimensoes, tipo, responsavel, qtd_comodos, status, data)
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
		nome = (request.form.get("nome"))
		endereco = (request.form.get("endereco"))
		dimensoes = (request.form.get("dimensoes"))
		tipo = (request.form.get("tipo"))
		responsavel = (request.form.get("responsavel"))
		qtd_comodos = (request.form.get("qtd_comodos"))
		status = (request.form.get("status"))
		data = (request.form.get("data"))

		if nome and endereco and dimensoes and tipo and responsavel and qtd_comodos and status and data:
			imovel.nome = nome
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


# cadastro de insumo
class Insumo(db.Model):
	__tablename__ = 'insumo'
	_id 		= db.Column(db.Integer, primary_key = True, autoincrement = True)
	codigo 		= db.Column(db.Integer)
	descricao 	= db.Column(db.String)
	unidade 	= db.Column(db.Integer)

	def __init__(self, codigo, descricao, unidade):
		self.codigo	= codigo
		self.descricao= descricao
		self.unidade= unidade
db.create_all()

@app.route("/cadastro-insumo", methods=['GET', 'POST'])
def cadastro_insumo():
	if request.method == "POST":
		codigo = (request.form.get("codigo"))
		descricao = (request.form.get("descricao"))
		unidade = (request.form.get("unidade"))

		if codigo and descricao and unidade:
			insumo = Insumo(codigo, descricao, unidade)
			db.session.add(insumo)
			db.session.commit()
	return redirect(url_for("home"))

@app.route("/lista-insumo")
def lista_insumo():
	insumos = Insumo.query.all()
	return render_template("lista_insumo.html", insumos=insumos)

@app.route("/atualizar-insumo/<int:id>", methods=['GET', 'POST'])
def atualizar_insumo(id):
	insumo = Insumo.query.filter_by(_id=id).first()
	if request.method == "POST":
		codigo = (request.form.get("codigo"))
		descricao = (request.form.get("descricao"))
		unidade = (request.form.get("unidade"))

		if codigo and descricao and unidade:
			insumo.codigo  = codigo
			insumo.descricao = descricao
			insumo.unidade = unidade
			db.session.commit()

	return render_template("atualizar_insumo.html", insumo=insumo)

@app.route("/excluir-insumo/<int:id>")
def excluir_insumo(id):
	insumo = Insumo.query.filter_by(_id=id).first()
	db.session.delete(insumo)
	db.session.commit()

	insumos = Insumo.query.all()
	return render_template("lista.html", insumos=insumos)

# compra de insumos
class Compra(db.Model):
	__tablename__  = 'compra'
	_id 		   = db.Column(db.Integer, primary_key = True, autoincrement = True)
	insumo    	   = db.Column(db.String)
	imovel         = db.Column(db.String)
	data 		   = db.Column(db.String)
	valor_unitario = db.Column(db.Float)
	valor_total    = db.Column(db.Float)

	def __init__(self, imovel,insumo,data,valor_unitario,valor_total):
		self.imovel	= imovel
		self.insumo = insumo
		self.data   = data
		self.valor_unitario = valor_unitario
		self.valor_total    = valor_total
db.create_all()

@app.route("/compra")
def compra_insumo():
	insumos = Insumo.query.all()
	imoveis = Imovel.query.all()
	return render_template("compra_insumo.html", insumos=insumos, imoveis=imoveis)

@app.route("/cadastro-compra", methods=['GET', 'POST'])
def adicionar_compra():
	if request.method == "POST":
		insumo = (request.form.get("insumo"))
		imovel = (request.form.get("imovel"))
		valor_unitario = (request.form.get("valor_unitario"))
		valor_total = (request.form.get("valor_total"))
		data = (request.form.get("data"))
		
		if data and valor_unitario and valor_total and insumo and imovel:
			compra = Compra(imovel,insumo,data,valor_unitario,valor_total)
			db.session.add(compra)
			db.session.commit()
	return redirect(url_for("home"))

@app.route("/lista-compra-insumo")
def lista_compra_insumo():
	compras = Compra.query.all()
	return render_template("lista_compra_insumo.html", compras=compras)	

@app.route("/excluir-compra-insumo/<int:id>")
def excluir_compra_insumo(id):
	compra = Compra.query.filter_by(_id=id).first()
	db.session.delete(compra)
	db.session.commit()

	compras = Compra.query.all()
	render_template("lista_compra_insumo.html", compras=compras)
	return redirect(url_for("lista_compra_insumo"))

@app.route("/atualizar-compra-insumo/<int:id>", methods=['GET', 'POST'])
def atualizar_compra_insumo(id):
	compra = Compra.query.filter_by(_id=id).first()
	insumos = Insumo.query.all()
	imoveis = Imovel.query.all()
	if request.method == "POST":
		insumo = (request.form.get("insumo"))
		imovel = (request.form.get("imovel"))
		valor_unitario = (request.form.get("valor_unitario"))
		valor_total = (request.form.get("valor_total"))
		data = (request.form.get("data"))
		
		if data and valor_unitario and valor_total and insumo and imovel:
			compra.imovel=imovel
			compra.insumo=insumo
			compra.data=data
			compra.valor_unitario=valor_unitario
			compra.valor_total=valor_total
			db.session.commit()
	return render_template("atualizar_compra_insumo.html",compra=compra,insumos=insumos,imoveis=imoveis)

@app.route("/insumo-imovel/<string:nome>")
def insumo_imovel(nome):
	compras = Compra.query.filter_by(imovel=nome).all()
	return render_template("lista_compra_insumo.html", compras=compras)
	
if __name__ == "__main__":
	app.run(debug=True)
