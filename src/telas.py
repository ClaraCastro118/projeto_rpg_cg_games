import tkinter as tk
from tkinter import messagebox
from database import inicializar_banco, conectar_banco, criptografar_senha, deletar_persona

def abrir_tela_personalizacao(usuario_id, nome_usuario):
    """Abre a tela onde o usuário gerencia suas personas (personagens)."""
    janela_pers = tk.Tk()
    janela_pers.title(f"CB Games - Painel de Personagens ({nome_usuario})")
    janela_pers.geometry("450x560")
    
    tk.Label(janela_pers, text="Criação e Personalização de Personagem", font=("Arial", 12, "bold")).pack(pady=10)
    
    # Campos de Personalização
    tk.Label(janela_pers, text="Nome do Personagem:").pack()
    entry_nome_p = tk.Entry(janela_pers, width=30)
    entry_nome_p.pack(pady=2)
    
    tk.Label(janela_pers, text="Especialidade (ex: Guerreiro, Mago):").pack()
    entry_esp = tk.Entry(janela_pers, width=30)
    entry_esp.pack(pady=2)
    
    tk.Label(janela_pers, text="Cor do Cabelo:").pack()
    entry_cabelo = tk.Entry(janela_pers, width=30)
    entry_cabelo.pack(pady=2)
    
    tk.Label(janela_pers, text="Cor da Persona (Pele/Traje):").pack()
    entry_cor = tk.Entry(janela_pers, width=30)
    entry_cor.pack(pady=2)
    
    def acao_salvar_persona():
        nome_p = entry_nome_p.get()
        especialidade = entry_esp.get()
        cabelo = entry_cabelo.get()
        cor = entry_cor.get()
        
        if not nome_p or not especialidade or not cabelo or not cor:
            messagebox.showerror("Erro", "Preencha todos os campos da persona!")
            return
            
        try:
            conexao = conectar_banco()
            cursor = conexao.cursor()
            cursor.execute("""
                INSERT INTO persona (usuario_id, nome, especialidade, cor_cabelo, cor_persona) 
                VALUES (?, ?, ?, ?, ?)
            """, (usuario_id, nome_p, especialidade, cabelo, cor))
            conexao.commit()
            conexao.close()
            
            messagebox.showinfo("Sucesso", "Personagem criado com segurança!")
            entry_nome_p.delete(0, tk.END)
            entry_esp.delete(0, tk.END)
            entry_cabelo.delete(0, tk.END)
            entry_cor.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar personagem: {e}")

    def acao_ver_personagens():
        conexao = conectar_banco()
        cursor = conexao.cursor()
        cursor.execute("SELECT id, nome, especialidade, cor_cabelo, cor_persona FROM persona WHERE usuario_id = ?", (usuario_id,))
        personas = cursor.fetchall()
        conexao.close()
        
        if not personas:
            messagebox.showinfo("Aviso", "Você ainda não tem personagens cadastrados.")
            return
            
        detalhes = ""
        for p in personas:
            detalhes += f"ID: {p[0]} | Nome: {p[1]} | Classe: {p[2]} | Cabelo: {p[3]} | Cor: {p[4]}\n"
            
        messagebox.showinfo("Seus Personagens", detalhes)

    # Nova função conectada ao botão de exclusão
    def acao_deletar():
        persona_id = entry_id_del.get()
        
        if not persona_id:
            messagebox.showerror("Erro", "Digite o ID do personagem que deseja excluir!")
            return
            
        try:
            conexao = conectar_banco()
            cursor = conexao.cursor()
            # Garante que o personagem existe e pertence ao usuário logado por segurança
            cursor.execute("SELECT id FROM persona WHERE id = ? AND usuario_id = ?", (persona_id, usuario_id))
            existe = cursor.fetchone()
            conexao.close()
            
            if not existe:
                messagebox.showwarning("Aviso", "Personagem não encontrado ou não pertence a você.")
                return
                
            # Chama a função de delete que está no seu database.py
            deletar_persona(persona_id)
            messagebox.showinfo("Sucesso", "Personagem excluído com sucesso!")
            entry_id_del.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao excluir: {e}")

    btn_salvar = tk.Button(janela_pers, text="Salvar Personagem", command=acao_salvar_persona, bg="green", fg="white", width=22)
    btn_salvar.pack(pady=8)
    
    btn_listar = tk.Button(janela_pers, text="Ver Meus Personagens", command=acao_ver_personagens, bg="blue", fg="white", width=22)
    btn_listar.pack(pady=5)
    
    # Elementos visuais para deletar
    tk.Label(janela_pers, text="ID do Personagem para Excluir:").pack(pady=(10, 0))
    entry_id_del = tk.Entry(janela_pers, width=15)
    entry_id_del.pack(pady=2)
    
    btn_deletar = tk.Button(janela_pers, text="Excluir Personagem", command=acao_deletar, bg="red", fg="white", width=22)
    btn_deletar.pack(pady=5)
    
    janela_pers.mainloop()


def abrir_tela_principal():
    # Garante que as tabelas existem assim que a tela abre
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
        cursor.execute("SELECT id, nome FROM usuarios WHERE nome = ? AND senha = ?", (usuario, senha_segura))
        resultado = cursor.fetchone()
        conexao.close()
        
        if resultado:
            usuario_id = resultado[0]
            nome_usuario = resultado[1]
            messagebox.showinfo("Sucesso", f"Login bem-sucedido! Bem-vindo, {nome_usuario}.")
            janela_login.destroy()
            abrir_tela_personalizacao(usuario_id, nome_usuario)
        else:
            messagebox.showerror("Acesso Negado", "Usuário não encontrado ou senha incorreta.")

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