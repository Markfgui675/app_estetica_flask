from flask import render_template, url_for, flash, request, redirect
from datetime import datetime
from app import app
from app.model.model import get_db_connection
from app.controller import detox


@app.route("/detox")
def homepage_detox():
    conn = get_db_connection()
    cliente_detox = conn.execute('SELECT * FROM cliente_detox ORDER BY nome ASC').fetchall()
    conn.close()
    return render_template('detox/detox.html', cliente_detox=cliente_detox)

@app.route('/clientedetox/<int:cliente_id>')
def cliente_detox(cliente_id):
    conn = get_db_connection()
    cliente = conn.execute("SELECT * FROM cliente_detox WHERE id = ?", (cliente_id,)).fetchone()
    checkins = conn.execute("SELECT * FROM checkin_detox WHERE cliente_id = ? ORDER BY data DESC", (cliente_id,))
    return render_template('detox/cliente_detox.html', cliente=cliente, checkins=checkins)

@app.route('/adcheckindatadetox/<int:cliente_id>', methods=['GET', 'POST'])
def ad_checkin_detox_data(cliente_id):
    conn = get_db_connection()
    agora = datetime.now().strftime("%d/%m/%Y")
    cliente = conn.execute("SELECT * FROM cliente_detox WHERE id = ?", (cliente_id,)).fetchone()
    if request.method == 'POST':
        data_input = request.form['data_checkin'].strip()
        status = False
        try:

            novos_checkins = cliente['checkins'] + 1
            if novos_checkins >= 3:
                status = True
            
            if novos_checkins >= 4:
                status = False
                novos_checkins = 0
                detox.zera_checkin(cliente_id)

            conn.execute(
                "INSERT INTO checkin_detox (cliente_id, data) VALUES (?, ?)",
                (cliente_id, data_input)
            )
            conn.execute("UPDATE cliente_detox SET checkins = ? WHERE id = ?", (novos_checkins, cliente_id))
            conn.execute("UPDATE cliente_detox SET status = ? WHERE id = ?", (status,cliente_id))
            conn.commit()
            flash(f"Check-in adicionado para {cliente['nome']} em {data_input}", "success")
            conn.close()
            return redirect(url_for('homepage_detox'))
        except ValueError:
            flash("Formato inválido! Use DD/MM/AAAA HH:MM", "warning")
    conn.close()
    return render_template('detox/ch_data_detox.html', cliente=cliente, agora=agora)

@app.route('/checkindetox/<int:cliente_id>')
def registrar_checkin_detox(cliente_id):
    conn = get_db_connection()
    cliente = conn.execute("SELECT * FROM cliente_detox WHERE id = ?", (cliente_id,)).fetchone()
    status = False

    if cliente:
        
        
        novos_checkins = cliente['checkins'] +1
        if novos_checkins >= 3:
            status = True
        
        if novos_checkins >= 4:
            status = False
            novos_checkins = 0
            detox.zera_checkin(cliente_id)
        
        conn.execute("UPDATE cliente_detox SET checkins = ? WHERE id = ?", (novos_checkins, cliente_id))
        conn.execute("UPDATE cliente_detox SET status = ? WHERE id = ?", (status,cliente_id))
        conn.execute("INSERT INTO checkin_detox (cliente_id, data) VALUES (?, ?)",
                        (cliente_id, datetime.now()))
        conn.commit()
    conn.close()
    return redirect(url_for('homepage_detox'))

@app.route("/excluir_detox/<int:cliente_id>")
def excluir_detox(cliente_id):
    detox.excluir_cliente(cliente_id)
    return redirect(url_for("homepage_detox"))

@app.route("/excluircheckindetox/<int:checkin_id>")
def excluir_ch_detox(checkin_id):
    detox.excluir_checkin(checkin_id)
    flash(f"Check-in removido!", "warning")
    return redirect(url_for("homepage_detox"))
