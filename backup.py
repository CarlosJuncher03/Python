from PyQt5.QtCore import QObject, pyqtSignal
import mysql.connector
import os
import subprocess
import datetime
from tkinter import filedialog

historico_backup = []

class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(str)
    progress = pyqtSignal(int)

class backup_mysql(QObject):
    def __init__(self):
        super().__init__()
        self.signals = WorkerSignals()

    def fazer_backup(self, ip_maquina, local_salvo, nome_arquivo):
        # Lógica para fazer o backup aqui...

        # Adicionando entrada ao histórico
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        entrada_historico = {
            'ip_maquina': ip_maquina,
            'local_salvo': local_salvo,
            'nome_arquivo': nome_arquivo,
            'data': timestamp
        }

        historico_backup.append(entrada_historico)

    def local_pasta(self):
        self.local = filedialog.askdirectory()
        if self.local:
            print(f'Pasta selecionada: {self.local}')
        return self.local

    def tempo(self):
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    def backup(self, ip, porta, local, banco, usuario, senha):
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            arquivo_backup = os.path.join(local, f'{timestamp}.sql')
            comando = f'mysqldump -h {ip} -P {porta} -u {usuario} -p{senha} --column-statistics=0 {banco} > "{arquivo_backup}"'
            # Executa o comando no terminal
            subprocess.run(comando, shell=True, check=True)

            # Chama a função fazer_backup para adicionar ao histórico
            self.fazer_backup(ip, local, timestamp)

            return f"Backup do banco {banco} realizado com sucesso"
        except subprocess.CalledProcessError as erro:
            return f"Erro no backup: {erro}"
        except Exception as e:
            return f"Erro inesperado: {e}"

    def testar_conexao(self, ip, porta, banco, usuario, senha):
        try:
            # Tenta estabelecer uma conexão com o banco de dados
            conexao = mysql.connector.connect(
                host=ip,
                port=porta,
                user=usuario,
                database=banco,
                password=senha
            )

            # Se a conexão for bem-sucedida, retorna um dicionário com sucesso=True
            self.signals.finished.emit()
            conexao.close()
            return {'success': True}

        except mysql.connector.Error as e:
            # Se houver um erro, retorna um dicionário com sucesso=False e a mensagem de erro
            self.signals.error.emit(f"Erro ao testar a conexão: {str(e)}")
            return {'success': False, 'error_message': str(e)}
