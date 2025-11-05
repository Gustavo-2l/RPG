import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
from jogador import Jogador

def combate(jogador, inimigo, caminho_fundo="assets/Florestaprofunda.png"):
    # --- Janela do combate ---
    janela = tk.Toplevel()
    janela.title(f"⚔️ Batalha contra {inimigo.nome}")
    janela.attributes("-fullscreen", True)  # Tela cheia
    janela.configure(bg="black")

    # --- Canvas para colocar fundo ---
    canvas = tk.Canvas(janela, bg="black")
    canvas.pack(fill="both", expand=True)

    # Carrega imagem original do fundo
    try:
        imagem_original = Image.open(caminho_fundo)
    except Exception as e:
        print(f"Erro ao carregar imagem de fundo: {e}")
        imagem_original = None

    # --- Labels de status ---
    label_jogador = tk.Label(janela, text=f"{jogador.nome}: ❤️ {jogador.vida}/{jogador.vida_max}",
                             fg="white", bg="#000000", font=("Consolas", 12))
    label_inimigo = tk.Label(janela, text=f"{inimigo.nome}: ❤️ {inimigo.vida}/{inimigo.vida_max}",
                             fg="red", bg="#000000", font=("Consolas", 12))

    canvas.create_window(20, 20, anchor="nw", window=label_jogador)
    canvas.create_window(20, 60, anchor="nw", window=label_inimigo)

    # --- Log de combate ---
    log = tk.Text(janela, width=70, height=12, bg="#0d0d0d", fg="white", font=("Consolas", 10))
    canvas.create_window(20, 100, anchor="nw", window=log)

    # --- Frame para botões ---
    frame_botoes = tk.Frame(janela, bg="#000000")
    canvas.create_window(20, 500, anchor="nw", window=frame_botoes)

    # --- Funções ---
    def registrar(texto):
        log.insert(tk.END, texto + "\n")
        log.see(tk.END)

    def atualizar_status():
        label_jogador.config(text=f"{jogador.nome}: ❤️ {jogador.vida}/{jogador.vida_max}")
        label_inimigo.config(text=f"{inimigo.nome}: ❤️ {inimigo.vida}/{inimigo.vida_max}")

    def atacar():
        dano = jogador.atacar()
        inimigo.vida -= dano
        registrar(f"{jogador.nome} causou {dano} de dano!")
        atualizar_status()
        if inimigo.vida <= 0:
            registrar(f"{inimigo.nome} foi derrotado!")
            messagebox.showinfo("Vitória!", f"{jogador.nome} venceu a batalha!")
            janela.destroy()

    def defender():
        registrar(f"{jogador.nome} se defendeu!")
        # Aqui você pode implementar redução de dano ou outro efeito

    def usar_habilidade():
        if jogador.habilidade_desbloqueada:
            registrar(f"{jogador.nome} usou {jogador.habilidade_desbloqueada}!")
            # Implementar efeito da habilidade
        else:
            registrar(f"{jogador.nome} não possui habilidade desbloqueada.")

    # --- Botões ---
    botoes = [
        ("⚔️ Atacar", atacar),
        ("🛡️ Defender", defender),
        ("✨ Habilidade", usar_habilidade)
    ]
    for texto, cmd in botoes:
        tk.Button(frame_botoes, text=texto, command=cmd, bg="#333", fg="white", width=12, height=2).pack(side="left", padx=5)

    registrar(f"O combate começou contra {inimigo.nome}!")
    atualizar_status()

    # --- Redimensiona a imagem de fundo automaticamente ---
    def redimensionar_fundo(event):
        if imagem_original:
            nova_imagem = imagem_original.resize((event.width, event.height))
            fundo = ImageTk.PhotoImage(nova_imagem)
            canvas.background = fundo  # mantém referência
            canvas.create_image(0, 0, image=fundo, anchor="nw")
            canvas.tag_lower("all")  # garante que o fundo fique atrás de tudo

    canvas.bind("<Configure>", redimensionar_fundo)

    # --- Tecla ESC para sair do fullscreen ---
    janela.bind("<Escape>", lambda e: janela.destroy())
