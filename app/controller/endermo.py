from app.model.model import get_db_connection


def adicionar_cliente(nome):
    conn = get_db_connection()
    conn.execute("INSERT INTO clientes_endermo (nome, status_endermo, checkins_endermo) VALUES (?, 0, 0)", (nome,))
    conn.commit()
    conn.close()

def excluir_cliente(cliente_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM clientes_endermo WHERE id = ?", (cliente_id,))
    conn.execute("DELETE FROM checkins_endermo WHERE cliente_id = ?", (cliente_id,))
    conn.commit()
    conn.close()



def excluir_checkin(checkin_id):
    conn = get_db_connection()
    cliente_id = conn.execute("SELECT * FROM checkins_endermo WHERE id = ?", (checkin_id,)).fetchone()['cliente_id']
    cliente = conn.execute("SELECT * FROM clientes_endermo WHERE id = ?", (cliente_id,)).fetchone()
    conn.execute("DELETE FROM checkins_endermo WHERE id = ?", (checkin_id,))
    status_endermo = False

    novos_checkins = cliente['checkins_endermo']
    if novos_checkins > 0:
        novos_checkins-=1
    
    if novos_checkins >= 3:
        status_endermo = True
    
    if novos_checkins >= 4:
        novos_checkins = 0
        status_endermo = False

    conn.execute("UPDATE clientes_endermo SET checkins_endermo = ? WHERE id = ?", (novos_checkins, cliente_id))
    conn.execute("UPDATE clientes_endermo SET status_endermo = ? WHERE id = ?", (status_endermo,cliente_id))
    conn.commit()
    conn.close()


def zera_checkin(cliente_id):
    '''reinicia a contagem dos histórico de check-ins'''

    conn = get_db_connection()
    conn.execute("DELETE FROM checkins_endermo WHERE cliente_id = ?", (cliente_id,))
    conn.commit()
    conn.close()
