from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

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

init_db()

@app.route('/')
def home_page():
    return render_template('index.html')  # OU '<h2>Minha página lindíssima de Python</h2>'

@app.route('/doar', methods=["POST"])
def doar():
    dados = request.get_json()

    titulo = dados.get('titulo')
    categoria = dados.get('categoria')
    autor = dados.get('autor')
    imagen = dados.get('imagen') 

    if not all([titulo, categoria, autor, imagen]):  
        return jsonify({'erro': 'Todos os campos são obrigatórios'}), 400

    with sqlite3.connect('database.db') as conn:
        conn.execute("""INSERT INTO livros (titulo, categoria, autor, imagen)
                    VALUES (?,?,?,?)""", (titulo, categoria, autor, imagen)) 
        conn.commit()

    return jsonify({"mensagem": "Livro cadastrado com sucesso"}), 201

@app.route('/livros', methods=['GET'])
def listar_livros():
    with sqlite3.connect('database.db') as con:
        livros = con.execute("SELECT * FROM livros").fetchall()

    livros_formatados = [
        {"id": livro[0], "titulo": livro[1], "categoria": livro[2], "autor": livro[3], "imagen": livro[4]}
        for livro in livros
    ]

    return jsonify(livros_formatados)

@app.route('/livros/<int:livro_id>', methods=['DELETE'])
def deletar_livro(livro_id):
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM livros WHERE id = ?", (livro_id,))
        conn.commit()

    if cursor.rowcount == 0:
        return jsonify({"erro": "Livro não encontrado"}), 404

    return jsonify({"mensagem": "Livro excluído com sucesso"}), 200

if __name__ == '__main__':
    app.run(debug=True)
