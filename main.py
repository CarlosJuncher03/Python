from flask import Flask, render_template, request, jsonify, url_for, redirect
from backup import backup_mysql

app = Flask(__name__)
instancia_backup = backup_mysql()

@app.route('/andamento')
def andamento():
    return redirect(url_for('andamento'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sucesso_backup')
def sucesso_backup():
    return render_template('sucesso_backup.html')

@app.route('/', methods=['POST'])
def processar_acao():
    global instancia_backup
    acao = request.form.get('acao')
    
    try:
        if acao == 'iniciar_backup':
            ip = request.form.get('ipBanco')
            porta = request.form.get('portaBanco')
            local = request.form.get('campoLocalSalvar')
            banco = request.form.get('nomeBanco')
            usuario = request.form.get('usuario')
            senha = request.form.get('senha')

            if not all([ip, porta, local, banco, usuario, senha]):
                raise ValueError("Por favor, preencha todos os campos.")

            andamento() 

            resultado = instancia_backup.backup(ip, porta, local, banco, usuario, senha)

            return render_template('sucesso_backup.html', resultado=resultado)

        elif acao == 'escolher_pasta':
            local_selecionado = instancia_backup.local_pasta()
            return jsonify({'local_selecionado': local_selecionado})

        elif acao == 'testar_conexao':
            ip = request.form.get('ipBanco')
            porta = request.form.get("portaBanco")
            banco = request.form.get("nomeBanco")
            usuario = request.form.get("usuario")
            senha = request.form.get("senha")

            if not all([ip, porta, banco, usuario, senha]):
                raise ValueError("Por favor, preencha todos os campos.")

            resultado = instancia_backup.testar_conexao(ip, porta, banco, usuario, senha)

            return render_template('resultado_teste_conexao.html', resultado=resultado)

        else:
            return "Nenhuma ação válida especificada."

    except ValueError as e:
        return render_template('erro.html', mensagem=str(e))

if __name__ == '__main__':
    app.run(debug=False)
