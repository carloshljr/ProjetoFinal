# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 17:32:08 2016

@author: Carlosjunior
"""
from flask import Flask, render_template, request, redirect, url_for

class produto():
    
    #"Classe utilizada para armazenar os dados de um produto"
    
    def __init__(self,nomep,tipo,marca,data,local,observ,nomeu,codigo,email,telefone):
        self.nomep = nomep
        self.tipo = tipo
        self.marca = marca
        self.data = data
        self.local = local
        self.observ = observ
        self.nomeu = nomeu
        self.codigo = codigo
        self.email = email
        self.telefone = telefone
        

#Dicionario que irá armazenar os objetos da classe produto
#O codigo sera usada como chave

DB = {}

#instrucao para a inicializacao do Flask
app = Flask(__name__, static_url_path='')

@app.route('/')
def main():
	#A funcao abaixo vai ler e renderizar o arquivo HTML abaixo,
	#passando os parametros dic e erro. Por padrao, HTML nao sabe
	#interpretar codigo, mas foi adaptado para utilizacao e geracao
	#de conteudo dinamico.
	#Abrir e ler o arquivo em algum editor de texto.
    return render_template('Ifinder.html', dic = DB, erro = '')
    

#O endpoint abaixo ira tratar quando o usuario pedir a insercao
#de um item. Por padrao sera via POST de um formulario da pagina.
#novamente utiliza-se a variavel request para recuperar os dados.    
@app.route('/add', methods=['POST', 'GET'])
def add():
    
    #Tentar a insercao apenas quando vier via POST
    if request.method == 'POST':

        nomep = request.form['nomep']
        tipo = request.form['tipo']
        marca = request.form['marca']
        data = request.form['data']
        local = request.form['local']
        observ = request.form['observ']
        nomeu = request.form['nomeu']
        codigo = request.form['codigo']
        email = request.form['email']
        telefone = request.form['telefone']
        