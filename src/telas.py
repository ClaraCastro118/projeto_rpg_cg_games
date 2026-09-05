import tkinter as tk
from tkinter import messagebox
from database import inicializar_banco, conectar_banco, criptografar_senha, deletar_persona

def abrir_tela_jogo(usuario_id):
    """Abre o mundo do jogo e renderiza TODOS os personagens do usuário lado a lado."""
    conexao = conectar_banco()
    cursor = conexao.cursor()
    # Pega todos os personagens pertencentes ao usuário logado
    cursor.execute("SELECT nome, cor_cabelo, cor_persona FROM persona WHERE usuario_id = ?", (usuario_id,))
    personagens = cursor.fetchall()
    conexao.close()

    if not personagens:
        messagebox.showwarning("Aviso", "Você precisa criar e salvar um personagem antes de entrar no jogo!")
        return

    janela_jogo = tk.Toplevel()
    janela_jogo.title("Meu Grupo de Personagens")
    # Aumentei a largura da janela para caber mais personagens
    janela_jogo.geometry("800x450")
    
    canvas = tk.Canvas(janela_jogo, width=800, height=400, bg="#87CEEB")
    canvas.pack()

    # Desenhando o chão verde
    canvas.create_rectangle(0, 350, 800, 400, fill="forestgreen", outline="")

    # Lista para guardar as partes do corpo que vamos animar depois
    elementos_animacao = []

    # Laço de repetição: desenha cada personagem com um espaço de 120 pixels entre eles
    for indice, p in enumerate(personagens):
        nome, cor_cabelo, cor_persona = p
        
        # Calcula a posição X na tela para eles não ficarem um em cima do outro
        posicao_x = 100 + (indice * 120)

        # --- Validação de cores segura ---
        try:
            janela_jogo.winfo_rgb(cor_persona)
            cor_roupa = cor_persona
        except tk.TclError:
            cor_roupa = "gray" # Cor padrão caso a cor da persona seja inválida

        try:
            janela_jogo.winfo_rgb(cor_cabelo)
            cor_cab = cor_cabelo
        except tk.TclError:
            cor_cab = "black" # Cor padrão caso a cor do cabelo seja inválida
        # ---------------------------------

        # 1. PERNAS E SAPATOS (Ficam de fora da animação para manter o pé no chão)
        canvas.create_rectangle(posicao_x - 15, 310, posicao_x - 5, 350, fill="#2F4F4F", outline="black") # Perna esq
        canvas.create_rectangle(posicao_x + 5, 310, posicao_x + 15, 350, fill="#2F4F4F", outline="black") # Perna dir
        canvas.create_rectangle(posicao_x - 20, 340, posicao_x - 3, 350, fill="black") # Sapato esq
        canvas.create_rectangle(posicao_x + 3, 340, posicao_x + 20, 350, fill="black") # Sapato dir

        # 2. PARTES DO CORPO (Animadas juntas - Tronco e braços)
        tronco = canvas.create_rectangle(posicao_x - 20, 250, posicao_x + 20, 310, fill=cor_roupa, outline="black")
        braco_esq = canvas.create_rectangle(posicao_x - 35, 250, posicao_x - 20, 295, fill=cor_roupa, outline="black")
        braco_dir = canvas.create_rectangle(posicao_x + 20, 250, posicao_x + 35, 295, fill=cor_roupa, outline="black")
        mao_esq = canvas.create_oval(posicao_x - 33, 290, posicao_x - 22, 305, fill="#FDDBB7", outline="black")
        mao_dir = canvas.create_oval(posicao_x + 22, 290, posicao_x + 33, 305, fill="#FDDBB7", outline="black")

        # 3. PARTES DA CABEÇA (Animadas juntas - sobem um pouco mais que o corpo)
        rosto = canvas.create_oval(posicao_x - 25, 200, posicao_x + 25, 255, fill="#FDDBB7", outline="black")
        
        # --- CABELO REFATORADO: Estilo "Desenhado / Espetado" ---
        pontos_cabelo = [
            posicao_x - 26, 235,  # Base esquerda
            posicao_x - 35, 205,  # Mecha 1
            posicao_x - 18, 195,  # Vale 1
            posicao_x - 15, 175,  # Mecha 2
            posicao_x - 5, 190,   # Vale 2
            posicao_x + 8, 170,   # Mecha 3
            posicao_x + 15, 185,  # Vale 3
            posicao_x + 28, 175,  # Mecha 4
            posicao_x + 22, 198,  # Vale 4
            posicao_x + 35, 215,  # Mecha 5
            posicao_x + 26, 235,  # Base direita
            posicao_x + 15, 210,  # Curva da franja (direita)
            posicao_x + 5, 225,   # Mecha da franja no meio da testa
            posicao_x - 10, 210,  # Curva da franja (esquerda)
        ]
        cabelo = canvas.create_polygon(pontos_cabelo, fill=cor_cab, outline="black", width=1)
        # --------------------------------------------------------

        olho_esq = canvas.create_oval(posicao_x - 12, 222, posicao_x - 7, 227, fill="black")
        olho_dir = canvas.create_oval(posicao_x + 7, 222, posicao_x + 12, 227, fill="black")
        boca = canvas.create_arc(posicao_x - 10, 230, posicao_x + 10, 245, start=190, extent=160, style=tk.ARC, width=2)
        
        # Nome ajustado mais para cima (Y de 175 para 155) para não cobrir as mechas
        texto_nome = canvas.create_text(posicao_x, 155, text=nome, font=("Arial", 10, "bold"))

        # Agrupa os elementos em listas para a animação
        lista_cabeca = [rosto, cabelo, olho_esq, olho_dir, boca, texto_nome]
        lista_corpo = [tronco, braco_esq, braco_dir, mao_esq, mao_dir]
        
        elementos_animacao.append((lista_cabeca, lista_corpo))

    def animar_respiracao(crescendo=True):
        # Determina a direção do movimento (Cabeça sobe 2px, corpo sobe 1px)
        dy_cabeca = -2 if crescendo else 2
        dy_corpo = -1 if crescendo else 1

        for partes_cabeca, partes_corpo in elementos_animacao:
            # Move todas as partes da cabeça
            for item in partes_cabeca:
                canvas.move(item, 0, dy_cabeca)
            # Move todas as partes do corpo
            for item in partes_corpo:
                canvas.move(item, 0, dy_corpo)
                
        # Alterna o estado (True para False, False para True) repetindo a cada 600ms
        janela_jogo.after(600, animar_respiracao, not crescendo)

    animar_respiracao()


