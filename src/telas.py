import hashlib
import sqlite3
import tkinter as tk
from tkinter import messagebox

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
            nome TEXT NOT NULL,
            senha TEXT NOT NULL
        )
    """)
    conexao.commit()
    conexao.close()

def abrir_tela_principal():
    # Já cria a tabela assim que a tela abre, evitando o erro
    inicializar_banco()
    
    janela_login = tk.Tk()
    janela_login.title("CB Games - Login e Cadastro")
    janela_login.geometry("400x350")
    
    titulo = tk.Label(janela_login, text="CB Games - RPG", font=("Arial", 16, "bold"))
    titulo.pack(pady=20)
    
    # Campo de Usuário
    tk.Label(janela_login, text="Nome de Usuário:").pack()
    entry_usuario = tk.Entry(janela_login, width=30)
    entry_usuario.pack(pady=5)
    
    # Campo de Senha
    tk.Label(janela_login, text="Senha:").pack()
    entry_senha = tk.Entry(janela_login, show="*", width=30)
    entry_senha.pack(pady=5)
    
    def acao_entrar():
        usuario = entry_usuario.get()
        senha_pura = entry_senha.get()
        
        if not usuario or not senha_pura:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return
            
        senha_segura = criptografar_senha(senha_pura)
        
        conexao = conectar_banco()
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE nome = ? AND senha = ?", (usuario, senha_segura))
        resultado = cursor.fetchone()
        conexao.close()
        
        if resultado:
            messagebox.showinfo("Sucesso", "Login bem-sucedido! Bem-vindo ao jogo.")
            janela_login.destroy()
        else:
            messagebox.showerror("Acesso Negado", "Usuário não encontrado ou senha incorreta. Clique em 'Cadastrar' se não tiver uma conta.")

    def acao_cadastrar():
        usuario = entry_usuario.get()
        senha_pura = entry_senha.get()
        
        if not usuario or not senha_pura:
            messagebox.showerror("Erro", "Preencha todos os campos para cadastrar!")
            return
            
        conexao = conectar_banco()
        cursor = conexao.cursor()
        
        cursor.execute("SELECT * FROM usuarios WHERE nome = ?", (usuario,))
        usuario_existe = cursor.fetchone()
        
        if usuario_existe:
            conexao.close()
            messagebox.showwarning("Aviso", "Este usuário já é cadastrado! Tente fazer o login.")
            return
            
        senha_segura = criptografar_senha(senha_pura)
        try:
            cursor.execute("INSERT INTO usuarios (nome, senha) VALUES (?, ?)", (usuario, senha_segura))
            conexao.commit()
            conexao.close()
            messagebox.showinfo("Sucesso", "Usuário cadastrado com segurança! Agora você já pode entrar.")
        except Exception as e:
            conexao.close()
            messagebox.showerror("Erro", f"Erro ao cadastrar: {e}")

    frame_botoes = tk.Frame(janela_login)
    frame_botoes.pack(pady=20)
    
    btn_entrar = tk.Button(frame_botoes, text="Entrar", command=acao_entrar, bg="blue", fg="white", width=12)
    btn_entrar.grid(row=0, column=0, padx=10)
    
    btn_cadastrar = tk.Button(frame_botoes, text="Cadastrar", command=acao_cadastrar, bg="green", fg="white", width=12)
    btn_cadastrar.grid(row=0, column=1, padx=10)
    
    janela_login.mainloop()

if __name__ == "__main__":
    abrir_tela_principal()

