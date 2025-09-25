from app.model.model import get_db_connection


def adicionar_cliente(nome):
    conn = get_db_connection()
    conn.execute("INSERT INTO cliente_ventosa (nome, status, checkins) VALUES (?, 0, 0)", (nome,))
    conn.commit()
    conn.close()

def excluir_cliente(cliente_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM cliente_ventosa WHERE id = ?", (cliente_id,))
    conn.execute("DELETE FROM checkin_ventosa WHERE cliente_id = ?", (cliente_id,))
    conn.commit()
    conn.close()



def excluir_checkin(checkin_id):
    conn = get_db_connection()
    cliente_id = conn.execute("SELECT * FROM checkin_ventosa WHERE id = ?", (checkin_id,)).fetchone()['cliente_id']
    cliente = conn.execute("SELECT * FROM cliente_ventosa WHERE id = ?", (cliente_id,)).fetchone()
    conn.execute("DELETE FROM checkin_ventosa WHERE id = ?", (checkin_id,))
    status = False

    novos_checkins = cliente['checkins']
    if novos_checkins > 0:
        novos_checkins-=1
    
    if novos_checkins >= 3:
        status = True
    
    if novos_checkins >= 4:
        novos_checkins = 0
        status = False

    conn.execute("UPDATE cliente_ventosa SET checkins = ? WHERE id = ?", (novos_checkins, cliente_id))
    conn.execute("UPDATE cliente_ventosa SET status = ? WHERE id = ?", (status,cliente_id))
    conn.commit()
    conn.close()


def zera_checkin(cliente_id):
    '''reinicia a contagem dos histórico de check-ins'''

    conn = get_db_connection()
    conn.execute("DELETE FROM checkin_ventosa WHERE cliente_id = ?", (cliente_id,))
    conn.commit()
    conn.close()
