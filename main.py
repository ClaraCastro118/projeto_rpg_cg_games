import hashlib
import sqlite3
import tkinter as tk
from tkinter import messagebox


# 1. Função para criptografar a senha (Gera um Hash seguro)
def criptografar_senha(senha):
  # Transforma a senha em bytes e aplica o algoritmo SHA-256
  return hashlib.sha256(senha.encode()).hexdigest()


# 2. Configurando o Banco de Dados SQLite
def inicializar_banco():
  conexao = sqlite3.connect("database.db")
  cursor = conexao.cursor()
  # Tabela de usuários
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            senha TEXT NOT NULL
        )
    """)
  conexao.commit()
  conexao.close()


# Executa a criação do banco ao iniciar
inicializar_banco()

# 3. Interface Gráfica Básica com Tkinter
app = tk.Tk()
app.title("CB Games - Sistema de Login e Criação de Personagens")
app.geometry("400x350")

titulo = tk.Label(app, text="CB Games - RPG", font=("Arial", 16, "bold"))
titulo.pack(pady=20)

# Campo de Usuário
lbl_usuario = tk.Label(app, text="Nome de Usuário:")
lbl_usuario.pack()
entry_usuario = tk.Entry(app, width=30)
entry_usuario.pack(pady=5)

# Campo de Senha
lbl_senha = tk.Label(app, text="Senha:")
lbl_senha.pack()
entry_senha = tk.Entry(app, show="*", width=30)
entry_senha.pack(pady=5)


def acao_cadastrar():
  usuario = entry_usuario.get()
  senha_pura = entry_senha.get()

  if not usuario or not senha_pura:
    messagebox.showerror("Erro", "Preencha todos os campos!")
    return

  # Criptografamos a senha antes de mandar para o banco
  senha_segura = criptografar_senha(senha_pura)

  # Salvando no banco de dados
  try:
    conexao = sqlite3.connect("database.db")
    cursor = conexao.cursor()
    cursor.execute(
        "INSERT INTO usuarios (nome, senha) VALUES (?, ?)",
        (usuario, senha_segura),
    )
    conexao.commit()
    conexao.close()
    messagebox.showinfo("Sucesso", "Usuário cadastrado com segurança!")
  except Exception as e:
    messagebox.showerror("Erro", f"Erro ao cadastrar: {e}")


btn_cadastrar = tk.Button(
    app,
    text="Cadastrar",
    command=acao_cadastrar,
    bg="green",
    fg="white",
    width=20,
)
btn_cadastrar.pack(pady=15)

app.mainloop()

