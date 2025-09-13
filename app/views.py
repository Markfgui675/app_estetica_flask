from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime
from app import app

# Função para conexão com banco
def get_db_connection():
    conn = sqlite3.connect('checkins.db')
    conn.row_factory = sqlite3.Row
    return conn

# Criação das tabelas
def init_db():
    conn = get_db_connection()

    conn.execute('''
    CREATE TABLE IF NOT EXISTS clientes_massagem (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        status_massagem BOOLEAN DEFAULT FALSE,
        checkins_massagem INTEGER DEFAULT 0
    )
    ''')

    conn.execute('''
    CREATE TABLE IF NOT EXISTS clientes_limpeza (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        status_limpeza BOOLEAN DEFAULT FALSE,
        checkins_limpeza INTEGER DEFAULT 0
    )
    ''')

    conn.execute('''
    CREATE TABLE IF NOT EXISTS checkins_massagem (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER,
        data TEXT,
        FOREIGN KEY(cliente_id) REFERENCES clientes(id)
    )
    ''')

    conn.execute('''
    CREATE TABLE IF NOT EXISTS checkins_limpeza (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER,
        data TEXT,
        FOREIGN KEY(cliente_id) REFERENCES clientes(id)
    )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def homepage():
    conn = get_db_connection()
    clientes_massagem = conn.execute('SELECT * FROM clientes_massagem').fetchall()
    clientes_limpeza = conn.execute('SELECT * FROM clientes_limpeza').fetchall()
    conn.close()
    return render_template('index.html', clientes_massagem=clientes_massagem, clientes_limpeza=clientes_limpeza)

@app.route('/adicionar', methods=['POST'])
def adicionar_cliente():
    nome = request.form['nome']
    conn = get_db_connection()
    conn.execute("INSERT INTO clientes_limpeza (nome, status_limpeza, checkins_limpeza) VALUES (?, 0, 0)", (nome,))
    conn.commit()
    conn.close()
    return redirect(url_for('homepage'))

    #modificar forma de registro de clientes

@app.route('/checkinmassagem/<int:cliente_id>')
def registrar_checkin_massagem(cliente_id):
    conn = get_db_connection()
    cliente = conn.execute("SELECT * FROM clientes_massagem WHERE id = ?", (cliente_id,)).fetchone()
    status_massagem = False

    if cliente:
        novos_checkins = cliente['checkins_massagem'] + 1
        if novos_checkins >= 3:
            status_massagem = True
        
        if novos_checkins >= 4:
            status_massagem = False
            novos_checkins = 0

    
        conn.execute("UPDATE clientes_massagem SET checkins_massagem = ? WHERE id = ?", (novos_checkins, cliente_id))
        conn.execute("UPDATE clientes_massagem SET status_massagem = ? WHERE id = ?", (status_massagem,cliente_id))
        conn.execute("INSERT INTO checkins_massagem (cliente_id, data) VALUES (?, ?)",
                        (cliente_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
    conn.close()
    return redirect(url_for('homepage'))

@app.route('/checkinlimpeza/<int:cliente_id>')
def registrar_checkin_limpeza(cliente_id):
    conn = get_db_connection()
    cliente = conn.execute("SELECT * FROM clientes_limpeza WHERE id = ?", (cliente_id,)).fetchone()
    status_limpeza = False

    if cliente:
        novos_checkins = cliente['checkins_limpeza'] +1
        if novos_checkins >= 4:
            status_limpeza = True
        
        if novos_checkins >= 5:
            status_limpeza = False
            novos_checkins = 0
        
        conn.execute("UPDATE clientes_limpeza SET checkins_limpeza = ? WHERE id = ?", (novos_checkins, cliente_id))
        conn.execute("UPDATE clientes_limpeza SET status_limpeza = ? WHERE id = ?", (status_limpeza,cliente_id))
        conn.execute("INSERT INTO checkins_limpeza (cliente_id, data) VALUES (?, ?)",
                        (cliente_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
    conn.close()
    return redirect(url_for('homepage'))

