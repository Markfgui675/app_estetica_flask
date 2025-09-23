from app.model.model import get_db_connection


def adicionar_cliente(nome):
    conn = get_db_connection()
    conn.execute("INSERT INTO clientes_ventosa (nome, status_ventosa, checkins_ventosa) VALUES (?, 0, 0)", (nome,))
    conn.commit()
    conn.close()

def excluir_cliente(cliente_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM clientes_ventosa WHERE id = ?", (cliente_id,))
    conn.execute("DELETE FROM checkins_ventosa WHERE cliente_id = ?", (cliente_id,))
    conn.commit()
    conn.close()



def excluir_checkin(checkin_id):
    conn = get_db_connection()
    cliente_id = conn.execute("SELECT * FROM checkins_ventosa WHERE id = ?", (checkin_id,)).fetchone()['cliente_id']
    cliente = conn.execute("SELECT * FROM clientes_ventosa WHERE id = ?", (cliente_id,)).fetchone()
    conn.execute("DELETE FROM checkins_ventosa WHERE id = ?", (checkin_id,))
    status_ventosa = False

    novos_checkins = cliente['checkins_ventosa']
    if novos_checkins > 0:
        novos_checkins-=1
    
    if novos_checkins >= 3:
        status_ventosa = True
    
    if novos_checkins >= 4:
        novos_checkins = 0
        status_ventosa = False

    conn.execute("UPDATE clientes_ventosa SET checkins_ventosa = ? WHERE id = ?", (novos_checkins, cliente_id))
    conn.execute("UPDATE clientes_ventosa SET status_ventosa = ? WHERE id = ?", (status_ventosa,cliente_id))
    conn.commit()
    conn.close()


def zera_checkin(cliente_id):
    '''reinicia a contagem dos histórico de check-ins'''

    conn = get_db_connection()
    conn.execute("DELETE FROM checkins_ventosa WHERE cliente_id = ?", (cliente_id,))
    conn.commit()
    conn.close()
