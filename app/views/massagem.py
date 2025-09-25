from flask import render_template, url_for, flash, request, redirect
from datetime import datetime
from app import app
from app.model.model import get_db_connection
from app.controller import massagem

@app.route("/")
def homepage_massagem():
    conn = get_db_connection()
    cliente_massagem = conn.execute('SELECT * FROM cliente_massagem ORDER BY nome ASC').fetchall()
    conn.close()
    return render_template('massagem/massagem.html', cliente_massagem=cliente_massagem)

@app.route('/clientemassagem/<int:cliente_id>')
def cliente_massagem(cliente_id):
    conn = get_db_connection()
    cliente = conn.execute("SELECT * FROM cliente_massagem WHERE id = ?", (cliente_id,)).fetchone()
    checkins = conn.execute("SELECT * FROM checkin_massagem WHERE cliente_id = ? ORDER BY data ASC", (cliente_id,))
    agendamentos = conn.execute("SELECT * FROM historico_agendamento_massagem WHERE cliente_id = ? ORDER BY data ASC", (cliente_id,))
    return render_template('massagem/cliente_massagem.html', cliente=cliente, checkins=checkins, agendamentos=agendamentos)

@app.route('/adcheckindatamassagem/<int:cliente_id>', methods=['GET', 'POST'])
def ad_checkin_massagem_data(cliente_id):
    conn = get_db_connection()
    agora = datetime.now().strftime("%d/%m/%Y")
    cliente = conn.execute("SELECT * FROM cliente_massagem WHERE id = ?", (cliente_id,)).fetchone()
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
                massagem.zera_checkin(cliente_id)

            conn.execute(
                "INSERT INTO checkin_massagem (cliente_id, data) VALUES (?, ?)",
                (cliente_id, data_input)
            )
            conn.execute("UPDATE cliente_massagem SET checkins = ? WHERE id = ?", (novos_checkins, cliente_id))
            conn.execute("UPDATE cliente_massagem SET status = ? WHERE id = ?", (status,cliente_id))
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
    cliente = conn.execute("SELECT * FROM cliente_massagem WHERE id = ?", (cliente_id,)).fetchone()
    status = False

    if cliente:
        
        novos_checkins = cliente['checkins'] + 1
        if novos_checkins >= 3:
            status = True
        
        if novos_checkins >= 4:
            status = False
            novos_checkins = 0
            massagem.zera_checkin(cliente_id)
        

        conn.execute("INSERT INTO checkin_massagem (cliente_id, data) VALUES (?, ?)",
                        (cliente_id, datetime.now()))
        conn.execute("UPDATE cliente_massagem SET checkins = ? WHERE id = ?", (novos_checkins, cliente_id))
        conn.execute("UPDATE cliente_massagem SET status = ? WHERE id = ?", (status,cliente_id))
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

@app.route("/adicionaragendamentomassagem/<int:cliente_id>", methods=['GET', 'POST'])
def adicionar_agendamento_massagem(cliente_id):
    conn = get_db_connection()
    cliente = conn.execute("SELECT * FROM cliente_massagem WHERE id = ?", (cliente_id,)).fetchone()
    if request.method == 'POST':
        data_input = request.form['data_checkin'].strip()
        try:
            massagem.adicionar_agendamento(cliente_id, data=data_input)
            flash(f"Agendamento adicionado para {cliente['nome']} em {data_input}", "success")
        except ValueError:
          flash("Formato inválido! Use DD/MM/AAAA HH:MM", "warning")  
    return render_template("massagem/agendamento.html", cliente=cliente)


@app.route("/excluiragendamentomassagem/<int:data_id>")
def excluir_agendamento_massagem(data_id):
    massagem.excluir_agendamento(data_id)
    flash(f"Agendamento removido!", "warning")
    return redirect(url_for("homepage_massagem"))
