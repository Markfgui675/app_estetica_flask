from app.model.model import get_db_connection

def adicionar_cliente(nome):
    conn = get_db_connection()
    conn.execute("INSERT INTO clientes_limpeza (nome, status_limpeza, checkins_limpeza) VALUES (?, 0, 0)", (nome,))
    conn.commit()
    conn.close()

def excluir_cliente(cliente_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM clientes_limpeza WHERE id = ?", (cliente_id,))
    conn.execute("DELETE FROM checkins_limpeza WHERE cliente_id = ?", (cliente_id,))
    conn.commit()
    conn.close()

def excluir_checkin(checkin_id):
    conn = get_db_connection()
    cliente_id = conn.execute("SELECT * FROM checkins_limpeza WHERE id = ?", (checkin_id,)).fetchone()['cliente_id']
    cliente = conn.execute("SELECT * FROM clientes_limpeza WHERE id = ?", (cliente_id,)).fetchone()
    conn.execute("DELETE FROM checkins_limpeza WHERE id = ?", (checkin_id,))
    status_limpeza = False

    novos_checkins = cliente['checkins_limpeza']
    if novos_checkins > 0:
        novos_checkins-=1
    
    if novos_checkins >= 4:
        status_limpeza = True
    
    if novos_checkins >= 5:
        novos_checkins = 0
        status_limpeza = False

    conn.execute("UPDATE clientes_limpeza SET checkins_limpeza = ? WHERE id = ?", (novos_checkins, cliente_id))
    conn.execute("UPDATE clientes_limpeza SET status_limpeza = ? WHERE id = ?", (status_limpeza,cliente_id))
    conn.commit()
    conn.close()

def zera_checkin(cliente_id):
    '''reinicia a contagem dos histórico de check-ins'''

    conn = get_db_connection()
    conn.execute("DELETE FROM checkins_limpeza WHERE cliente_id = ?", (cliente_id,))
    conn.commit()
    conn.close()
