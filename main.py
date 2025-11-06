import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from jogador import Jogador
from inimigo import Inimigo
from combate import combate
from historia import historia
from fases import carregar_fases
import os


# --- Função para gerenciar as fases ---
def iniciar_fase(jogador, fases, indice_fase=0):
    if indice_fase >= len(fases):
        messagebox.showinfo("🏁 Fim do Jogo", f"Parabéns {jogador.nome}! Você completou todas as fases!")
        root.destroy()
        return

    fase = fases[indice_fase]
    inimigos = fase.inimigos + ([fase.boss] if fase.boss else [])
    indice_inimigo = 0

    def iniciar_proximo_inimigo():
        nonlocal indice_inimigo
        if indice_inimigo >= len(inimigos):
            # Fase concluída
            for lenda in fase.lendas:
                if lenda not in jogador.habilidades:
                    jogador.habilidades.append(lenda)
            print(f"✅ Fase {fase.nome} concluída!")
            iniciar_fase(jogador, fases, indice_fase + 1)
            return

        inimigo_atual = inimigos[indice_inimigo]

        def ao_terminar(resultado=None):
            nonlocal indice_inimigo

            # --- Se o jogador perdeu ---
            if resultado == "derrota" or jogador.vida <= 0:
                messagebox.showinfo("💀 Derrota", f"{jogador.nome} foi derrotado!")
                root.destroy()
                return

            # --- Se venceu ---
            indice_inimigo += 1
            iniciar_proximo_inimigo()

        # Inicia o combate com o inimigo atual
        combate(jogador, inimigo_atual, fase.caminho_fundo, on_fim=ao_terminar)

    iniciar_proximo_inimigo()


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

    # Fecha a tela inicial
    root.withdraw()

    # História inicial
    historia(jogador.nome)

    # Carrega as fases
    fases = carregar_fases()
    if not fases:
        messagebox.showerror("Erro", "Nenhuma fase foi carregada!")
        root.deiconify()
        return

    # Começa a primeira fase
    iniciar_fase(jogador, fases)


# --- Atualiza imagem do personagem ---
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
    label_personagem.image = imagem_tk  # evita descarte da imagem


# --- Interface inicial ---
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
classe_var.trace("w", atualizar_personagem)

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

# --- Inicia ---
root.mainloop()
