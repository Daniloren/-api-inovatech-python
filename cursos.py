from flask import Flask, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import json


app = Flask(__name__)


@app.route("/cursos", methods=["GET"])
def criarcurso():
    curso = request.form
    # return redirect(url_for("<crs>", crs=curso))
    return jsonify(curso)


@app.route("/cursos", methods=["POST"])
def criarcurso():
    curso = request.form
    # return redirect(url_for("<crs>", crs=curso))
    return jsonify(curso)


@app.route("/<crs>")
def user(crs):
    return f"<h1>{crs}</h1>"


if __name__ == "__main__":
    app.run(debug=True)
