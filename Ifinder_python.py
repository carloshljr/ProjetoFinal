# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 17:32:08 2016

@author: Carlosjunior
"""
from flask import Flask, render_template, request, redirect, url_for

import firecall



from datetime import datetime

class Produto():
    
    #"Classe utilizada para armazenar os dados de um produto"
    
    def __init__(self,dt, nomep,tipo,marca,data,local,observ,codigo,email,telefone):
        self.dt = dt
        self.nomep = nomep
        self.tipo = tipo
        self.marca = marca
        self.data = data
        self.local = local
        self.observ = observ
        self.codigo = codigo
        self.email = email
        self.telefone = telefone
        
    def Salvar(self):
        prod = {}
        prod[self.nomep]= self.dt,self.nomep, self.tipo, self.marca, self.data, self.local, self.observ, self.codigo, self.email, self.telefone
        
        my_firebase = firecall.Firebase("https://ifind.firebaseio.com/")
        my_firebase.put_sync(point = '/Produto/{0}'.format(self.dt) , data = prod)
        
    def Listar(self):
        
        pass
        

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
    #Deve verificar o firebase, e mostrar o produtos no servidor
    
    #"""for i in range(len(dicionario)):
       # produto = my_firebase.get.sync(point = '/Produto/{0}'.format(self.dt) , data = prod)#puxar do firebase o produto #puxar do firebase todos os produtos
       # dt = produto.dt
       # nomep = produto.nomep
       # tipo = produto.tipo
       # marca = produto.marca
       # data = produto.data
       # local = produto.local
       # observ = produto.observ
       # codigo = produto.codigo
       # email = produto.email
       # telefone = produto.telefone"""
    


    return render_template('ifind.html', dic = DB, erro = '')
    

#O endpoint abaixo ira tratar quando o usuario pedir a insercao
#de um item. Por padrao sera via POST de um formulario da pagina.
#novamente utiliza-se a variavel request para recuperar os dados.    
@app.route('/add', methods=['POST', 'GET'])
def add():
    
    #Tentar a insercao apenas quando vier via POST
    if request.method == 'POST':
    
        nomep = request.form['Nome']
        tipo = request.form['Tipo']
        marca = request.form['Marca']
        data = request.form['Data']
        local = request.form['Local']
        observ = request.form['Observacoes']
        codigo = request.form['Codigo']
        email = request.form['Email']
        telefone = request.form['Telefone']
        dt = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
        
         #Aqui uma pequena validacao dos dados inseridos.
        if codigo == '': 
            e = 'A validação, o email e o nome do produto não podem estar vazios!' #Mensagem de erro
            return render_template('ifind.html', dic = DB, erro = e)
        elif codigo in DB:
            e = 'Objeto perdido já cadastrado! Porfavor use outro codigo de validação'  #Mensagem de erro
            return render_template('ifind.html', dic = DB, erro = e)            
        else:
            DB[dt] = Produto(dt, nomep,tipo,marca,data,local,observ,codigo,email,telefone)
            DB[dt].Salvar()
    #Caso for chamado via GET ou apos terminar a insercao:
    return redirect(url_for('main'))
@app.route('/produto', methods = ['POST', 'GET'])
def abrir_produto():
    return render_template('ifind,3.html', dic = DB, erro = '')

@app.route('/verifica', methods=['POST', 'GET'])
def verificacao():
    if request.method == 'POST':

        codigov = request.args['CodigoV']
        dt = request.args['dt']#puxar do html o dt
        nomep = request.form.get('Nome')
        my_firebase = firecall.Firebase("https://ifind.firebaseio.com/")
        my_firebase.get_sync(point = '/Produto/{0}/{1}/{2}'.format(dt,nomep,Produto.codigo))

        #validacao dos dados inseridos

        if codigov == Produto.codigo:
            #liberar o email da pessoa que achou
            my_firebase.get_sync(point = '/Produto/{0}/{1}/{2}'.format(dt,nomep,Produto.email))
        else:
            e = 'O codigo que vc inseriu não confere! Por favor tente novamente.'
    return redirect(url_for('abrir_produto'))
#Comando necessario para iniciar a aplicacao. Como a aplicacao nao
#ira rodar no Spyder, durante a fase de desenvolvimento e 
#aconselhavel deixar o modo debug ligado. Desligar quando for realizar
#o deployment.
if __name__ == '__main__':
    app.run(debug=True, host= '0.0.0.0', port=5320)
