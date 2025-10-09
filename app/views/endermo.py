from flask import render_template, url_for, flash, request, redirect
from datetime import datetime
from app import app
from app.model.model import get_db_connection
from app.controller import endermo
from app.utils.data import data_br

@app.route("/endermo")
def homepage_endermo():
    conn = get_db_connection()
    cliente_endermo = conn.execute('SELECT * FROM cliente_endermo ORDER BY nome ASC').fetchall()
    conn.close()
    return render_template('endermo/endermo.html', cliente_endermo=cliente_endermo)

@app.route('/clienteendermo/<int:cliente_id>')
def cliente_endermo(cliente_id):
    conn = get_db_connection()
    cliente = conn.execute("SELECT * FROM cliente_endermo WHERE id = ?", (cliente_id,)).fetchone()
    checkins = conn.execute("SELECT * FROM checkin_endermo WHERE cliente_id = ? ORDER BY data ASC", (cliente_id,))
    agendamentos = conn.execute("SELECT * FROM historico_agendamento_endermo WHERE cliente_id = ? ORDER BY data ASC", (cliente_id,))
    return render_template('endermo/cliente_endermo.html', cliente=cliente, checkins=checkins, agendamentos=agendamentos)

@app.route('/adcheckindataendermo/<int:cliente_id>', methods=['GET', 'POST'])
def ad_checkin_endermo_data(cliente_id):
    conn = get_db_connection()
    agora = datetime.now().strftime("%d/%m/%Y")
    cliente = conn.execute("SELECT * FROM cliente_endermo WHERE id = ?", (cliente_id,)).fetchone()
    if request.method == 'POST':
        data_input = request.form['data_checkin'].strip()
        databr = data_br(data_input)
        status = False
        try:

            novos_checkins = cliente['checkins'] + 1
            if novos_checkins >= 7:
                status = True
            
            if novos_checkins >= 9:
                status = False
                novos_checkins = 0
                endermo.zera_checkin(cliente_id)

            conn.execute(
                "INSERT INTO checkin_endermo (cliente_id, data) VALUES (?, ?)",
                (cliente_id, databr)
            )
            if novos_checkins >= 9:
                endermo.zera_checkin(cliente_id)
            conn.execute("UPDATE cliente_endermo SET checkins = ? WHERE id = ?", (novos_checkins, cliente_id))
            conn.execute("UPDATE cliente_endermo SET status = ? WHERE id = ?", (status,cliente_id))
            conn.commit()
            flash(f"Check-in adicionado para {cliente['nome']} em {databr}", "success")
            conn.close()
            return redirect(url_for('homepage_endermo'))
        except ValueError:
            flash("Formato inválido! Use DD/MM/AAAA HH:MM", "warning")
    conn.close()
    return render_template('endermo/ch_data_endermo.html', cliente=cliente, agora=agora)

@app.route('/checkinendermo/<int:cliente_id>')
def registrar_checkin_endermo(cliente_id):
    conn = get_db_connection()
    cliente = conn.execute("SELECT * FROM cliente_endermo WHERE id = ?", (cliente_id,)).fetchone()
    status = False

    if cliente:

        
        novos_checkins = cliente['checkins'] +1
        if novos_checkins >= 7:
            status = True
        
        if novos_checkins >= 9:
            status = False
            novos_checkins = 0
            endermo.zera_checkin(cliente_id)
        
        conn.execute("INSERT INTO checkin_endermo (cliente_id, data) VALUES (?, ?)",
                        (cliente_id, datetime.now().strftime("%d/%m/%Y %H:%M")))
        if novos_checkins >= 9:
            endermo.zera_checkin(cliente_id)
        conn.execute("UPDATE cliente_endermo SET checkins = ? WHERE id = ?", (novos_checkins, cliente_id))
        conn.execute("UPDATE cliente_endermo SET status = ? WHERE id = ?", (status,cliente_id))
        conn.commit()
    conn.close()
    return redirect(url_for('homepage_endermo'))

@app.route("/excluir_endermo/<int:cliente_id>")
def excluir_endermo(cliente_id):
    endermo.excluir_cliente(cliente_id)
    return redirect(url_for("homepage_endermo"))

@app.route("/excluircheckinendermo/<int:checkin_id>")
def excluir_ch_endermo(checkin_id):
    endermo.excluir_checkin(checkin_id)
    flash(f"Check-in removido!", "warning")
    return redirect(url_for("homepage_endermo"))

@app.route("/adicionaragendamentoendermo/<int:cliente_id>", methods=['GET', 'POST'])
def adicionar_agendamento_endermo(cliente_id):
    conn = get_db_connection()
    cliente = conn.execute("SELECT * FROM cliente_endermo WHERE id = ?", (cliente_id,)).fetchone()
    if request.method == 'POST':
        data_input = request.form['data_checkin'].strip()
        try:
            endermo.adicionar_agendamento(cliente_id, data=data_input)
            flash(f"Agendamento adicionado para {cliente['nome']} em {data_br(data_input)}", "success")
        except ValueError:
          flash("Formato inválido! Use DD/MM/AAAA HH:MM", "warning")  
    return render_template("endermo/agendamento.html", cliente=cliente)


@app.route("/excluiragendamentoendermo/<int:data_id>")
def excluir_agendamento_endermo(data_id):
    endermo.excluir_agendamento(data_id)
    flash(f"Agendamento removido!", "warning")
    return redirect(url_for("homepage_endermo"))

@app.route("/busca_endermo", methods=['GET', 'POST'])
def buscar_endermo():
    resultados = []
    termo = ""
    if request.method == 'POST':
        termo = request.form['termo'].strip()
        resultados = endermo.buscar_clientes(termo)
    return render_template('endermo/endermo.html', resultados=resultados)
