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
    CREATE TABLE IF NOT EXISTS clientes_massagem (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        status_massagem BOOLEAN DEFAULT FALSE,
        checkins_massagem INTEGER DEFAULT 0
    )
    ''')
    conn.execute('''
    CREATE TABLE IF NOT EXISTS clientes_limpeza (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        status_limpeza BOOLEAN DEFAULT FALSE,
        checkins_limpeza INTEGER DEFAULT 0,
        historico_agendamento TEXT
    )
    ''')
    conn.execute('''
    CREATE TABLE IF NOT EXISTS clientes_ventosa (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        status_ventosa BOOLEAN DEFAULT FALSE,
        checkins_ventosa INTEGER DEFAULT 0,
        historico_agendamento TEXT
    )
    ''')
    conn.execute('''
    CREATE TABLE IF NOT EXISTS clientes_flacidez (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        status_flacidez BOOLEAN DEFAULT FALSE,
        checkins_flacidez INTEGER DEFAULT 0,
        historico_agendamento TEXT
    )
    ''')
    conn.execute('''
    CREATE TABLE IF NOT EXISTS clientes_endermo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        status_endermo BOOLEAN DEFAULT FALSE,
        checkins_endermo INTEGER DEFAULT 0,
        historico_agendamento TEXT
    )
    ''')
    conn.execute('''
    CREATE TABLE IF NOT EXISTS clientes_detox (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        status_detox BOOLEAN DEFAULT FALSE,
        checkins_detox INTEGER DEFAULT 0,
        historico_agendamento TEXT
    )
    ''')





    #checkins
    conn.execute('''
    CREATE TABLE IF NOT EXISTS checkins_massagem (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER,
        data TEXT,
        FOREIGN KEY(cliente_id) REFERENCES clientes(id)
    )
    ''')
    conn.execute('''
    CREATE TABLE IF NOT EXISTS checkins_limpeza (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER,
        data TEXT,
        FOREIGN KEY(cliente_id) REFERENCES clientes(id)
    )
    ''')
    conn.execute('''
    CREATE TABLE IF NOT EXISTS checkins_ventosa (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER,
        data TEXT,
        FOREIGN KEY(cliente_id) REFERENCES clientes(id)
    )
    ''')
    conn.execute('''
    CREATE TABLE IF NOT EXISTS checkins_flacidez (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER,
        data TEXT,
        FOREIGN KEY(cliente_id) REFERENCES clientes(id)
    )
    ''')
    conn.execute('''
    CREATE TABLE IF NOT EXISTS checkins_endermo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER,
        data TEXT,
        FOREIGN KEY(cliente_id) REFERENCES clientes(id)
    )
    ''')
    conn.execute('''
    CREATE TABLE IF NOT EXISTS checkins_detox (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER,
        data TEXT,
        FOREIGN KEY(cliente_id) REFERENCES clientes(id)
    )
    ''')

    conn.commit()
    conn.close()