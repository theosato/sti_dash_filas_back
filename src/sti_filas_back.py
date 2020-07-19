from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import Column, Integer, DateTime
from flask_cors import CORS
import json 
import os
import datetime
import requests

app = Flask(__name__)
cors = CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'crud.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'False'

db = SQLAlchemy(app)
ma = Marshmallow(app)

################################################## M O D E L S ##################################################
class Fila(db.Model):
    __tablename__ = 'filas'
    idFila = db.Column(db.Integer, primary_key=True)
    nomeAtracao = db.Column(db.String(80), unique=False)
    quantPessoas = db.Column(db.String(30), unique=False)
    tempoFila = db.Column(db.String(30), unique=False)
    vazaoFila = db.Column(db.String(30), unique=False)
    duracaoFila = db.Column(db.String(30), unique=False)
    dataAtracao = db.Column(db.String(80), default=datetime.datetime.utcnow)
    filaAtiva = db.Column(db.String(2), unique=False)

    def __init__(self, nomeAtracao, quantPessoas, tempoFila, vazaoFila, duracaoFila, dataAtracao, filaAtiva):
        self.nomeAtracao = nomeAtracao
        self.quantPessoas = quantPessoas
        self.tempoFila = tempoFila
        self.vazaoFila = vazaoFila
        self.duracaoFila = duracaoFila
        self.dataAtracao = dataAtracao
        self.filaAtiva = filaAtiva

################################################## S C H E M A ##################################################
class FilaSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('idFila', 'nomeAtracao', 'quantPessoas', 'tempoFila', 'vazaoFila', 'duracaoFila', 'dataAtracao', 'filaAtiva')

fila_schema = FilaSchema()
filas_schema = FilaSchema(many=True)

################################################## R O U T E S ##################################################
@app.route("/")
def homepage():
    text = "Este eh o backend do sistema de filas do Sem Tempo, Irmão. Voce pode acessar os endpoints aqui descritos."

    response = {
        "status_code": 200,
        "message": text,
        "/fila [POST]": "adiciona uma fila ao evento",
        "/fila [GET]": "retorna as informações de todas as filas de um evento",
        "/fila/<id> [GET]": "retorna as informações da fila com o id especificado",
        "/fila/<id> [PUT]": "atualiza as informações da fila com o id especificado",
        "/fila/<id> [DELETE]": "deleta a fila com o id especificado",
    } 
    return jsonify(response)


# endpoint to create new line
@app.route("/fila", methods=['POST'])
def add_fila():
    if request.method == 'POST':
        nomeAtracao = request.json['nomeAtracao']
        quantPessoas = request.json['quantPessoas']
        tempoFila = request.json['tempoFila']
        vazaoFila = request.json['vazaoFila']
        duracaoFila = request.json['duracaoFila']
        dataAtracao = request.json['dataAtracao']
        filaAtiva = "0"

        new_fila = Fila(nomeAtracao, quantPessoas, tempoFila, vazaoFila, duracaoFila, dataAtracao, filaAtiva)
        db.session.add(new_fila)
        db.session.commit()

        response = fila_schema.dump(new_fila)
        print("\n \n \n \n")
        print(response,type(response))
        print("\n \n \n \n")
        
        return jsonify(response)

# endpoint to show all lines
@app.route("/fila", methods=['GET'])
def get_fila():
    if request.method == 'GET':
        all_filas = Fila.query.all()
        
        response = filas_schema.dump(all_filas)
        
        return jsonify(response)

# endpoint to get line detail by id
@app.route("/fila/<id>", methods=["GET"])
def fila_detail(id):
    if request.method == 'GET':
        fila = Fila.query.get(id)
        response = fila_schema.dump(fila)

        return jsonify(response)

# endpoint to update line
@app.route("/fila/<id>", methods=["PUT"])
def fila_update(id):
    if request.method == 'PUT':

        fila = Fila.query.get(id)

        if fila is not None:
            if 'nomeAtracao' in request.json.keys():
                fila.nomeAtracao = request.json['nomeAtracao']
            if 'quantPessoas' in request.json.keys():
                fila.quantPessoas = request.json['quantPessoas']
            if 'tempoFila' in request.json.keys():
                fila.tempoFila = request.json['tempoFila']
            if 'vazaoFila' in request.json.keys():
                fila.vazaoFila = request.json['vazaoFila']
            if 'duracaoFila' in request.json.keys():
                fila.duracaoFila = request.json['duracaoFila']
            if 'dataAtracao' in request.json.keys():
                fila.dataAtracao = request.json['dataAtracao']
            if 'filaAtiva' in request.json.keys():
                fila.filaAtiva = request.json['filaAtiva']
            
            db.session.commit()

            return fila_schema.jsonify(fila)

        return None

# endpoint to delete line
@app.route("/fila/<id>", methods=["DELETE"])
def fila_delete(id):
    if request.method == 'DELETE':
        fila = Fila.query.get(id)
        db.session.delete(fila)
        db.session.commit()

        return fila_schema.jsonify(fila)


############################################################################################################

if __name__ == '__main__':
    app.run(debug=True)