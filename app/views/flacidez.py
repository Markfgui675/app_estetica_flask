from flask import render_template, url_for, flash, request, redirect
from datetime import datetime
from app import app
from app.model.model import get_db_connection
from app.controller import flacidez
from app.utils.data import data_br


@app.route("/flacidez")
def homepage_flacidez():
    conn = get_db_connection()
    cliente_flacidez = conn.execute('SELECT * FROM cliente_flacidez ORDER BY nome ASC').fetchall()
    conn.close()
    return render_template('flacidez/flacidez.html', cliente_flacidez=cliente_flacidez)

@app.route('/clienteflacidez/<int:cliente_id>')
def cliente_flacidez(cliente_id):
    conn = get_db_connection()
    cliente = conn.execute("SELECT * FROM cliente_flacidez WHERE id = ?", (cliente_id,)).fetchone()
    checkins = conn.execute("SELECT * FROM checkin_flacidez WHERE cliente_id = ? ORDER BY data ASC", (cliente_id,))
    agendamentos = conn.execute("SELECT * FROM historico_agendamento_flacidez WHERE cliente_id = ? ORDER BY data ASC", (cliente_id,))
    return render_template('flacidez/cliente_flacidez.html', cliente=cliente, checkins=checkins, agendamentos=agendamentos)

@app.route('/adcheckindataflacidez/<int:cliente_id>', methods=['GET', 'POST'])
def ad_checkin_flacidez_data(cliente_id):
    conn = get_db_connection()
    agora = datetime.now().strftime("%d/%m/%Y")
    cliente = conn.execute("SELECT * FROM cliente_flacidez WHERE id = ?", (cliente_id,)).fetchone()
    if request.method == 'POST':
        data_input = request.form['data_checkin'].strip()
        databr = data_br(data_input)
        status = False
        try:

            novos_checkins = cliente['checkins'] + 1
            if novos_checkins >= 5:
                status = True
            
            if novos_checkins >= 7:
                status = False
                novos_checkins = 0
                flacidez.zera_checkin(cliente_id)

            conn.execute(
                "INSERT INTO checkin_flacidez (cliente_id, data) VALUES (?, ?)",
                (cliente_id, databr)
            )
            if novos_checkins >= 7:
                flacidez.zera_checkin(cliente_id)
            conn.execute("UPDATE cliente_flacidez SET checkins = ? WHERE id = ?", (novos_checkins, cliente_id))
            conn.execute("UPDATE cliente_flacidez SET status = ? WHERE id = ?", (status,cliente_id))
            conn.commit()
            flash(f"Check-in adicionado para {cliente['nome']} em {databr}", "success")
            conn.close()
            return redirect(url_for('homepage_flacidez'))
        except ValueError:
            flash("Formato inválido! Use DD/MM/AAAA HH:MM", "warning")
    conn.close()
    return render_template('flacidez/ch_data_flacidez.html', cliente=cliente, agora=agora)

@app.route('/checkinflacidez/<int:cliente_id>')
def registrar_checkin_flacidez(cliente_id):
    conn = get_db_connection()
    cliente = conn.execute("SELECT * FROM cliente_flacidez WHERE id = ?", (cliente_id,)).fetchone()
    status = False

    if cliente:

        
        novos_checkins = cliente['checkins'] +1
        if novos_checkins >= 5:
            status = True
        
        if novos_checkins >= 7:
            status = False
            novos_checkins = 0
            flacidez.zera_checkin(cliente_id)
        
        conn.execute("INSERT INTO checkin_flacidez (cliente_id, data) VALUES (?, ?)",
                        (cliente_id, datetime.now().strftime("%d/%m/%Y %H:%M")))
        if novos_checkins >= 7:
            flacidez.zera_checkin(cliente_id)
        conn.execute("UPDATE cliente_flacidez SET checkins = ? WHERE id = ?", (novos_checkins, cliente_id))
        conn.execute("UPDATE cliente_flacidez SET status = ? WHERE id = ?", (status,cliente_id))
        conn.commit()
    conn.close()
    return redirect(url_for('homepage_flacidez'))

@app.route("/excluir_flacidez/<int:cliente_id>")
def excluir_flacidez(cliente_id):
    flacidez.excluir_cliente(cliente_id)
    return redirect(url_for("homepage_flacidez"))

@app.route("/excluircheckinflacidez/<int:checkin_id>")
def excluir_ch_flacidez(checkin_id):
    flacidez.excluir_checkin(checkin_id)
    flash(f"Check-in removido!", "warning")
    return redirect(url_for("homepage_flacidez"))

@app.route("/adicionaragendamentoflacidez/<int:cliente_id>", methods=['GET', 'POST'])
def adicionar_agendamento_flacidez(cliente_id):
    conn = get_db_connection()
    cliente = conn.execute("SELECT * FROM cliente_flacidez WHERE id = ?", (cliente_id,)).fetchone()
    if request.method == 'POST':
        data_input = request.form['data_checkin'].strip()
        try:
            flacidez.adicionar_agendamento(cliente_id, data=data_input)
            flash(f"Agendamento adicionado para {cliente['nome']} em {data_br(data_input)}", "success")
        except ValueError:
          flash("Formato inválido! Use DD/MM/AAAA HH:MM", "warning")  
    return render_template("flacidez/agendamento.html", cliente=cliente)


@app.route("/excluiragendamentoflacidez/<int:data_id>")
def excluir_agendamento_flacidez(data_id):
    flacidez.excluir_agendamento(data_id)
    flash(f"Agendamento removido!", "warning")
    return redirect(url_for("homepage_flacidez"))
