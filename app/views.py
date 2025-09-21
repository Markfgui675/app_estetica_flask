from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
from app import app

import sqlite3
from datetime import datetime

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
        checkins_limpeza INTEGER DEFAULT 0,
        historico_agendamento TEXT
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

def adicionar_cliente_limpeza(nome):
    conn = get_db_connection()
    conn.execute("INSERT INTO clientes_limpeza (nome, status_limpeza, checkins_limpeza) VALUES (?, 0, 0)", (nome,))
    conn.commit()
    conn.close()

def adicionar_cliente_massagem(nome):
    conn = get_db_connection()
    conn.execute("INSERT INTO clientes_massagem (nome, status_massagem, checkins_massagem) VALUES (?, 0, 0)", (nome,))
    conn.commit()
    conn.close()

def excluir_cliente_limpeza(cliente_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM clientes_limpeza WHERE id = ?", (cliente_id,))
    conn.execute("DELETE FROM checkins_limpeza WHERE cliente_id = ?", (cliente_id,))
    conn.commit()
    conn.close()

def excluir_cliente_massagem(cliente_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM clientes_massagem WHERE id = ?", (cliente_id,))
    conn.execute("DELETE FROM checkins_massagem WHERE cliente_id = ?", (cliente_id,))
    conn.commit()
    conn.close()

def excluir_checkin_massagem(checkin_id):
    conn = get_db_connection()
    cliente_id = conn.execute("SELECT * FROM checkins_massagem WHERE id = ?", (checkin_id,)).fetchone()['cliente_id']
    cliente = conn.execute("SELECT * FROM clientes_massagem WHERE id = ?", (cliente_id,)).fetchone()
    conn.execute("DELETE FROM checkins_massagem WHERE id = ?", (checkin_id,))
    novos_checkins = cliente['checkins_massagem'] - 1
    conn.execute("UPDATE clientes_massagem SET checkins_massagem = ? WHERE id = ?", (novos_checkins, cliente_id))
    conn.commit()
    conn.close()

def excluir_checkin_limpeza(checkin_id):
    conn = get_db_connection()
    cliente_id = conn.execute("SELECT * FROM checkins_limpeza WHERE id = ?", (checkin_id,)).fetchone()['cliente_id']
    cliente = conn.execute("SELECT * FROM clientes_limpeza WHERE id = ?", (cliente_id,)).fetchone()
    conn.execute("DELETE FROM checkins_limpeza WHERE id = ?", (checkin_id,))
    novos_checkins = cliente['checkins_limpeza'] - 1
    conn.execute("UPDATE clientes_limpeza SET checkins_limpeza = ? WHERE id = ?", (novos_checkins, cliente_id))
    conn.commit()
    conn.close()


@app.route("/")
def homepage_massagem():
    conn = get_db_connection()
    clientes_massagem = conn.execute('SELECT * FROM clientes_massagem').fetchall()
    conn.close()
    return render_template('massagem.html', clientes_massagem=clientes_massagem)

@app.route('/limpeza')
def homepage_limpeza():
    conn = get_db_connection()
    clientes_limpeza = conn.execute('SELECT * FROM clientes_limpeza').fetchall()
    conn.close()
    return render_template('limpeza.html',clientes_limpeza=clientes_limpeza)


@app.route('/adicionar', methods=['POST'])
def adicionar_cliente():
    nome = request.form['nome']
    tipo = request.form['servico']
    if tipo.lower() == 'Limpeza de pele'.lower():
        adicionar_cliente_limpeza(nome)
        return redirect(url_for('homepage_limpeza'))
    if tipo.lower() == 'Massagem'.lower():
        adicionar_cliente_massagem(nome)
        return redirect(url_for('homepage_massagem'))

@app.route('/clientemassagem/<int:cliente_id>')
def cliente_massagem(cliente_id):
    conn = get_db_connection()
    cliente = conn.execute("SELECT * FROM clientes_massagem WHERE id = ?", (cliente_id,)).fetchone()
    checkins = conn.execute("SELECT * FROM checkins_massagem WHERE cliente_id = ?", (cliente_id,))
    return render_template('cliente_massagem.html', cliente=cliente, checkins=checkins)

@app.route('/adcheckindatamassagem/<int:cliente_id>', methods=['GET', 'POST'])
def ad_checkin_massagem_data(cliente_id):
    conn = get_db_connection()
    agora = datetime.now().strftime("%d/%m/%Y")
    cliente = conn.execute("SELECT * FROM clientes_massagem WHERE id = ?", (cliente_id,)).fetchone()
    if request.method == 'POST':
        data_input = request.form['data_checkin'].strip()
        data = data_input.split('T')
        data_01 = data[0].split('-')
        data_01_x = []
        for x in reversed(data_01):
            data_01_x.append(x)
        data_f = ""
        for i in range(len(data_01_x)):
            if i+1>=len(data_01_x):
                data_f+=data_01_x[i]
                break
            data_f+=f'{data_01_x[i]}/'
        data_input = f'{data_f} {data[1]}'
        try:
            #Valida e formata a data
            data_formatada = datetime.strptime(data_input, "%d/%m/%Y %H:%M")
            data_str = data_formatada.strftime("%d/%m/%Y %H:%M:%S")

            novos_checkins = cliente['checkins_massagem'] + 1

            conn.execute(
                "INSERT INTO checkins_massagem (cliente_id, data) VALUES (?, ?)",
                (cliente_id, data_str)
            )
            conn.execute("UPDATE clientes_massagem SET checkins_massagem = ? WHERE id = ?", (novos_checkins, cliente_id))
            conn.commit()
            flash(f"Check-in adicionado para {cliente['nome']} em {data_str}", "success")
            conn.close()
            return redirect(url_for('homepage_massagem'))
        except ValueError:
            flash("Formato inválido! Use DD/MM/AAAA HH:MM", "warning")
    conn.close()
    return render_template('ch_data_massagem.html', cliente=cliente, agora=agora)
    


@app.route('/clientelimpeza/<int:cliente_id>')
def cliente_limpeza(cliente_id):
    conn = get_db_connection()
    cliente = conn.execute("SELECT * FROM clientes_limpeza WHERE id = ?", (cliente_id,)).fetchone()
    checkins = conn.execute("SELECT * FROM checkins_limpeza WHERE cliente_id = ?", (cliente_id,))
    return render_template('cliente_limpeza.html', cliente=cliente, checkins=checkins)

@app.route('/adcheckindatalimpeza/<int:cliente_id>', methods=['GET', 'POST'])
def ad_checkin_limpeza_data(cliente_id):
    conn = get_db_connection()
    agora = datetime.now().strftime("%d/%m/%Y")
    cliente = conn.execute("SELECT * FROM clientes_limpeza WHERE id = ?", (cliente_id,)).fetchone()
    if request.method == 'POST':
        data_input = request.form['data_checkin'].strip()
        data = data_input.split('T')
        data_01 = data[0].split('-')
        data_01_x = []
        for x in reversed(data_01):
            data_01_x.append(x)
        data_f = ""
        for i in range(len(data_01_x)):
            if i+1>=len(data_01_x):
                data_f+=data_01_x[i]
                break
            data_f+=f'{data_01_x[i]}/'
        data_input = f'{data_f} {data[1]}'
        try:
            #Valida e formata a data
            data_formatada = datetime.strptime(data_input, "%d/%m/%Y %H:%M")
            data_str = data_formatada.strftime("%d/%m/%Y %H:%M:%S")

            novos_checkins = cliente['checkins_limpeza'] + 1

            conn.execute(
                "INSERT INTO checkins_limpeza (cliente_id, data) VALUES (?, ?)",
                (cliente_id, data_str)
            )
            conn.execute("UPDATE clientes_limpeza SET checkins_limpeza = ? WHERE id = ?", (novos_checkins, cliente_id))
            conn.commit()
            flash(f"Check-in adicionado para {cliente['nome']} em {data_str}", "success")
            conn.close()
            return redirect(url_for('homepage_limpeza'))
        except ValueError:
            flash("Formato inválido! Use DD/MM/AAAA HH:MM", "warning")
    conn.close()
    return render_template('ch_data_limpeza.html', cliente=cliente, agora=agora)


@app.route('/checkinmassagem/<int:cliente_id>')
def registrar_checkin_massagem(cliente_id):
    conn = get_db_connection()
    cliente = conn.execute("SELECT * FROM clientes_massagem WHERE id = ?", (cliente_id,)).fetchone()
    status_massagem = False

    if cliente:

        hoje = datetime.now().strftime("%d/%m/%Y")

        checkin_existente = conn.execute('''SELECT * FROM checkins_massagem WHERE cliente_id = ? AND data LIKE ?''', (cliente_id, f"{hoje}%")).fetchone()

        if checkin_existente:
            flash(f"O cliente {cliente['nome']} já fez check-in hoje!", "warning")
            conn.close()
            return redirect(url_for('homepage_massagem'))
        
        novos_checkins = cliente['checkins_massagem'] + 1
        if novos_checkins >= 3:
            status_massagem = True
        
        if novos_checkins >= 4:
            status_massagem = False
            novos_checkins = 0

    
        conn.execute("UPDATE clientes_massagem SET checkins_massagem = ? WHERE id = ?", (novos_checkins, cliente_id))
        conn.execute("UPDATE clientes_massagem SET status_massagem = ? WHERE id = ?", (status_massagem,cliente_id))
        conn.execute("INSERT INTO checkins_massagem (cliente_id, data) VALUES (?, ?)",
                        (cliente_id, datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
        conn.commit()
    conn.close()
    return redirect(url_for('homepage_massagem'))

@app.route('/checkinlimpeza/<int:cliente_id>')
def registrar_checkin_limpeza(cliente_id):
    conn = get_db_connection()
    cliente = conn.execute("SELECT * FROM clientes_limpeza WHERE id = ?", (cliente_id,)).fetchone()
    status_limpeza = False

    if cliente:

        hoje = datetime.now().strftime("%d/%m/%Y")

        checkin_existente = conn.execute('''SELECT * FROM checkins_limpeza WHERE cliente_id = ? AND data LIKE ?''', (cliente_id, f"{hoje}%")).fetchone()

        if checkin_existente:
            flash(f"O cliente {cliente['nome']} já fez check-in hoje!", "warning")
            conn.close()
            return redirect(url_for('homepage_limpeza'))
        
        novos_checkins = cliente['checkins_limpeza'] +1
        if novos_checkins >= 4:
            status_limpeza = True
        
        if novos_checkins >= 5:
            status_limpeza = False
            novos_checkins = 0
        
        conn.execute("UPDATE clientes_limpeza SET checkins_limpeza = ? WHERE id = ?", (novos_checkins, cliente_id))
        conn.execute("UPDATE clientes_limpeza SET status_limpeza = ? WHERE id = ?", (status_limpeza,cliente_id))
        conn.execute("INSERT INTO checkins_limpeza (cliente_id, data) VALUES (?, ?)",
                        (cliente_id, datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
        conn.commit()
    conn.close()
    return redirect(url_for('homepage_limpeza'))


@app.route("/excluir_massagem/<int:cliente_id>")
def excluir_massagem(cliente_id):
    excluir_cliente_massagem(cliente_id)
    return redirect(url_for("homepage_massagem"))

@app.route("/excluir_limpeza/<int:cliente_id>")
def excluir_limpeza(cliente_id):
    excluir_cliente_limpeza(cliente_id)
    return redirect(url_for("homepage_limpeza"))



#função que remove check-in de cliente massagem
@app.route("/excluircheckinmassagem/<int:checkin_id>")
def excluir_ch_massagem(checkin_id):
    excluir_checkin_massagem(checkin_id)
    flash(f"Check-in removido!", "warning")
    return redirect(url_for("homepage_massagem"))

#função que remove check-in de cliente limpeza
@app.route("/excluircheckinlimpeza/<int:checkin_id>")
def excluir_ch_limpeza(checkin_id):
    excluir_checkin_limpeza(checkin_id)
    flash(f"Check-in removido!", "warning")
    return redirect(url_for("homepage_limpeza"))

