from app.model.model import get_db_connection


def adicionar_cliente(nome):
    conn = get_db_connection()
    conn.execute("INSERT INTO clientes_detox (nome, status_detox, checkins_detox) VALUES (?, 0, 0)", (nome,))
    conn.commit()
    conn.close()

def excluir_cliente(cliente_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM clientes_detox WHERE id = ?", (cliente_id,))
    conn.execute("DELETE FROM checkins_detox WHERE cliente_id = ?", (cliente_id,))
    conn.commit()
    conn.close()



def excluir_checkin(checkin_id):
    conn = get_db_connection()
    cliente_id = conn.execute("SELECT * FROM checkins_detox WHERE id = ?", (checkin_id,)).fetchone()['cliente_id']
    cliente = conn.execute("SELECT * FROM clientes_detox WHERE id = ?", (cliente_id,)).fetchone()
    conn.execute("DELETE FROM checkins_detox WHERE id = ?", (checkin_id,))
    status_detox = False

    novos_checkins = cliente['checkins_detox']
    if novos_checkins > 0:
        novos_checkins-=1
    
    if novos_checkins >= 3:
        status_detox = True
    
    if novos_checkins >= 4:
        novos_checkins = 0
        status_detox = False

    conn.execute("UPDATE clientes_detox SET checkins_detox = ? WHERE id = ?", (novos_checkins, cliente_id))
    conn.execute("UPDATE clientes_detox SET status_detox = ? WHERE id = ?", (status_detox,cliente_id))
    conn.commit()
    conn.close()


def zera_checkin(cliente_id):
    '''reinicia a contagem dos histórico de check-ins'''

    conn = get_db_connection()
    conn.execute("DELETE FROM checkins_detox WHERE cliente_id = ?", (cliente_id,))
    conn.commit()
    conn.close()
