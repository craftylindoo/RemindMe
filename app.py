from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

def get_db():
    conexao = sqlite3.connect('listadelembretes')
    conexao.row_factory = sqlite3.Row
    return conexao

@app.route('/lembretes',methods=['GET'])
def listar_lembretes():
    conexao = get_db()
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM lembretes')
    lembretes = [dict(row) for row in cursor.fetchall()]
    conexao.close()
    return jsonify(lembretes)

@app.route('/lembretes/<int:id>',methods=['GET'])
def buscar_lembretes(id):
    conexao = get_db()
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM lembretes WHERE id = ?', (id,))
    row = cursor.fetchone()
    conexao.close()
    if row:
        return jsonify(dict(row))
    return jsonify({'erro': 'lembrete nao encontrado'}), 404

@app.route('/lembretes',methods=['POST'])
def criar_lembrete():
    dados = request.get_json()
    conexao = get_db()
    cursor = conexao.cursor()
    cursor.execute('''INSERT INTO lembretes (compromisso, data_de_registro, data_do_compromisso, horario_do_compromisso)
    VALUES (?, ?, ?, ?)''', (dados['compromisso'], dados['data_de_registro'], dados['data_do_compromisso'], dados['horario_do_compromisso'] ))
    conexao.commit()
    novo_id = cursor.lastrowid
    conexao.close()
    return jsonify({'id': novo_id, 'mensagem': 'lembrete criado!'}), 201

@app.route('/lembretes/<int:id>',methods=['DELETE'])
def deletar_lembrete(id):
    conexao = get_db()
    cursor = conexao.cursor()
    cursor.execute('DELETE FROM lembretes WHERE id = ?', (id,))
    conexao.commit()
    conexao.close()
    if cursor.rowcount > 0:
        return jsonify({'mensagem': 'lembrete deletado!'})
    return jsonify({'erro': 'lembrete nao encontrado :('}), 404

@app.route('/lembretes/<int:id>',methods=['PUT'])
def atualizar_lembretes(id):
    dados = request.get_json()
    conexao = get_db()
    cursor =  conexao.cursor()
    cursor.execute('''UPDATE lembretes
                   SET compromisso = ?, data_do_compromisso = ?, horario_do_compromisso = ?
                   WHERE id = ?''',
                   (dados['compromisso'], dados['data_do_compromisso'], dados['horario_do_compromisso'], id))
    conexao.commit()
    conexao.close()
    if cursor.rowcount > 0:
        return jsonify({'mensagem': 'lembrete atualizado!'})
    return jsonify({'erro': 'ocorreu um erro :('}), 404

app.run(port=5000,host='localhost',debug=True)
