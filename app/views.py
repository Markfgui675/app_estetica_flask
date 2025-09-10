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
        checkins INTEGER DEFAULT 0
    )
    ''')
    conn.execute('''
    CREATE TABLE IF NOT EXISTS historico_checkins (
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
    conn.execute("INSERT INTO clientes (nome, checkins) VALUES (?, 0)", (nome,))
    conn.commit()
    conn.close()
    return redirect(url_for('homepage'))

@app.route('/checkin/<int:cliente_id>')
def registrar_checkin(cliente_id):
    conn = get_db_connection()
    cliente = conn.execute("SELECT * FROM clientes WHERE id = ?", (cliente_id,)).fetchone()

    if cliente:
        novos_checkins = cliente['checkins'] + 1
        if novos_checkins >= 4:
            novos_checkins = 0  # Zera os checkins
            msg = "🎉 Cliente ganhou uma massagem!"
        else:
            msg = "✅ Check-in registrado!"
        
        conn.execute("UPDATE clientes SET checkins = ? WHERE id = ?", (novos_checkins, cliente_id))
        conn.execute("INSERT INTO historico_checkins (cliente_id, data) VALUES (?, ?)",
                     (cliente_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
    conn.close()
    return redirect(url_for('homepage'))
