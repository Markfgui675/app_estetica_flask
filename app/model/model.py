import sqlite3

# Função para conexão com banco
def get_db_connection():
    conn = sqlite3.connect('checkins.db')
    conn.row_factory = sqlite3.Row
    return conn

# Criação das tabelas
def init_db():
    conn = get_db_connection()

    #clientes
    conn.execute('''
    CREATE TABLE IF NOT EXISTS cliente_massagem (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        status BOOLEAN DEFAULT FALSE,
        checkins INTEGER DEFAULT 0
    )
    ''')
    conn.execute('''
    CREATE TABLE IF NOT EXISTS cliente_limpeza (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        status BOOLEAN DEFAULT FALSE,
        checkins INTEGER DEFAULT 0
    )
    ''')
    conn.execute('''
    CREATE TABLE IF NOT EXISTS cliente_ventosa (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        status BOOLEAN DEFAULT FALSE,
        checkins INTEGER DEFAULT 0
    )
    ''')
    conn.execute('''
    CREATE TABLE IF NOT EXISTS cliente_flacidez (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        status BOOLEAN DEFAULT FALSE,
        checkins INTEGER DEFAULT 0
    )
    ''')
    conn.execute('''
    CREATE TABLE IF NOT EXISTS cliente_endermo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        status BOOLEAN DEFAULT FALSE,
        checkins INTEGER DEFAULT 0
    )
    ''')
    conn.execute('''
    CREATE TABLE IF NOT EXISTS cliente_detox (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        status BOOLEAN DEFAULT FALSE,
        checkins INTEGER DEFAULT 0
    )
    ''')





    #checkins
    conn.execute('''
    CREATE TABLE IF NOT EXISTS checkin_massagem (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER,
        data DATETIME,
        FOREIGN KEY(cliente_id) REFERENCES clientes(id)
    )
    ''')
    conn.execute('''
    CREATE TABLE IF NOT EXISTS checkin_limpeza (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER,
        data DATETIME,
        FOREIGN KEY(cliente_id) REFERENCES clientes(id)
    )
    ''')
    conn.execute('''
    CREATE TABLE IF NOT EXISTS checkin_ventosa (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER,
        data DATETIME,
        FOREIGN KEY(cliente_id) REFERENCES clientes(id)
    )
    ''')
    conn.execute('''
    CREATE TABLE IF NOT EXISTS checkin_flacidez (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER,
        data DATETIME,
        FOREIGN KEY(cliente_id) REFERENCES clientes(id)
    )
    ''')
    conn.execute('''
    CREATE TABLE IF NOT EXISTS checkin_endermo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER,
        data DATETIME,
        FOREIGN KEY(cliente_id) REFERENCES clientes(id)
    )
    ''')
    conn.execute('''
    CREATE TABLE IF NOT EXISTS checkin_detox (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER,
        data DATETIME,
        FOREIGN KEY(cliente_id) REFERENCES clientes(id)
    )
    ''')

    

    #historico_agendamento
    conn.execute('''
    CREATE TABLE IF NOT EXISTS historico_agendamento_massagem (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER,
        data DATETIME,
        FOREIGN KEY(cliente_id) REFERENCES clientes(id)
    )
    ''')

    conn.commit()
    conn.close()