from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DATABASE = "hamburgueria.db"

def query_db(query, args=(), one=False):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(query, args)
    rv = cursor.fetchall()
    conn.commit()
    conn.close()
    return (rv[0] if rv else None) if one else rv

@app.route("/Clientes", methods=["POST"])
def adc_cliente():
    data = request.get_json()
    nome = data["nome"]
    morada = data["morada"]
    telefone = data["telefone"]
    query_db("INSERT INTO Clientes (nome, morada, telefone) VALUES (?, ?, ?)", (nome, morada, telefone))
    return jsonify({"message": "Cliente adicionado com sucesso!"}), 201

@app.route("/Hamburguers", methods=["POST"])
def adc_hamburguer():
    data = request.get_json()
    nome_hamburguer = data["nome_hamburguer"]
    ingredientes = data["ingredientes"]
    preco = data["preco"]  # Adicionando a coluna "preco"
    query_db("INSERT INTO Hamburguers (nome_hamburguer, ingredientes, preco) VALUES (?, ?, ?)", [nome_hamburguer, ingredientes, preco])
    return jsonify({"message": "Hamburguer adicionado com sucesso!"}), 201

@app.route("/Pedidos", methods=["POST"])
def adc_pedido():
    data = request.get_json()
    id_cliente = data["id_cliente"]
    nome_hamburguer = data["nome_hamburguer"]
    quantidade = data["quantidade"]
    tamanho = data["tamanho"]
    valor_total = data["valor_total"]
    query_db("INSERT INTO Pedidos (id_cliente, nome_hamburguer, quantidade, tamanho, valor_total) VALUES (?, ?, ?, ?, ?)",
             [id_cliente, nome_hamburguer, quantidade, tamanho, valor_total])
    return jsonify({"message": "Pedido adicionado com sucesso!"}), 201

@app.route("/Clientes", methods=["GET"])
def get_clientes():
    clientes = query_db("SELECT * FROM Clientes")
    return jsonify(clientes)

@app.route("/Hamburguers", methods=["GET"])
def get_hamburguers():
    hamburguers = query_db("SELECT * FROM Hamburguers")
    return jsonify(hamburguers)

@app.route("/Pedidos", methods=["GET"])
def get_pedidos():
    pedidos = query_db("SELECT * FROM Pedidos")
    return jsonify(pedidos)

if __name__ == "__main__":
    app.run(debug=True)
