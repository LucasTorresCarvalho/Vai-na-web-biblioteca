from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Função para inicializar o banco de dados SQLite
def init_db():
    with sqlite3.connect('database.db') as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS livros(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    categoria TEXT NOT NULL,
                    autor TEXT NOT NULL,
                    imagen TEXT NOT NULL
                    )""")
        print("Banco de dados criado!!")

# Chama a função para criar o banco de dados ao iniciar o servidor
init_db()

@app.route('/')
def home_page():
    return '<h2>Minha página lindíssima de Python</h2>'

@app.route('/doar', methods=["POST"])
def doar():
    dados = request.get_json()

    titulo = dados.get('titulo')
    categoria = dados.get('categoria')
    autor = dados.get('autor')
    imagen = dados.get('imagen')  # 🔥 Pegamos 'imagen', que é o nome da coluna no banco

    if not all([titulo, categoria, autor, imagen]):  
        return jsonify({'erro': 'Todos os campos são obrigatórios'}), 400

    with sqlite3.connect('database.db') as conn:
        conn.execute("""INSERT INTO livros (titulo, categoria, autor, imagen)
                    VALUES (?,?,?,?)""", (titulo, categoria, autor, imagen))  # 🔥 Agora funciona
        conn.commit()

        return jsonify({"mensagem": "Livro cadastrado com sucesso"}), 201


# ✅ Rota corrigida e movida para fora da função doar()
@app.route('/livros', methods=['GET'])
def listar_livros():
    with sqlite3.connect('database.db') as con:
        livros = con.execute("SELECT * FROM livros").fetchall()

    livros_formatados = []

    for livro in livros:
        dicionario_livros = {
            "id": livro[0],
            "titulo": livro[1],
            "categoria": livro[2],
            "autor": livro[3],
            "imagen": livro[4]
        }
        livros_formatados.append(dicionario_livros)

    return jsonify(livros_formatados)  # ✅ Agora está fora do loop

if __name__ == '__main__':
    app.run(debug=True)  # ✅ Corrigido


