from flask import render_template, url_for, flash, request, redirect
from datetime import datetime
from app import app
from app.model.model import get_db_connection
from app.controller import massagem

@app.route("/")
def homepage_massagem():
    conn = get_db_connection()
    clientes_massagem = conn.execute('SELECT * FROM clientes_massagem ORDER BY nome ASC').fetchall()
    conn.close()
    return render_template('massagem/massagem.html', clientes_massagem=clientes_massagem)

@app.route('/clientemassagem/<int:cliente_id>')
def cliente_massagem(cliente_id):
    conn = get_db_connection()
    cliente = conn.execute("SELECT * FROM clientes_massagem WHERE id = ?", (cliente_id,)).fetchone()
    checkins = conn.execute("SELECT * FROM checkins_massagem1 WHERE cliente_id = ? ORDER BY data ASC", (cliente_id,))
    return render_template('massagem/cliente_massagem.html', cliente=cliente, checkins=checkins)

@app.route('/adcheckindatamassagem/<int:cliente_id>', methods=['GET', 'POST'])
def ad_checkin_massagem_data(cliente_id):
    conn = get_db_connection()
    agora = datetime.now().strftime("%d/%m/%Y")
    cliente = conn.execute("SELECT * FROM clientes_massagem WHERE id = ?", (cliente_id,)).fetchone()
    if request.method == 'POST':
        data_input = request.form['data_checkin'].strip()
        status_massagem = False
        try:

            novos_checkins = cliente['checkins_massagem'] + 1
            if novos_checkins >= 3:
                status_massagem = True
            
            if novos_checkins >= 4:
                status_massagem = False
                novos_checkins = 0
                massagem.zera_checkin(cliente_id)

            conn.execute(
                "INSERT INTO checkins_massagem1 (cliente_id, data) VALUES (?, ?)",
                (cliente_id, data_input)
            )
            conn.execute("UPDATE clientes_massagem SET checkins_massagem = ? WHERE id = ?", (novos_checkins, cliente_id))
            conn.execute("UPDATE clientes_massagem SET status_massagem = ? WHERE id = ?", (status_massagem,cliente_id))
            conn.commit()
            flash(f"Check-in adicionado para {cliente['nome']} em {data_input}", "success")
            conn.close()
            return redirect(url_for('homepage_massagem'))
        except ValueError:
            flash("Formato inválido! Use DD/MM/AAAA HH:MM", "warning")
    conn.close()
    return render_template('massagem/ch_data_massagem.html', cliente=cliente, agora=agora)

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
            massagem.zera_checkin(cliente_id)
        

        conn.execute("INSERT INTO checkins_massagem1 (cliente_id, data) VALUES (?, ?)",
                        (cliente_id, datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
        conn.execute("UPDATE clientes_massagem SET checkins_massagem = ? WHERE id = ?", (novos_checkins, cliente_id))
        conn.execute("UPDATE clientes_massagem SET status_massagem = ? WHERE id = ?", (status_massagem,cliente_id))
        conn.commit()
    conn.close()
    return redirect(url_for('homepage_massagem'))

@app.route("/excluir_massagem/<int:cliente_id>")
def excluir_massagem(cliente_id):
    massagem.excluir_cliente(cliente_id)
    return redirect(url_for("homepage_massagem"))

@app.route("/excluircheckinmassagem/<int:checkin_id>")
def excluir_ch_massagem(checkin_id):
    massagem.excluir_checkin(checkin_id)
    flash(f"Check-in removido!", "warning")
    return redirect(url_for("homepage_massagem"))
