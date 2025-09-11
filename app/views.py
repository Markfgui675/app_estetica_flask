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
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        status_massagem BOOLEAN DEFAULT FALSE,
        status_limpeza BOOLEAN DEFAULT FALSE,
        checkins_massagem INTEGER DEFAULT 0,
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
    clientes = conn.execute('SELECT * FROM clientes').fetchall()
    conn.close()
    return render_template('index.html', clientes=clientes)

@app.route('/adicionar', methods=['POST'])
def adicionar_cliente():
    nome = request.form['nome']
    conn = get_db_connection()
    conn.execute("INSERT INTO clientes (nome, status_massagem, status_limpeza, checkins) VALUES (?, 0, 0, 0)", (nome,))
    conn.commit()
    conn.close()
    return redirect(url_for('homepage'))

@app.route('/checkin/<int:cliente_id>')
def registrar_checkin(cliente_id):
    conn = get_db_connection()
    cliente = conn.execute("SELECT * FROM clientes WHERE id = ?", (cliente_id,)).fetchone()
    status_massagem = False
    status_limpeza = False

    if cliente:
        novos_checkins = cliente['checkins'] + 1
        if novos_checkins >= 3:
            status_massagem = True  # Zera os checkins
            msg = "🎉 Cliente ganhou uma massagem!"
            if novos_checkins >= 4:
                status_limpeza = True
        
        if novos_checkins >= 5:
            novos_checkins = 0
            status_limpeza = False
            status_massagem = False
            msg = "✅ Check-in registrado!"
        
        conn.execute("UPDATE clientes SET checkins = ? WHERE id = ?", (novos_checkins, cliente_id))
        conn.execute("UPDATE clientes SET status_massagem = ? WHERE id = ?", (status_massagem,cliente_id))
        conn.execute("UPDATE clientes SET status_limpeza = ? WHERE id = ?", (status_limpeza,cliente_id))
        conn.execute("INSERT INTO checkins (cliente_id, data) VALUES (?, ?)",
                     (cliente_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
    conn.close()
    return redirect(url_for('homepage'))

@app.route('/checkinmassagem/<int:cliente_id>')
def registrar_checkin_massagem(cliente_id):
    conn = get_db_connection()
    cliente = conn.execute("SELECT * FROM clientes WHERE id = ?", (cliente_id,)).fetchone()
    status_massagem = False

    if cliente:
        novos_checkins = cliente['checkins'] + 1
        if novos_checkins >= 3:
            status_massagem = True
        else:
            novos_checkins = 0
            status_massagem = False
    
        conn.execute("UPDATE clientes SET checkins = ? WHERE id = ?", (novos_checkins, cliente_id))
        conn.execute("UPDATE clientes SET status_massagem = ? WHERE id = ?", (status_massagem,cliente_id))
        conn.execute("INSERT INTO checkins_massagem (cliente_id, data) VALUES (?, ?)",
                        (cliente_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
    conn.close()
    return redirect(url_for('homepage'))

@app.route('/teste')
def teste():
    conn = get_db_connection()
    cliente = conn.execute("SELECT * FROM clientes WHERE id = 1").fetchone()
    print(cliente['checkins'])
    print(cliente['status_massagem'])
    print(cliente['status_limpeza'])
    return "testizin"
