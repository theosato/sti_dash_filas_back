from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import Column, Integer, DateTime
from flask_cors import CORS
import json 
import os
import datetime

app = Flask(__name__)
CORS(app)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'crud.sqlite')
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
    dataAtracao = db.Column(DateTime, default=datetime.datetime.utcnow)
    def __init__(self, nomeAtracao, quantPessoas, tempoFila, vazaoFila, duracaoFila, dataAtracao):
        self.nomeAtracao = nomeAtracao
        self.quantPessoas = quantPessoas
        self.tempoFila = tempoFila
        self.vazaoFila = vazaoFila
        self.duracaoFila = duracaoFila
        self.dataAtracao = dataAtracao
    def to_dict(self):
        response = {
            "id": self.idFila,
            "nome": self.nomeAtracao,
            "quantidade de pessoas": self.quantPessoas,
            "tempo de espera": self.tempoFila,
            "vazao": self.vazaoFila,
            "validade": self.duracaoFila,
            "data": self.dataAtracao
        }
        return response
################################################## S C H E M A ##################################################
class FilaSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('nomeAtracao', 'quantPessoas', 'tempoFila', 'vazaoFila', 'duracaoFila', 'dataAtracao')
fila_schema = FilaSchema()
filas_schema = FilaSchema(many=True)
################################################## R O U T E S ##################################################
# endpoint to create new line
@app.route("/fila", methods=["POST"])
def add_fila():
    nomeAtracao = request.json['nomeAtracao']
    quantPessoas = request.json['quantPessoas']
    tempoFila = request.json['tempoFila']
    vazaoFila = request.json['vazaoFila']
    duracaoFila = request.json['duracaoFila']
    dataAtracao = request.json['dataAtracao']
    new_fila = Fila(nomeAtracao, quantPessoas, tempoFila, vazaoFila, duracaoFila, dataAtracao)
    db.session.add(new_fila)
    db.session.commit()
    response = new_fila.to_dict()
    return response 
# endpoint to show all lines
@app.route("/fila", methods=["GET"])
def get_fila():
    all_filas = Fila.query.all()
    dict_result = {}
    for entry in all_filas:
        fila_dict = entry.to_dict()
        dict_result[fila_dict['idFila']] = fila_dict
    return json.loads(json.dumps(dict_result))
# endpoint to get line detail by id
@app.route("/fila/<id>", methods=["GET"])
def fila_detail(id):
    fila = Fila.query.get(id)
    response = fila.to_dict()
    return response 
# endpoint to update line
@app.route("/fila/<id>", methods=["PUT"])
def fila_update(id):
    fila = Fila.query.get(id)
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
    db.session.commit()
    return fila_schema.jsonify(fila)
# endpoint to delete line
@app.route("/fila/<id>", methods=["DELETE"])
def user_delete(id):
    fila = Fila.query.get(id)
    db.session.delete(fila)
    db.session.commit()
    return fila_schema.jsonify(fila)
############################################################################################################
if __name__ == '__main__':
    app.run(debug=True)