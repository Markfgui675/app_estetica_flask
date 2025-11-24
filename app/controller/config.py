from app.model.model import get_db_connection


detox = 5
endermo = 7
flacidez = 7
limpeza = 6
massagem = 5
ventosa = 5

def update_checkin(checkin):
    conn = get_db_connection()
    conn.execute("UPDATE config_massagem SET checkin = ?", (checkin))
    conn.commit()
    conn.close()
