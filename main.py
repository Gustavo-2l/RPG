import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # para exibir imagens no Tkinter
from jogador import Jogador
from inimigo import Inimigo
from combate import combate
from historia import historia
from fases import carregar_fases
import os
 
 
# --- Função principal do jogo ---
def iniciar_jogo():
    nome = entrada_nome.get().strip()
    classe = classe_var.get()
 
    if not nome:
        messagebox.showwarning("Aviso", "Digite o nome do seu personagem!")
        return
    if not classe:
        messagebox.showwarning("Aviso", "Escolha o gênero do seu personagem!")
        return
 
    jogador = Jogador(nome, classe)
 
    # Fecha a tela inicial antes de iniciar a história
    root.withdraw()
 
    # Mostra a introdução e espera o jogador fechar
    historia(jogador.nome)
 
    # Carrega todas as fases
    fases = carregar_fases()
    if not fases:
        messagebox.showerror("Erro", "Nenhuma fase foi carregada!")
        root.deiconify()
        return
 
    # Percorre todas as fases
    for i, fase in enumerate(fases, start=1):
        fase.iniciar(jogador, combate)
 
        # Se o jogador morrer, interrompe o jogo
        if jogador.vida <= 0:
            messagebox.showinfo("💀 Game Over", f"{jogador.nome} foi derrotado!")
            root.destroy()
            return
 
        # Mensagem intermediária entre as fases
        if i < len(fases):
            messagebox.showinfo(
                "⚔️ Fase Concluída!",
                f"Você completou a fase {i}!\nPrepare-se para a próxima...",
            )
 
    # Ao final de todas as fases
    messagebox.showinfo(
        "🏁 Fim do Jogo",
        f"Parabéns {jogador.nome}!\nVocê completou todas as fases!\n\n"
        f"Habilidades desbloqueadas: {', '.join(jogador.habilidades)}",
    )
 
    # Fecha o jogo ao final
    root.destroy()
 
 
# --- Atualiza imagem do personagem escolhido ---
def atualizar_personagem(*args):
    classe = classe_var.get()
    if not classe:
        return
 
    if classe == "Homem":
        caminho_imagem = os.path.join("assets", "imagempersonagem.png")
    else:
        caminho_imagem = os.path.join("assets", "imagemmulher.png")
 
    if not os.path.exists(caminho_imagem):
        print(f"⚠️ Imagem não encontrada: {caminho_imagem}")
        return
 
    imagem = Image.open(caminho_imagem)
    imagem = imagem.resize((120, 120))
    imagem_tk = ImageTk.PhotoImage(imagem)
 
    label_personagem.config(image=imagem_tk)
    label_personagem.image = imagem_tk  # mantém referência para evitar descarte
 
 
# --- Interface visual inicial ---
root = tk.Tk()
root.title("🌌 LEGENDARUM 🌌")
root.geometry("420x480")
root.configure(bg="#1e1e2f")
 
titulo = tk.Label(
    root,
    text="⚔️ LEGENDARUM ⚔️",
    font=("Georgia", 18, "bold"),
    bg="#1e1e2f",
    fg="#FFD700"
)
titulo.pack(pady=20)
 
# Entrada do nome
tk.Label(
    root, text="Digite seu nome:", font=("Arial", 12),
    bg="#1e1e2f", fg="white"
).pack()
entrada_nome = tk.Entry(root, font=("Arial", 12))
entrada_nome.pack(pady=5)
 
# Escolha da classe
tk.Label(
    root, text="Escolha sua classe:", font=("Arial", 12),
    bg="#1e1e2f", fg="white"
).pack(pady=(10, 0))
 
classe_var = tk.StringVar(value="")
classe_var.trace("w", atualizar_personagem)  # detecta mudança de classe
 
frame_classes = tk.Frame(root, bg="#1e1e2f")
frame_classes.pack(pady=5)
 
tk.Radiobutton(
    frame_classes, text="Homem", variable=classe_var, value="Homem",
    bg="#1e1e2f", fg="white", selectcolor="#333"
).pack(side="left", padx=10)
 
tk.Radiobutton(
    frame_classes, text="Mulher", variable=classe_var, value="Mulher",
    bg="#1e1e2f", fg="white", selectcolor="#333"
).pack(side="left", padx=10)
 
# --- Imagem do personagem ---
label_personagem = tk.Label(root, bg="#1e1e2f")
label_personagem.pack(pady=15)
 
# --- Botão iniciar ---
botao_iniciar = tk.Button(
    root,
    text=" Iniciar Jogo",
    font=("Arial", 14, "bold"),
    bg="#4CAF50",
    fg="white",
    command=iniciar_jogo
)
botao_iniciar.pack(pady=20)
 
# --- Inicia a janela principal ---
root.mainloop()
 