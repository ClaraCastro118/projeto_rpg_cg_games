import hashlib
import sqlite3

def criptografar_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def conectar_banco():
    # Como o database.db está na raiz do projeto (fora de src), 
    # usamos "../database.db" para voltar uma pasta e achar o arquivo
    return sqlite3.connect("../database.db")

def inicializar_banco():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    # Tabela de Usuários
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
    """)
    
    # Tabela de Persona (vinculada ao usuário pelo usuario_id)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS persona (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            nome TEXT NOT NULL,
            especialidade TEXT NOT NULL,
            cor_cabelo TEXT NOT NULL,
            cor_persona TEXT NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
    """)
    
    conexao.commit()
    conexao.close()
    
def cadastrar_usuario(usuario, senha):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO usuarios (nome, senha) VALUES (?, ?)", (usuario, senha))
    conexao.commit()
    conexao.close()
    
def atualizar_usuario(usuario, nova_senha):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("UPDATE usuarios SET senha = ? WHERE nome = ?", (nova_senha, usuario))
    conexao.commit()
    conexao.close()
    
def deletar_usuario(usuario):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM usuarios WHERE nome = ?", (usuario,))
    conexao.commit()
    conexao.close()

# Funções de Gerenciamento de Persona 
def criar_persona(usuario_id, nome, especialidade, cor_cabelo, cor_persona):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO persona (usuario_id, nome, especialidade, cor_cabelo, cor_persona) 
        VALUES (?, ?, ?, ?, ?)
    """, (usuario_id, nome, especialidade, cor_cabelo, cor_persona))
    conexao.commit()
    conexao.close()

def buscar_personas_usuario(usuario_id):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM persona WHERE usuario_id = ?", (usuario_id,))
    resultados = cursor.fetchall()
    conexao.close()
    return resultados

def atualizar_persona(persona_id, especialidade, cor_cabelo, cor_persona):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("""
        UPDATE persona 
        SET especialidade = ?, cor_cabelo = ?, cor_persona = ? 
        WHERE id = ?
    """, (especialidade, cor_cabelo, cor_persona, persona_id))
    conexao.commit()
    conexao.close()

def deletar_persona(persona_id):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM persona WHERE id = ?", (persona_id,))
    conexao.commit()
    conexao.close()