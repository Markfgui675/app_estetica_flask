from flask import render_template, url_for, flash, request, redirect
from datetime import datetime
from app import app
from app.model.model import get_db_connection
from app.controller import ventosa


@app.route("/ventosa")
def homepage_ventosa():
    conn = get_db_connection()
    clientes_ventosa = conn.execute('SELECT * FROM clientes_ventosa').fetchall()
    conn.close()
    return render_template('ventosa/ventosa.html', clientes_ventosa=clientes_ventosa)

@app.route('/clienteventosa/<int:cliente_id>')
def cliente_ventosa(cliente_id):
    conn = get_db_connection()
    cliente = conn.execute("SELECT * FROM clientes_ventosa WHERE id = ?", (cliente_id,)).fetchone()
    checkins = conn.execute("SELECT * FROM checkins_ventosa WHERE cliente_id = ?", (cliente_id,))
    return render_template('ventosa/cliente_ventosa.html', cliente=cliente, checkins=checkins)

@app.route('/adcheckindataventosa/<int:cliente_id>', methods=['GET', 'POST'])
def ad_checkin_ventosa_data(cliente_id):
    conn = get_db_connection()
    agora = datetime.now().strftime("%d/%m/%Y")
    cliente = conn.execute("SELECT * FROM clientes_ventosa WHERE id = ?", (cliente_id,)).fetchone()
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
        status_ventosa = False
        try:
            #Valida e formata a data
            data_formatada = datetime.strptime(data_input, "%d/%m/%Y %H:%M")
            data_str = data_formatada.strftime("%d/%m/%Y %H:%M:%S")

            novos_checkins = cliente['checkins_ventosa'] + 1
            if novos_checkins >= 3:
                status_ventosa = True
            
            if novos_checkins >= 4:
                status_ventosa = False
                novos_checkins = 0
                ventosa.zera_checkin(cliente_id)

            conn.execute(
                "INSERT INTO checkins_ventosa (cliente_id, data) VALUES (?, ?)",
                (cliente_id, data_str)
            )
            conn.execute("UPDATE clientes_ventosa SET checkins_ventosa = ? WHERE id = ?", (novos_checkins, cliente_id))
            conn.execute("UPDATE clientes_ventosa SET status_ventosa = ? WHERE id = ?", (status_ventosa,cliente_id))
            conn.commit()
            flash(f"Check-in adicionado para {cliente['nome']} em {data_str}", "success")
            conn.close()
            return redirect(url_for('homepage_ventosa'))
        except ValueError:
            flash("Formato inválido! Use DD/MM/AAAA HH:MM", "warning")
    conn.close()
    return render_template('ventosa/ch_data_ventosa.html', cliente=cliente, agora=agora)

@app.route('/checkinventosa/<int:cliente_id>')
def registrar_checkin_ventosa(cliente_id):
    conn = get_db_connection()
    cliente = conn.execute("SELECT * FROM clientes_ventosa WHERE id = ?", (cliente_id,)).fetchone()
    status_ventosa = False

    if cliente:

        hoje = datetime.now().strftime("%d/%m/%Y")

        checkin_existente = conn.execute('''SELECT * FROM checkins_ventosa WHERE cliente_id = ? AND data LIKE ?''', (cliente_id, f"{hoje}%")).fetchone()

        if checkin_existente:
            flash(f"O cliente {cliente['nome']} já fez check-in hoje!", "warning")
            conn.close()
            return redirect(url_for('homepage_ventosa'))
        
        novos_checkins = cliente['checkins_ventosa'] +1
        if novos_checkins >= 3:
            status_ventosa = True
        
        if novos_checkins >= 4:
            status_ventosa = False
            novos_checkins = 0
            ventosa.zera_checkin(cliente_id)
        
        conn.execute("UPDATE clientes_ventosa SET checkins_ventosa = ? WHERE id = ?", (novos_checkins, cliente_id))
        conn.execute("UPDATE clientes_ventosa SET status_ventosa = ? WHERE id = ?", (status_ventosa,cliente_id))
        conn.execute("INSERT INTO checkins_ventosa (cliente_id, data) VALUES (?, ?)",
                        (cliente_id, datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
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
