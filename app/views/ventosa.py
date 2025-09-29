from flask import render_template, url_for, flash, request, redirect
from datetime import datetime
from app import app
from app.model.model import get_db_connection
from app.controller import ventosa
from app.utils.data import data_br


@app.route("/ventosa")
def homepage_ventosa():
    conn = get_db_connection()
    cliente_ventosa = conn.execute('SELECT * FROM cliente_ventosa ORDER BY nome ASC').fetchall()
    conn.close()
    return render_template('ventosa/ventosa.html', cliente_ventosa=cliente_ventosa)

@app.route('/clienteventosa/<int:cliente_id>')
def cliente_ventosa(cliente_id):
    conn = get_db_connection()
    cliente = conn.execute("SELECT * FROM cliente_ventosa WHERE id = ?", (cliente_id,)).fetchone()
    checkins = conn.execute("SELECT * FROM checkin_ventosa WHERE cliente_id = ? ORDER BY data ASC", (cliente_id,))
    agendamentos = conn.execute("SELECT * FROM historico_agendamento_ventosa WHERE cliente_id = ? ORDER BY data ASC", (cliente_id,))
    return render_template('ventosa/cliente_ventosa.html', cliente=cliente, checkins=checkins, agendamentos=agendamentos)

@app.route('/adcheckindataventosa/<int:cliente_id>', methods=['GET', 'POST'])
def ad_checkin_ventosa_data(cliente_id):
    conn = get_db_connection()
    agora = datetime.now().strftime("%d/%m/%Y")
    cliente = conn.execute("SELECT * FROM cliente_ventosa WHERE id = ?", (cliente_id,)).fetchone()
    if request.method == 'POST':
        data_input = request.form['data_checkin'].strip()
        databr = data_br(data_input)
        status = False
        try:

            novos_checkins = cliente['checkins'] + 1
            if novos_checkins >= 3:
                status = True
            
            if novos_checkins >= 5:
                status = False
                novos_checkins = 0
                ventosa.zera_checkin(cliente_id)

            conn.execute(
                "INSERT INTO checkin_ventosa (cliente_id, data) VALUES (?, ?)",
                (cliente_id, databr)
            )
            if novos_checkins >= 5:
                ventosa.zera_checkin(cliente_id)
            conn.execute("UPDATE cliente_ventosa SET checkins = ? WHERE id = ?", (novos_checkins, cliente_id))
            conn.execute("UPDATE cliente_ventosa SET status = ? WHERE id = ?", (status,cliente_id))
            conn.commit()
            flash(f"Check-in adicionado para {cliente['nome']} em {databr}", "success")
            conn.close()
            return redirect(url_for('homepage_ventosa'))
        except ValueError:
            flash("Formato inválido! Use DD/MM/AAAA HH:MM", "warning")
    conn.close()
    return render_template('ventosa/ch_data_ventosa.html', cliente=cliente, agora=agora)

@app.route('/checkinventosa/<int:cliente_id>')
def registrar_checkin_ventosa(cliente_id):
    conn = get_db_connection()
    cliente = conn.execute("SELECT * FROM cliente_ventosa WHERE id = ?", (cliente_id,)).fetchone()
    status = False

    if cliente:

        
        novos_checkins = cliente['checkins'] +1
        if novos_checkins >= 3:
            status = True
        
        if novos_checkins >= 5:
            status = False
            novos_checkins = 0
            ventosa.zera_checkin(cliente_id)
        
        conn.execute("INSERT INTO checkin_ventosa (cliente_id, data) VALUES (?, ?)",
                        (cliente_id, datetime.now().strftime("%d/%m/%Y %H:%M")))
        if novos_checkins >= 5:
            ventosa.zera_checkin(cliente_id)
        conn.execute("UPDATE cliente_ventosa SET checkins = ? WHERE id = ?", (novos_checkins, cliente_id))
        conn.execute("UPDATE cliente_ventosa SET status = ? WHERE id = ?", (status,cliente_id))
        conn.commit()
    conn.close()
    return redirect(url_for('homepage_ventosa'))

@app.route("/excluir_ventosa/<int:cliente_id>")
def excluir_ventosa(cliente_id):
    ventosa.excluir_cliente(cliente_id)
    return redirect(url_for("homepage_ventosa"))

@app.route("/excluircheckinventosa/<int:checkin_id>")
def excluir_ch_ventosa(checkin_id):
    ventosa.excluir_checkin(checkin_id)
    flash(f"Check-in removido!", "warning")
    return redirect(url_for("homepage_ventosa"))

@app.route("/adicionaragendamentoventosa/<int:cliente_id>", methods=['GET', 'POST'])
def adicionar_agendamento_ventosa(cliente_id):
    conn = get_db_connection()
    cliente = conn.execute("SELECT * FROM cliente_ventosa WHERE id = ?", (cliente_id,)).fetchone()
    if request.method == 'POST':
        data_input = request.form['data_checkin'].strip()
        try:
            ventosa.adicionar_agendamento(cliente_id, data=data_input)
            flash(f"Agendamento adicionado para {cliente['nome']} em {data_br(data_input)}", "success")
        except ValueError:
          flash("Formato inválido! Use DD/MM/AAAA HH:MM", "warning")  
    return render_template("ventosa/agendamento.html", cliente=cliente)


@app.route("/excluiragendamentoventosa/<int:data_id>")
def excluir_agendamento_ventosa(data_id):
    ventosa.excluir_agendamento(data_id)
    flash(f"Agendamento removido!", "warning")
    return redirect(url_for("homepage_ventosa"))