def abrir_tela_personalizacao(usuario_id, nome_usuario):
    janela_pers = tk.Tk()
    janela_pers.title(f"CB Games - Painel de Personagens ({nome_usuario})")
    janela_pers.geometry("450x560")
    
    tk.Label(janela_pers, text="Criação e Personalização de Personagem", font=("Arial", 12, "bold")).pack(pady=10)
    
    tk.Label(janela_pers, text="Nome do Personagem:").pack()
    entry_nome_p = tk.Entry(janela_pers, width=30)
    entry_nome_p.pack(pady=2)
    
    tk.Label(janela_pers, text="Especialidade (ex: Guerreiro, Mago):").pack()
    entry_esp = tk.Entry(janela_pers, width=30)
    entry_esp.pack(pady=2)
    
    tk.Label(janela_pers, text="Cor do Cabelo (ex: black, yellow, red):").pack()
    entry_cabelo = tk.Entry(janela_pers, width=30)
    entry_cabelo.pack(pady=2)
    
    tk.Label(janela_pers, text="Cor da Persona (Pele/Traje) (ex: blue, green):").pack()
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

    def acao_deletar():
        persona_id = entry_id_del.get()
        
        if not persona_id:
            messagebox.showerror("Erro", "Digite o ID do personagem que deseja excluir!")
            return
            
        try:
            conexao = conectar_banco()
            cursor = conexao.cursor()
            cursor.execute("SELECT id FROM persona WHERE id = ? AND usuario_id = ?", (persona_id, usuario_id))
            existe = cursor.fetchone()
            conexao.close()
            
            if not existe:
                messagebox.showwarning("Aviso", "Personagem não encontrado ou não pertence a você.")
                return
                
            deletar_persona(persona_id)
            messagebox.showinfo("Sucesso", "Personagem excluído com sucesso!")
            entry_id_del.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao excluir: {e}")

    btn_salvar = tk.Button(janela_pers, text="Salvar Personagem", command=acao_salvar_persona, bg="green", fg="white", width=22)
    btn_salvar.pack(pady=8)
    
    btn_listar = tk.Button(janela_pers, text="Ver Meus Personagens", command=acao_ver_personagens, bg="blue", fg="white", width=22)
    btn_listar.pack(pady=5)
    
    # Botão de jogar chama diretamente a tela, sem pedir ID
    btn_jogar = tk.Button(janela_pers, text="🎮 Ver Todos no Jogo", command=lambda: abrir_tela_jogo(usuario_id), bg="purple", fg="white", width=22, font=("Arial", 10, "bold"))
    btn_jogar.pack(pady=10)
    
    tk.Label(janela_pers, text="ID do Personagem para Excluir:").pack(pady=(10, 0))
    entry_id_del = tk.Entry(janela_pers, width=15)
    entry_id_del.pack(pady=2)
    
    btn_deletar = tk.Button(janela_pers, text="Excluir Personagem", command=acao_deletar, bg="red", fg="white", width=22)
    btn_deletar.pack(pady=5)
    
    janela_pers.mainloop()


def abrir_tela_principal():
    inicializar_banco()
    
    janela_login = tk.Tk()
    janela_login.title("CB Games - Login e Cadastro")
    janela_login.geometry("400x350")
    
    titulo = tk.Label(janela_login, text="CB Games - RPG", font=("Arial", 16, "bold"))
    titulo.pack(pady=20)
    
    tk.Label(janela_login, text="Nome de Usuário:").pack()
    entry_usuario = tk.Entry(janela_login, width=30)
    entry_usuario.pack(pady=5)
    
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