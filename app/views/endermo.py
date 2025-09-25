from flask import render_template, url_for, flash, request, redirect
from datetime import datetime
from app import app
from app.model.model import get_db_connection
from app.controller import endermo


@app.route("/endermo")
def homepage_endermo():
    conn = get_db_connection()
    clientes_endermo = conn.execute('SELECT * FROM clientes_endermo ORDER BY nome ASC').fetchall()
    conn.close()
    return render_template('endermo/endermo.html', clientes_endermo=clientes_endermo)

@app.route('/clienteendermo/<int:cliente_id>')
def cliente_endermo(cliente_id):
    conn = get_db_connection()
    cliente = conn.execute("SELECT * FROM clientes_endermo WHERE id = ?", (cliente_id,)).fetchone()
    checkins = conn.execute("SELECT * FROM checkins_endermo WHERE cliente_id = ? ORDER BY data DESC", (cliente_id,))
    return render_template('endermo/cliente_endermo.html', cliente=cliente, checkins=checkins)

@app.route('/adcheckindataendermo/<int:cliente_id>', methods=['GET', 'POST'])
def ad_checkin_endermo_data(cliente_id):
    conn = get_db_connection()
    agora = datetime.now().strftime("%d/%m/%Y")
    cliente = conn.execute("SELECT * FROM clientes_endermo WHERE id = ?", (cliente_id,)).fetchone()
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
        status_endermo = False
        try:
            #Valida e formata a data
            data_formatada = datetime.strptime(data_input, "%d/%m/%Y %H:%M")
            data_str = data_formatada.strftime("%d/%m/%Y %H:%M:%S")

            novos_checkins = cliente['checkins_endermo'] + 1
            if novos_checkins >= 5:
                status_endermo = True
            
            if novos_checkins >= 6:
                status_endermo = False
                novos_checkins = 0
                endermo.zera_checkin(cliente_id)

            conn.execute(
                "INSERT INTO checkins_endermo (cliente_id, data) VALUES (?, ?)",
                (cliente_id, data_str)
            )
            conn.execute("UPDATE clientes_endermo SET checkins_endermo = ? WHERE id = ?", (novos_checkins, cliente_id))
            conn.execute("UPDATE clientes_endermo SET status_endermo = ? WHERE id = ?", (status_endermo,cliente_id))
            conn.commit()
            flash(f"Check-in adicionado para {cliente['nome']} em {data_str}", "success")
            conn.close()
            return redirect(url_for('homepage_endermo'))
        except ValueError:
            flash("Formato inválido! Use DD/MM/AAAA HH:MM", "warning")
    conn.close()
    return render_template('endermo/ch_data_endermo.html', cliente=cliente, agora=agora)

@app.route('/checkinendermo/<int:cliente_id>')
def registrar_checkin_endermo(cliente_id):
    conn = get_db_connection()
    cliente = conn.execute("SELECT * FROM clientes_endermo WHERE id = ?", (cliente_id,)).fetchone()
    status_endermo = False

    if cliente:

        
        novos_checkins = cliente['checkins_endermo'] +1
        if novos_checkins >= 5:
            status_endermo = True
        
        if novos_checkins >= 6:
            status_endermo = False
            novos_checkins = 0
            endermo.zera_checkin(cliente_id)
        
        conn.execute("UPDATE clientes_endermo SET checkins_endermo = ? WHERE id = ?", (novos_checkins, cliente_id))
        conn.execute("UPDATE clientes_endermo SET status_endermo = ? WHERE id = ?", (status_endermo,cliente_id))
        conn.execute("INSERT INTO checkins_endermo (cliente_id, data) VALUES (?, ?)",
                        (cliente_id, datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
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
