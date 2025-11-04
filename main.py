import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # para exibir imagens no Tkinter
from jogador import Jogador
from inimigo import Inimigo
from combate import combate
from historia import historia
from fases import carregar_fases
import os


# --- Função principal com Tkinter ---
def iniciar_jogo():
    nome = entrada_nome.get().strip()
    classe = classe_var.get()

    if not nome:
        messagebox.showwarning("Aviso", "Digite o nome do seu personagem!")
        return

    if classe not in ["Homem", "Mulher"]:
        messagebox.showwarning("Aviso", "Escolha uma classe válida!")
        return

    root.destroy()  # Fecha a janela inicial e começa o jogo

    # --- Parte lógica do jogo ---
    historia()
    jogador = Jogador(nome, classe)
    jogador.habilidades = []  # garante a lista

    fases = carregar_fases()

    for fase in fases:
        venceu = fase.iniciar(jogador, combate)
        if not venceu:
            messagebox.showerror("💀 Fim de jogo", f"{jogador.nome} foi derrotado!")
            return

    messagebox.showinfo(
        "🏁 Fim do Jogo",
        f"Parabéns {jogador.nome}!\nVocê completou todas as fases!\n\n"
        f"Habilidades desbloqueadas: {', '.join(jogador.habilidades)}",
    )


# --- Função para mostrar o personagem escolhido ---
def atualizar_personagem(*args):
    classe = classe_var.get()

    if classe == "Homem":
        caminho_imagem = "assets/imagempersonagem.png"  # imagem masculina
    else:
        caminho_imagem = "assets/imagemmulher.png"  # imagem feminina

    if not os.path.exists(caminho_imagem):
        print(f"⚠️ Imagem não encontrada: {caminho_imagem}")
        return

    imagem = Image.open(caminho_imagem)
    imagem = imagem.resize((120, 120))
    imagem_tk = ImageTk.PhotoImage(imagem)

    label_personagem.config(image=imagem_tk)
    label_personagem.image = imagem_tk  # mantém referência


# --- Interface visual inicial ---
root = tk.Tk()
root.title("RPG de Texto Visual")
root.geometry("420x420")
root.configure(bg="#1e1e2f")

titulo = tk.Label(
    root,
    text="⚔️ RPG de Texto Visual ⚔️",
    font=("Arial", 18, "bold"),
    bg="#1e1e2f",
    fg="#FFD700"
)
titulo.pack(pady=20)

# Entrada do nome
tk.Label(root, text="Digite seu nome:", font=("Arial", 12), bg="#1e1e2f", fg="white").pack()
entrada_nome = tk.Entry(root, font=("Arial", 12))
entrada_nome.pack(pady=5)

# Escolha da classe
tk.Label(root, text="Escolha sua classe:", font=("Arial", 12), bg="#1e1e2f", fg="white").pack(pady=(10, 0))
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

# Botão iniciar
botao_iniciar = tk.Button(
    root,
    text="🎮 Iniciar Jogo",
    font=("Arial", 14, "bold"),
    bg="#4CAF50",
    fg="white",
    command=iniciar_jogo
)
botao_iniciar.pack(pady=20)

root.mainloop()
