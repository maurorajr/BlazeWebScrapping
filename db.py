import sqlite3

def connect_db():
    """Conecta ao banco de dados SQLite."""
    conn = sqlite3.connect('D:/apps/sqlite/WebScraper/database.db')
    return conn

def create_tables():
    """Cria tabelas iniciais no banco de dados."""
    conn = connect_db()
    cursor = conn.cursor()

    # Exemplo de criação de tabela
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS configuracoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            valor TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Chame create_tables para criar a tabela ao iniciar o projeto
if __name__ == '__main__':
    create_tables()
