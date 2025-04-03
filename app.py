from flask import Flask, request, jsonify, render_template
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permite qualquer origem para testes

# Função para inicializar o banco de dados
def init_db():
    try:
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS livros(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            titulo TEXT NOT NULL,
                            categoria TEXT NOT NULL,
                            autor TEXT NOT NULL,
                            imagen TEXT NOT NULL
                            )""")
            conn.commit()
            cursor.close()
        print("Banco de dados criado!!")
    except sqlite3.Error as e:
        print(f"Erro ao criar o banco de dados: {str(e)}")

init_db()
@app.route('/')
def homepage():
    # Renderiza um template HTML chamado 'index.html'.
    return render_template('index.html')

@app.route('/doar', methods=["POST"])
def doar():
    try:
        dados = request.get_json()
        if not dados:
            return jsonify({'erro': 'Dados inválidos ou ausentes'}), 400

        titulo = dados.get('titulo')
        categoria = dados.get('categoria')
        autor = dados.get('autor')
        imagen = dados.get('imagen')

        if not all([titulo, categoria, autor, imagen]):
            return jsonify({'erro': 'Todos os campos são obrigatórios'}), 400

        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute("""INSERT INTO livros (titulo, categoria, autor, imagen)
                            VALUES (?,?,?,?)""", (titulo, categoria, autor, imagen))
            conn.commit()
            cursor.close()

        return jsonify({"mensagem": "Livro cadastrado com sucesso"}), 201
    except sqlite3.Error:
        return jsonify({"erro": "Erro ao salvar no banco de dados."}), 500
    except Exception:
        return jsonify({"erro": "Ocorreu um erro interno. Tente novamente mais tarde."}), 500
    
@app.route('/livros/<int:livro_id>', methods=['DELETE'])
def deletar_livro(livro_id):
    try:
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM livros WHERE id = ?", (livro_id,))
            conn.commit()
            linhas_afetadas = cursor.rowcount  # Conta quantas linhas foram afetadas
            cursor.close()

        if linhas_afetadas == 0:
            return jsonify({"erro": "Livro não encontrado"}), 404

        return jsonify({"mensagem": "Livro excluído com sucesso"}), 200
    except sqlite3.Error:
        return jsonify({"erro": "Erro ao excluir livro do banco de dados."}), 500
    except Exception:
        return jsonify({"erro": "Ocorreu um erro interno. Tente novamente mais tarde."}), 500

    
@app.route('/livros', methods=['GET'])
def listar_livros():
    # Conecta ao banco de dados e recupera todos os registros da tabela 'livros'.
    with sqlite3.connect('database.db') as conn:
        livros = conn.execute("SELECT * FROM livros").fetchall()

    # Lista para armazenar os livros formatados.
    livros_formatados = []

    # Formata cada livro como um dicionário e adiciona à lista.
    for livro in livros:
        dicionario_livros = {
            "id": livro[0],
            "titulo": livro[1],
            "categoria": livro[2],
            "autor": livro[3],
            "imagem_url": livro[4]
        }
        livros_formatados.append(dicionario_livros)

        

    # Retorna a lista de livros no formato JSON.
    return jsonify(livros_formatados)

if __name__ == '__main__':
    app.run(debug=True)  # Permite acesso externo
