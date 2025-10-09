from app.model.model import get_db_connection
from app.utils.data import data_br

def adicionar_cliente(nome):
    conn = get_db_connection()
    conn.execute("INSERT INTO cliente_endermo (nome, status, checkins) VALUES (?, 0, 0)", (nome,))
    conn.commit()
    conn.close()

def excluir_cliente(cliente_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM cliente_endermo WHERE id = ?", (cliente_id,))
    conn.execute("DELETE FROM checkin_endermo WHERE cliente_id = ?", (cliente_id,))
    conn.commit()
    conn.close()



def excluir_checkin(checkin_id):
    conn = get_db_connection()
    cliente_id = conn.execute("SELECT * FROM checkin_endermo WHERE id = ?", (checkin_id,)).fetchone()['cliente_id']
    cliente = conn.execute("SELECT * FROM cliente_endermo WHERE id = ?", (cliente_id,)).fetchone()
    conn.execute("DELETE FROM checkin_endermo WHERE id = ?", (checkin_id,))
    status = False

    novos_checkins = cliente['checkins']
    if novos_checkins > 0:
        novos_checkins-=1
    
    if novos_checkins >= 7:
        status = True
    
    if novos_checkins >= 8:
        novos_checkins = 0
        status = False

    conn.execute("UPDATE cliente_endermo SET checkins = ? WHERE id = ?", (novos_checkins, cliente_id))
    conn.execute("UPDATE cliente_endermo SET status = ? WHERE id = ?", (status,cliente_id))
    conn.commit()
    conn.close()


def zera_checkin(cliente_id):
    '''reinicia a contagem dos histórico de check-ins'''

    conn = get_db_connection()
    conn.execute("DELETE FROM checkin_endermo WHERE cliente_id = ?", (cliente_id,))
    conn.commit()
    conn.close()

def adicionar_agendamento(cliente_id, data):
    conn = get_db_connection()
    databr = data_br(data)
    conn.execute("INSERT INTO historico_agendamento_endermo (cliente_id, data) VALUES (?,?)", (cliente_id, databr))
    conn.commit()
    conn.close()

def excluir_agendamento(data_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM historico_agendamento_endermo WHERE id = ?", (data_id,))
    conn.commit()
    conn.close()

def buscar_clientes(nome):
    conn = get_db_connection()
    # LIKE faz a busca parcial; LOWER evita problema de maiúsculas/minúsculas
    clientes = conn.execute("""
        SELECT * FROM cliente_endermo
        WHERE LOWER(nome) LIKE ?
    """, ('%' + nome.lower() + '%',)).fetchall()
    conn.close()
    return clientes
