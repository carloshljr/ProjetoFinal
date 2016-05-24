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
    

        
def lista_produto():
    #Criando os produtos que ja estavam no firebase 
    my_firebase = firecall.Firebase("https://ifind.firebaseio.com/")
    prod = eval(my_firebase.get_sync(point = '/Produto'))
    #print(len(prod),prod)       
    Total = []
    for i in prod.values():
        #print(i)
        for e in i.values():
            #print(e)
            informacoes = []
            for x in e:
                informacoes.append(x)
            produto = Produto(informacoes[0],informacoes[1],informacoes[2],informacoes[3],informacoes[4],informacoes[5],informacoes[6],informacoes[7],informacoes[8],informacoes[9])
            Total.append(produto)
                
    return Total
        #Adicionando o produto na lista do DB

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
#Criando os produtos que ja estavam no firebase 
    my_firebase = firecall.Firebase("https://ifind.firebaseio.com/")
    prod = my_firebase.get_sync(point = '/Produto')
    #print(len(prod),prod)
    if prod == b'null':
        Total = []
    else:
        prod = eval(prod)        
        Total = []
        for i in prod.values():
            #print(i)
            for e in i.values():
                #print(e)
                informacoes = []
                for x in e:
                    informacoes.append(x)
                produto = Produto(informacoes[0],informacoes[1],informacoes[2],informacoes[3],informacoes[4],informacoes[5],informacoes[6],informacoes[7],informacoes[8],informacoes[9])
                Total.append(produto)

    
    
    for i in Total:
        nomep = i.nomep
        
        DB[nomep]=i
        

    return render_template('ifind.html', dic = DB, erro = '')
    

#O endpoint abaixo ira tratar quando o usuario pedir a insercao
#de um item. Por padrao sera via POST de um formulario da pagina.
#novamente utiliza-se a variavel request para recuperar os dados.    
@app.route('/add', methods=['POST', 'GET'])
def add():
    # print(0)
    #Tentar a insercao apenas quando vier via POST
    if request.method == 'POST':
        # print(1)
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
            # print(2)
            return render_template('ifind.html', dic = DB, erro = e)
        elif codigo in DB:
            e = 'Objeto perdido já cadastrado! Porfavor use outro codigo de validação'  #Mensagem de erro
            # print(3)
            return render_template('ifind.html', dic = DB, erro = e)            
        else:
            # print(4)
            Produto1 = Produto(dt, nomep,tipo,marca,data,local,observ,codigo,email,telefone)
            Produto1.Salvar()
    #Caso for chamado via GET ou apos terminar a insercao:
    # print(11)
    return redirect(url_for('main'))
@app.route('/produto/', methods = ['POST', 'GET'])
def abrir_produto():
    dt = request.args['dt']

    
    my_firebase = firecall.Firebase("https://ifind.firebaseio.com/")


    prod = eval(my_firebase.get_sync(point = '/Produto/{0}'.format(dt)))
    
        #Converter de prod (dicionario) para obj da classe produto
    D=[]
    for e in prod.values():
        for i in e:
            D.append(i)
    
    objet = Produto(D[0],D[1],D[2],D[3],D[4],D[5],D[6],D[7],D[8],D[9])
    # print(0)
    #Tentar a insercao apenas quando vier via POST
    # if request.method == 'GET':
    # #Caso for chamado via GET ou apos terminar a insercao:
    #     print(11)
    #     return render_template('ifind3.html', obj= objet, erro = '')
    # else:
    #     print(1)
    #     codigov = request.form['CodigoV']
    #      #Aqui uma pequena validacao dos dados inseridos.
    #     if codigoV != codigo: 
    #         e = error = 'O codigo de verificação que você inseriu não bate com os dos nossos dados. Porfavor tente novamente' #Mensagem de erro
    #         print(2)
    #         return render_template('ifind3.html', obj= objet, erro = e)          


    return render_template('ifind3.html', obj= objet, erro = '')
@app.route('/produto/verifica', methods=['POST', 'GET'])
def mostrar_contato():

    dt = request.args['dt']        
    my_firebase = firecall.Firebase("https://ifind.firebaseio.com/")
    prod = eval(my_firebase.get_sync(point = '/Produto/{0}'.format(dt)))

    #Converter de prod (dicionario) para obj da classe produto
    D=[]
    for e in prod.values():
        for i in e:
            D.append(i)
    objet = Produto(D[0],D[1],D[2],D[3],D[4],D[5],D[6],D[7],D[8],D[9])
    if request.method == 'POST':
        print(1)
        codigov = request.form['CodigoV']
         #Aqui uma pequena validacao dos dados inseridos.
        if codigoV == codigo: 
            print(2)
            return render_template('ifind4.html', obj= objet) 
    else:
        e = 'O codigo de verificação que você inseriu não bate com os dos nossos dados. Porfavor tente novamente' #Mensagem de erro
        print(objet)
        return render_template('ifind3.html', obj= objet, erro = e)
#Comando necessario para iniciar a aplicacao. Como a aplicacao nao
#ira rodar no Spyder, durante a fase de desenvolvimento e 
#aconselhavel deixar o modo debug ligado. Desligar quando for realizar
#o deployment.
if __name__ == '__main__':
    app.run(debug=True, host= '0.0.0.0', port=5321)
