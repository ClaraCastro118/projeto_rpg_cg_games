from database import conectar_banco, criptografar_senha

def inicializar_banco():
    # Garante que a tabela 'usuarios' existe assim que o app abre
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            senha TEXT NOT NULL check (length(senha) = 20)
        )
    """)
    conexao.commit()
    conexao.close()
    
def criacao_persona():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS persona (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL check (length(nome) = 20),
        especialidade TEXT NOT NULL ,
        cor_cabelo TEXT NOT NULL check (length(cor_cabelo) = 15),
        cor_persona TEXT NOT NULL check (length(cor_persona) = 15)
        )
                   """)

    
def cadastrar_usuario(usuario, senha):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO usuarios (nome, senha) VALUES (?, ?)", (usuario, senha))
    conexao.commit()
    conexao.close()
    
def atualizar_usuario(usuario, nova_senha):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("UPDATE usuarios set senha = ? WHERE nome = ?", (usuario, nova_senha))
    conexao.commit()
    conexao.close()
    
def deletar_usuario(usuario):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM usuarios WHERE nome = ?", (usuario,))
    conexao.commit()
    conexao.close()
    
