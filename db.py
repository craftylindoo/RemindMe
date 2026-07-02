import sqlite3

conexao = sqlite3.connect('listadelembretes')
cursor = conexao.cursor()

cursor.execute("DROP TABLE IF EXISTS lembretes")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS lembretes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        compromisso TEXT NOT NULL,
        data_de_registro TEXT NOT NULL,
        data_do_compromisso TEXT NOT NULL,
        horario_do_compromisso TEXT NOT NULL
    )
""")

cursor.executemany("""
INSERT INTO lembretes 
(compromisso, data_de_registro, data_do_compromisso, horario_do_compromisso)
VALUES (?, ?, ?, ?)
""", [
    ('Ir ao Petshop', '23/03', 'Toda quarta', '14:00'),
    ('Fazer compras', '08/07', '10/07', '20:00'),
    ('Ir à academia ', '13/02', 'Segunda, Quarta, Sexta', '07:00'),
    ('Ir a aula de ingles', '02/04', 'Terça, Quinta', '10:00'),
    ('Sair com o cachorro', '23/03', 'Todos os dias', '15:30'),
    ('Reunião', '10/07', '18/07', '16:00')
    
])

conexao.commit()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
print("Tabelas no banco:", cursor.fetchall())

cursor.execute("SELECT * FROM lembretes")
print("Dados na tabela:", cursor.fetchall())
