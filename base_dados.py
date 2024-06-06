import sqlite3

# Base de dados
sql = """
CREATE TABLE IF NOT EXISTS
    Clientes (
        id_cliente INTEGER PRIMARY KEY,
        nome TEXT NOT NULL,
        morada TEXT NOT NULL,
        telefone TEXT NOT NULL
    );

CREATE TABLE IF NOT EXISTS
    Hamburguers (
        nome_hamburguer TEXT PRIMARY KEY,
        ingredientes TEXT NOT NULL,
        preco REAL NOT NULL
    );

CREATE TABLE IF NOT EXISTS
    Pedidos (
        id_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
        id_cliente INTEGER NOT NULL,
        nome_hamburguer TEXT NOT NULL,
        quantidade INTEGER NOT NULL,
        tamanho TEXT CHECK (tamanho IN ('infantil', 'normal', 'duplo')),
        data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
        valor_total REAL NOT NULL,
        FOREIGN KEY (id_cliente) REFERENCES Clientes(id_cliente),
        FOREIGN KEY (nome_hamburguer) REFERENCES Hamburguers(nome_hamburguer)
    );
"""

data_hamburguers = [
    ('Hamburguer Simples', 'Pão, Carne de Vaca, Pickles, Cebola, Ketchup, Mostarda', 5.99),
    ('Cheeseburguer', 'Pão, Carne de Vaca, Queijo Cheddar, Pickles, Cebola, Ketchup, Mostarda', 6.99),
    ('Big Mac', 'Pão, Carne de Vaca, Queijo Cheddar, Pickles, Alface, Molho Irresistível', 7.99),
    ('CBO', 'Pão Macio, Panado de Frango, Cebola Estaladiça, Bacon, Queijo, Bacon', 8.99),
    ('McRoyal Bacon', 'Pão, Carne de Vaca, Bacon, Molho McBacon', 6.49),
    ('McRoyal Cheese', 'Pão, Queijo Cheddar, Pickles, Cebola, Ketchup, Mostarda', 7.49),
    ('Mc Chicken', 'Pão, Filete de Frango, Alface, Maionese', 5.99)
]

with sqlite3.connect('hamburgueria.db') as conn:
    cursor = conn.cursor()
    cursor.executescript(sql)
    
    cursor.executemany('INSERT OR REPLACE INTO Hamburguers (nome_hamburguer, ingredientes, preco) VALUES (?,?,?)', data_hamburguers)
    conn.commit()
