from flask import render_template, request, redirect, url_for, flash
from datetime import datetime
from app import app
from app.model.model import get_db_connection, init_db
from app.controller import limpeza, massagem
from app.views.massagem import *
from app.views.limpeza import *

init_db()


@app.route('/adicionar', methods=['POST'])
def adicionar_cliente():
    nome = request.form['nome']
    tipo = request.form['servico']
    if tipo.lower() == 'Limpeza de pele'.lower():
        limpeza.adicionar_cliente(nome)
        return redirect(url_for('homepage_limpeza'))
    elif tipo.lower() == 'Massagem'.lower():
        massagem.adicionar_cliente(nome)
        return redirect(url_for('homepage_massagem'))


