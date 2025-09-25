from app.model.model import get_db_connection


def adicionar_cliente(nome):
    conn = get_db_connection()
    conn.execute("INSERT INTO clientes_flacidez (nome, status_flacidez, checkins_flacidez) VALUES (?, 0, 0)", (nome,))
    conn.commit()
    conn.close()

def excluir_cliente(cliente_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM clientes_flacidez WHERE id = ?", (cliente_id,))
    conn.execute("DELETE FROM checkins_flacidez WHERE cliente_id = ?", (cliente_id,))
    conn.commit()
    conn.close()



def excluir_checkin(checkin_id):
    conn = get_db_connection()
    cliente_id = conn.execute("SELECT * FROM checkins_flacidez WHERE id = ?", (checkin_id,)).fetchone()['cliente_id']
    cliente = conn.execute("SELECT * FROM clientes_flacidez WHERE id = ?", (cliente_id,)).fetchone()
    conn.execute("DELETE FROM checkins_flacidez WHERE id = ?", (checkin_id,))
    status_flacidez = False

    novos_checkins = cliente['checkins_flacidez']
    if novos_checkins > 0:
        novos_checkins-=1
    
    if novos_checkins >= 5:
        status_flacidez = True
    
    if novos_checkins >= 6:
        novos_checkins = 0
        status_flacidez = False

    conn.execute("UPDATE clientes_flacidez SET checkins_flacidez = ? WHERE id = ?", (novos_checkins, cliente_id))
    conn.execute("UPDATE clientes_flacidez SET status_flacidez = ? WHERE id = ?", (status_flacidez,cliente_id))
    conn.commit()
    conn.close()


def zera_checkin(cliente_id):
    '''reinicia a contagem dos histórico de check-ins'''

    conn = get_db_connection()
    conn.execute("DELETE FROM checkins_flacidez WHERE cliente_id = ?", (cliente_id,))
    conn.commit()
    conn.close()
