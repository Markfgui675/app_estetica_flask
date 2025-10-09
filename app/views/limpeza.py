from flask import render_template, url_for, flash, request, redirect
from datetime import datetime
from app import app
from app.model.model import get_db_connection
from app.controller import limpeza
from app.utils.data import data_br


@app.route("/limpeza")
def homepage_limpeza():
    conn = get_db_connection()
    cliente_limpeza = conn.execute('SELECT * FROM cliente_limpeza ORDER BY nome ASC').fetchall()
    conn.close()
    return render_template('limpeza/limpeza.html', cliente_limpeza=cliente_limpeza)

@app.route('/clientelimpeza/<int:cliente_id>')
def cliente_limpeza(cliente_id):
    conn = get_db_connection()
    cliente = conn.execute("SELECT * FROM cliente_limpeza WHERE id = ?", (cliente_id,)).fetchone()
    checkins = conn.execute("SELECT * FROM checkin_limpeza WHERE cliente_id = ? ORDER BY data ASC", (cliente_id,))
    agendamentos = conn.execute("SELECT * FROM historico_agendamento_limpeza WHERE cliente_id = ? ORDER BY data ASC", (cliente_id,))
    return render_template('limpeza/cliente_limpeza.html', cliente=cliente, checkins=checkins, agendamentos=agendamentos)

@app.route('/adcheckindatalimpeza/<int:cliente_id>', methods=['GET', 'POST'])
def ad_checkin_limpeza_data(cliente_id):
    conn = get_db_connection()
    agora = datetime.now().strftime("%d/%m/%Y")
    cliente = conn.execute("SELECT * FROM cliente_limpeza WHERE id = ?", (cliente_id,)).fetchone()
    if request.method == 'POST':
        data_input = request.form['data_checkin'].strip()
        databr = data_br(data_input)
        status = False
        try:

            novos_checkins = cliente['checkins'] + 1
            if novos_checkins >= 6:
                status = True
            
            if novos_checkins >= 8:
                status = False
                novos_checkins = 0
                limpeza.zera_checkin(cliente_id)

            conn.execute(
                "INSERT INTO checkin_limpeza (cliente_id, data) VALUES (?, ?)",
                (cliente_id, databr)
            )
            if novos_checkins >= 8:
                limpeza.zera_checkin(cliente_id)
            conn.execute("UPDATE cliente_limpeza SET checkins = ? WHERE id = ?", (novos_checkins, cliente_id))
            conn.execute("UPDATE cliente_limpeza SET status = ? WHERE id = ?", (status,cliente_id))
            conn.commit()
            flash(f"Check-in adicionado para {cliente['nome']} em {databr}", "success")
            conn.close()
            return redirect(url_for('homepage_limpeza'))
        except ValueError:
            flash("Formato inválido! Use DD/MM/AAAA HH:MM", "warning")
    conn.close()
    return render_template('limpeza/ch_data_limpeza.html', cliente=cliente, agora=agora)

@app.route('/checkinlimpeza/<int:cliente_id>')
def registrar_checkin_limpeza(cliente_id):
    conn = get_db_connection()
    cliente = conn.execute("SELECT * FROM cliente_limpeza WHERE id = ?", (cliente_id,)).fetchone()
    status = False

    if cliente:

        
        novos_checkins = cliente['checkins'] +1
        if novos_checkins >= 6:
            status = True
        
        if novos_checkins >= 8:
            status = False
            novos_checkins = 0
            limpeza.zera_checkin(cliente_id)
        
        conn.execute("INSERT INTO checkin_limpeza (cliente_id, data) VALUES (?, ?)",
                        (cliente_id, datetime.now().strftime("%d/%m/%Y %H:%M")))
        if novos_checkins >= 8:
            limpeza.zera_checkin(cliente_id)
        conn.execute("UPDATE cliente_limpeza SET checkins = ? WHERE id = ?", (novos_checkins, cliente_id))
        conn.execute("UPDATE cliente_limpeza SET status = ? WHERE id = ?", (status,cliente_id))
        conn.commit()
    conn.close()
    return redirect(url_for('homepage_limpeza'))

@app.route("/excluir_limpeza/<int:cliente_id>")
def excluir_limpeza(cliente_id):
    limpeza.excluir_cliente(cliente_id)
    return redirect(url_for("homepage_limpeza"))

@app.route("/excluircheckinlimpeza/<int:checkin_id>")
def excluir_ch_limpeza(checkin_id):
    limpeza.excluir_checkin(checkin_id)
    flash(f"Check-in removido!", "warning")
    return redirect(url_for("homepage_limpeza"))

@app.route("/adicionaragendamentolimpeza/<int:cliente_id>", methods=['GET', 'POST'])
def adicionar_agendamento_limpeza(cliente_id):
    conn = get_db_connection()
    cliente = conn.execute("SELECT * FROM cliente_limpeza WHERE id = ?", (cliente_id,)).fetchone()
    if request.method == 'POST':
        data_input = request.form['data_checkin'].strip()
        try:
            limpeza.adicionar_agendamento(cliente_id, data=data_input)
            flash(f"Agendamento adicionado para {cliente['nome']} em {data_br(data_input)}", "success")
        except ValueError:
          flash("Formato inválido! Use DD/MM/AAAA HH:MM", "warning")  
    return render_template("limpeza/agendamento.html", cliente=cliente)


@app.route("/excluiragendamentolimpeza/<int:data_id>")
def excluir_agendamento_limpeza(data_id):
    limpeza.excluir_agendamento(data_id)
    flash(f"Agendamento removido!", "warning")
    return redirect(url_for("homepage_limpeza"))

@app.route("/busca_limpeza", methods=['GET', 'POST'])
def buscar_limpeza():
    resultados = []
    termo = ""
    if request.method == 'POST':
        termo = request.form['termo'].strip()
        resultados = limpeza.buscar_clientes(termo)
    return render_template('limpeza/limpeza.html', resultados=resultados)
