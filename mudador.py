@app.route("/adicionaragendamentoventosa/<int:cliente_id>", methods=['GET', 'POST'])
def adicionar_agendamento_ventosa(cliente_id):
    conn = get_db_connection()
    cliente = conn.execute("SELECT * FROM cliente_ventosa WHERE id = ?", (cliente_id,)).fetchone()
    if request.method == 'POST':
        data_input = request.form['data_checkin'].strip()
        try:
            ventosa.adicionar_agendamento(cliente_id, data=data_input)
            flash(f"Agendamento adicionado para {cliente['nome']} em {data_input}", "success")
        except ValueError:
          flash("Formato inválido! Use DD/MM/AAAA HH:MM", "warning")  
    return render_template("ventosa/agendamento.html", cliente=cliente)


@app.route("/excluiragendamentoventosa/<int:data_id>")
def excluir_agendamento_ventosa(data_id):
    ventosa.excluir_agendamento(data_id)
    flash(f"Agendamento removido!", "warning")
    return redirect(url_for("homepage_ventosa"))