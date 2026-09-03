import hashlib
import sqlite3

def criptografar_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def conectar_banco():
    # Como o database.db está na raiz do projeto (fora de src), 
    # usamos "../database.db" para voltar uma pasta e achar o arquivo
    return sqlite3.connect("../database.db")

def inicializar_banco():
    # Garante que a tabela 'usuarios' existe assim que o app abre
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
    """)
    conexao.commit()
    conexao.close()
    
def criacao_persona():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS persona (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            especialidade TEXT NOT NULL,
            cor_cabelo TEXT NOT NULL,
            cor_persona TEXT NOT NULL
        )
    """)
    conexao.commit()  # Adicionado para salvar a tabela
    conexao.close()   # Adicionado para fechar a conexão
    
def cadastrar_usuario(usuario, senha):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO usuarios (nome, senha) VALUES (?, ?)", (usuario, senha))
    conexao.commit()
    conexao.close()
    
def atualizar_usuario(usuario, nova_senha):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    # Ordem corrigida: primeiro a nova senha, depois o nome do usuário
    cursor.execute("UPDATE usuarios SET senha = ? WHERE nome = ?", (nova_senha, usuario))
    conexao.commit()
    conexao.close()
    
def deletar_usuario(usuario):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM usuarios WHERE nome = ?", (usuario,))
    conexao.commit()
    conexao.close()