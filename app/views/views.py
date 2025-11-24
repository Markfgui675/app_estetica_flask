from flask import request, redirect, url_for
from app import app
from app.model.model import init_db
from app.controller import limpeza, massagem, detox, ventosa, flacidez, endermo
from app.views.massagem import *
from app.views.limpeza import *
from app.views.detox import *
from app.views.endermo import *
from app.views.ventosa import *
from app.views.flacidez import *
from app.views.config import *

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
    elif tipo.lower() == 'Detox'.lower():
        detox.adicionar_cliente(nome)
        return redirect(url_for('homepage_detox'))
    elif tipo.lower() == 'Ventosa'.lower():
        ventosa.adicionar_cliente(nome)
        return redirect(url_for('homepage_ventosa'))
    elif tipo.lower() == 'Flacidez'.lower():
        flacidez.adicionar_cliente(nome)
        return redirect(url_for('homepage_flacidez'))
    elif tipo.lower() == 'Endermo'.lower():
        endermo.adicionar_cliente(nome)
        return redirect(url_for('homepage_endermo'))

