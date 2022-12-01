from flask import Flask, request, Response, jsonify
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:123456@localhost:5433/postgres" #Acesso Local

db = SQLAlchemy(app)

class Cursos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200))
    categoria = db.Column(db.String(200))
    
    def to_json(self):
        return {"id": self.id, "nome": self.nome, "categoria": self.categoria}

#Selecionar um
@app.route("/cursos", methods=["GET"])
def buscarcurso():
   
    cursos_classe = Cursos.query.all()
    cursos_json = [cursos.to_json() for cursos in cursos_classe]
    
    return gera_response(200, "cursos", cursos_json)

@app.route("/cursos/<id>", methods=["GET"])
def selecionar_curso(id):
    
    cursos_classe = Cursos.query.filter_by(id=id).first()
    cursos_json = cursos_classe.to_json()
    
    return gera_response(200, "cursos", cursos_json)

#Cadastrar
@app.route("/cursos", methods=["POST"])
def criarcurso():
    body = request.get_json()
    
    try:
        cursos = Cursos(nome=body["nome"], categoria= body["categoria"])
        db.session.add(cursos) 
        db.session.commit()
        return gera_response(201, "cursos", cursos.to_json(), "Criado com sucesso")
    except Exception as e:
        print('Erro', e)  
        return gera_response(400, "curso", {}, "Erro ao cadastrar")
    
    #Atualizar
@app.route("/cursos/<id>", methods=["PUT"])
def atualiza_curso(id):
    cursos_classe = Cursos.query.filter_by(id=id).first()
    body = request.get_json()
    
    try:
        if('nome' in body):
            cursos_classe.nome = body['nome']
        if('categoria' in body):
            cursos_classe.categoria = body['categoria']
        
        db.session.add(cursos_classe)
        db.session.commit()
        return gera_response(200, "cursos", cursos_classe.to_json(), "Atualizado com sucesso")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "cursos", {}, "Erro ao atualizar")
    
    # Deletar
@app.route("/cursos/<id>", methods=["DELETE"])
def deleta_curso(id):
    cursos_classe = Cursos.query.filter_by(id=id).first()

    try:
        db.session.delete(cursos_classe)
        db.session.commit()
        return gera_response(200, "cursos", cursos_classe.to_json(), "Deletado com sucesso")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "cursos", {}, "Erro ao deletar")

#função para mostrar conteúdo. Mensagem=false pq não é obrigatória 
def gera_response(status, nome_do_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_do_conteudo] = conteudo

    if(mensagem):
        body["mensagem"] = mensagem

    return Response(json.dumps(body), status=status, mimetype="application/json")

    

    
    
    #return Response(cursos_json)
    # return redirect(url_for("<crs>", crs=curso))
    #return jsonify(curso)
    
def gera_response(status, nome_do_conteudo, conteudo, mensagem=False):    
    body = {}
    body[nome_do_conteudo] = conteudo
    
    if(mensagem):
        body["mensagem"] = mensagem
    return Response(json.dumps(body), status=status, mimetype="application/json")
   
        


    
    #categoria = request.form[categoria]
    # return redirect(url_for("<crs>", crs=curso))
    return jsonify(curso)


@app.route("/<crs>")
def user(crs):
    return f"<h1>{crs}</h1>"


if __name__ == "__main__":
    app.run(debug=True)
