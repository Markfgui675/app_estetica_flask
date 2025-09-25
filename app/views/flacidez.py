from flask import render_template, url_for, flash, request, redirect
from datetime import datetime
from app import app
from app.model.model import get_db_connection
from app.controller import flacidez


@app.route("/flacidez")
def homepage_flacidez():
    conn = get_db_connection()
    clientes_flacidez = conn.execute('SELECT * FROM clientes_flacidez').fetchall()
    conn.close()
    return render_template('flacidez/flacidez.html', clientes_flacidez=clientes_flacidez)

@app.route('/clienteflacidez/<int:cliente_id>')
def cliente_flacidez(cliente_id):
    conn = get_db_connection()
    cliente = conn.execute("SELECT * FROM clientes_flacidez WHERE id = ?", (cliente_id,)).fetchone()
    checkins = conn.execute("SELECT * FROM checkins_flacidez WHERE cliente_id = ?", (cliente_id,))
    return render_template('flacidez/cliente_flacidez.html', cliente=cliente, checkins=checkins)

@app.route('/adcheckindataflacidez/<int:cliente_id>', methods=['GET', 'POST'])
def ad_checkin_flacidez_data(cliente_id):
    conn = get_db_connection()
    agora = datetime.now().strftime("%d/%m/%Y")
    cliente = conn.execute("SELECT * FROM clientes_flacidez WHERE id = ?", (cliente_id,)).fetchone()
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
        status_flacidez = False
        try:
            #Valida e formata a data
            data_formatada = datetime.strptime(data_input, "%d/%m/%Y %H:%M")
            data_str = data_formatada.strftime("%d/%m/%Y %H:%M:%S")

            novos_checkins = cliente['checkins_flacidez'] + 1
            if novos_checkins >= 5:
                status_flacidez = True
            
            if novos_checkins >= 6:
                status_flacidez = False
                novos_checkins = 0
                flacidez.zera_checkin(cliente_id)

            conn.execute(
                "INSERT INTO checkins_flacidez (cliente_id, data) VALUES (?, ?)",
                (cliente_id, data_str)
            )
            conn.execute("UPDATE clientes_flacidez SET checkins_flacidez = ? WHERE id = ?", (novos_checkins, cliente_id))
            conn.execute("UPDATE clientes_flacidez SET status_flacidez = ? WHERE id = ?", (status_flacidez,cliente_id))
            conn.commit()
            flash(f"Check-in adicionado para {cliente['nome']} em {data_str}", "success")
            conn.close()
            return redirect(url_for('homepage_flacidez'))
        except ValueError:
            flash("Formato inválido! Use DD/MM/AAAA HH:MM", "warning")
    conn.close()
    return render_template('flacidez/ch_data_flacidez.html', cliente=cliente, agora=agora)

@app.route('/checkinflacidez/<int:cliente_id>')
def registrar_checkin_flacidez(cliente_id):
    conn = get_db_connection()
    cliente = conn.execute("SELECT * FROM clientes_flacidez WHERE id = ?", (cliente_id,)).fetchone()
    status_flacidez = False

    if cliente:

        
        novos_checkins = cliente['checkins_flacidez'] +1
        if novos_checkins >= 5:
            status_flacidez = True
        
        if novos_checkins >= 6:
            status_flacidez = False
            novos_checkins = 0
            flacidez.zera_checkin(cliente_id)
        
        conn.execute("UPDATE clientes_flacidez SET checkins_flacidez = ? WHERE id = ?", (novos_checkins, cliente_id))
        conn.execute("UPDATE clientes_flacidez SET status_flacidez = ? WHERE id = ?", (status_flacidez,cliente_id))
        conn.execute("INSERT INTO checkins_flacidez (cliente_id, data) VALUES (?, ?)",
                        (cliente_id, datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
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
