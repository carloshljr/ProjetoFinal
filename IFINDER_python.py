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
    return render_template('Ifind.html', dic = DB, erro = '')
    

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
        
         #Aqui uma pequena validacao dos dados inseridos.
        if codigo == '' or email == '' or nomep == '':
            e = 'A validação, o email e o nome do produto não podem estar vazios!' #Mensagem de erro
            return render_template('ifind.html', dic = DB, erro = e)
        elif nomep in DB:
            e = 'Objeto perdido já cadastrado!'  #Mensagem de erro
            return render_template('ifind.html', dic = DB, erro = e)            
        else:
            DB[nomep] = produto(nomep,tipo,marca,data,local,observ,codigo,email,telefone)
            
    #Caso for chamado via GET ou apos terminar a insercao:
    return redirect(url_for('ifind'))


#Comando necessario para iniciar a aplicacao. Como a aplicacao nao
#ira rodar no Spyder, durante a fase de desenvolvimento e 
#aconselhavel deixar o modo debug ligado. Desligar quando for realizar
#o deployment.
if __name__ == '__main__':
    app.run(debug=True, host= '0.0.0.0', port=5000)
