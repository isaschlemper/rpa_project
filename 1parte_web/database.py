import sqlite3

DB_PATH = "1parte_web/techsolutions.db"

def conectar():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            nome          TEXT    NOT NULL,
            email         TEXT    NOT NULL,
            telefone      TEXT    NOT NULL,
            endereco      TEXT,
            data_cadastro TEXT    DEFAULT (date('now'))
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS faturas (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id      INTEGER NOT NULL,
            valor           REAL    NOT NULL,
            data_vencimento TEXT    NOT NULL,
            status          TEXT    DEFAULT 'pendente',
            data_emissao    TEXT    DEFAULT (date('now')),
            FOREIGN KEY (cliente_id) REFERENCES clientes(id)
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Banco de dados criado com sucesso!")

def listar_faturas_pendentes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT f.id, c.nome, c.email, c.telefone, f.valor, f.data_vencimento, f.status
        FROM faturas f
        JOIN clientes c ON f.cliente_id = c.id
        WHERE f.status = 'pendente'
        ORDER BY f.data_vencimento
    """)
    faturas = cursor.fetchall()
    conn.close()
    return [dict(f) for f in faturas]

def listar_todas_faturas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT f.id, c.nome, c.email, c.telefone, f.valor, f.data_vencimento, f.status, f.data_emissao
        FROM faturas f
        JOIN clientes c ON f.cliente_id = c.id
        ORDER BY f.data_vencimento
    """)
    faturas = cursor.fetchall()
    conn.close()
    return [dict(f) for f in faturas]

def atualizar_status_fatura(fatura_id, novo_status):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE faturas SET status = ? WHERE id = ?",
        (novo_status, fatura_id)
    )
    conn.commit()
    conn.close()

if __name__ == "__main__":
    criar_tabelas()