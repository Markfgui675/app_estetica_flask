from app.model.model import get_db_connection


detox = 5
endermo = 7
flacidez = 7
limpeza = 6
massagem = 5
ventosa = 5

def init():
    
    conn = get_db_connection()

    conn.execute("INSERT INTO config_massagem (checkin) VALUES (?)", (massagem,))
    conn.execute("INSERT INTO config_ventosa (checkin) VALUES (?)", (ventosa,))
    conn.execute("INSERT INTO config_limpeza (checkin) VALUES (?)", (limpeza,))
    conn.execute("INSERT INTO config_flacidez (checkin) VALUES (?)", (flacidez,))
    conn.execute("INSERT INTO config_endermo (checkin) VALUES (?)", (endermo,))
    conn.execute("INSERT INTO config_detox (checkin) VALUES (?)", (detox,))
    conn.commit()
    conn.close()

def update_checkin(checkin):
    conn = get_db_connection()
    conn.execute("UPDATE config_massagem SET checkin = ?", (checkin))
    conn.commit()
    conn.close()
