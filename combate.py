import tkinter as tk
from PIL import Image, ImageTk
import numpy as np  # <-- import numpy
from models.jogador import Jogador

def combate(jogador, inimigo, caminho_fundo="assets/Florestaprofunda.png", on_fim=None):
    # --- Janela do combate ---
    janela = tk.Toplevel()
    janela.title(f"⚔️ Batalha contra {inimigo.nome}")
    janela.geometry("800x600")
    janela.configure(bg="black")

    # --- Canvas ---
    canvas = tk.Canvas(janela, width=800, height=600, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    # --- Fundo ---
    try:
        imagem_original = Image.open(caminho_fundo)
        fundo = ImageTk.PhotoImage(imagem_original)
        canvas.background = fundo
        canvas.create_image(0, 0, image=fundo, anchor="nw")
    except Exception as e:
        print(f"Erro ao carregar fundo: {e}")
        imagem_original = None

    # --- Labels de status ---
    label_jogador = tk.Label(janela, text=f"{jogador.nome}: ❤️ {jogador.vida}/{jogador.vida_max}",
                             fg="white", bg="#000000", font=("Consolas", 12))
    label_inimigo = tk.Label(janela, text=f"{inimigo.nome}: ❤️ {inimigo.vida}/{inimigo.vida_max}",
                             fg="red", bg="#000000", font=("Consolas", 12))

    canvas.create_window(20, 20, anchor="nw", window=label_jogador)
    canvas.create_window(20, 60, anchor="nw", window=label_inimigo)

    # --- Log ---
    log = tk.Text(janela, width=80, height=15, bg="#0d0d0d", fg="white",
                  font=("Consolas", 10), relief="flat")
    canvas.create_window(20, 100, anchor="nw", window=log)

    # --- Frame de botões ---
    frame_botoes = tk.Frame(janela, bg="#000000")
    canvas.create_window(20, 500, anchor="nw", window=frame_botoes)

    # --- Variáveis de controle ---
    jogador.defendendo = False
    jogador.esquivando = False
    if not hasattr(jogador, "itens"):
        jogador.itens = {"poção": 2}

    # --- Funções auxiliares ---
    def registrar(texto):
        log.insert(tk.END, texto + "\n")
        log.see(tk.END)

    def atualizar_status():
        label_jogador.config(text=f"{jogador.nome}: ❤️ {jogador.vida}/{jogador.vida_max}")
        label_inimigo.config(text=f"{inimigo.nome}: ❤️ {inimigo.vida}/{inimigo.vida_max}")

    def verificar_fim():
        if inimigo.vida <= 0:
            registrar(f"{inimigo.nome} foi derrotado! 🏆")
            registrar(f"{jogador.nome} venceu a batalha!")
            if on_fim:
                janela.after(1500, lambda: [janela.destroy(), on_fim("vitoria")])
            else:
                janela.after(1500, janela.destroy)
            return True
        elif jogador.vida <= 0:
            registrar(f"{jogador.nome} foi derrotado... 💀")
            if on_fim:
                janela.after(1500, lambda: [janela.destroy(), on_fim("derrota")])
            else:
                janela.after(1500, janela.destroy)
            return True
        return False

    def fim_turno():
        for b in botoes_widgets:
            b.config(state="disabled")
        janela.after(1000, turno_inimigo)

    def turno_inimigo():
        if verificar_fim():
            return

        # --- Esquiva ---
        if jogador.esquivando:
            chance = np.random.rand()  # <-- usando numpy
            if chance <= 0.5:
                registrar(f"{jogador.nome} esquivou com sucesso! 🌀 Nenhum dano recebido.")
                jogador.esquivando = False
                registrar(f"É a vez de {jogador.nome}!")
                for b in botoes_widgets:
                    b.config(state="normal")
                return
            else:
                registrar(f"{jogador.nome} tentou esquivar, mas falhou! 😣")
            jogador.esquivando = False

        # --- Ataque inimigo ---
        dano = inimigo.atacar()

        if jogador.defendendo:
            dano = int(dano * 0.5)
            jogador.defendendo = False
            registrar(f"{jogador.nome} defendeu e reduziu o dano pela metade!")

        jogador.vida -= dano
        if jogador.vida < 0:
            jogador.vida = 0

        registrar(f"{inimigo.nome} atacou e causou {dano} de dano!")
        atualizar_status()

        if verificar_fim():
            return

        registrar(f"É a vez de {jogador.nome}!")
        for b in botoes_widgets:
            b.config(state="normal")

    # --- Ações do jogador ---
    def atacar():
        dano = jogador.atacar()
        inimigo.vida -= dano
        if inimigo.vida < 0:
            inimigo.vida = 0
        registrar(f"{jogador.nome} atacou e causou {dano} de dano!")
        atualizar_status()
        if not verificar_fim():
            fim_turno()

    def defender():
        registrar(f"{jogador.nome} se defendeu! 🛡️ (menos dano no próximo ataque)")
        jogador.defendendo = True
        fim_turno()

    def esquivar():
        registrar(f"{jogador.nome} se prepara para esquivar! 🌀 (50% de chance de evitar dano)")
        jogador.esquivando = True
        fim_turno()

    def usar_item():
        if jogador.itens.get("poção", 0) > 0:
            jogador.itens["poção"] -= 1
            cura = np.random.randint(20, 36)  # <-- usando numpy
            jogador.vida += cura
            if jogador.vida > jogador.vida_max:
                jogador.vida = jogador.vida_max
            registrar(f"{jogador.nome} usou uma poção e recuperou {cura} de vida! 💊 ({jogador.itens['poção']} restantes)")
            atualizar_status()
        else:
            registrar("⚠️ Você não tem mais poções!")
        fim_turno()

    def usar_habilidade():
        if getattr(jogador, "habilidade_desbloqueada", None):
            registrar(f"{jogador.nome} usou {jogador.habilidade_desbloqueada}! ✨")
            dano = np.random.randint(15, 26)  # <-- usando numpy
            inimigo.vida -= dano
            if inimigo.vida < 0:
                inimigo.vida = 0
            registrar(f"A habilidade causou {dano} de dano extra!")
            atualizar_status()
        else:
            registrar(f"{jogador.nome} não possui habilidade desbloqueada.")
        fim_turno()

    # --- Botões ---
    botoes = [
        ("⚔️ Atacar", atacar),
        ("🛡️ Defender", defender),
        ("🌀 Esquivar", esquivar),
        ("💊 Usar Item", usar_item),
        ("✨ Habilidade", usar_habilidade)
    ]
    botoes_widgets = []
    for texto, cmd in botoes:
        b = tk.Button(frame_botoes, text=texto, command=cmd,
                      bg="#333", fg="white", width=12, height=2)
        b.pack(side="left", padx=5)
        botoes_widgets.append(b)

    # --- Log inicial ---
    registrar(f"O combate começou contra {inimigo.nome}! ⚔️")
    registrar(f"É a vez de {jogador.nome}!")
    atualizar_status()

    # --- Redimensionar fundo dinamicamente ---
    def redimensionar_fundo(event):
        if imagem_original:
            nova_img = imagem_original.resize((event.width, event.height))
            fundo_redimensionado = ImageTk.PhotoImage(nova_img)
            canvas.background = fundo_redimensionado
            canvas.create_image(0, 0, image=fundo_redimensionado, anchor="nw")
            canvas.tag_lower("all")

    canvas.bind("<Configure>", redimensionar_fundo)

    # --- ESC para sair ---
    janela.bind("<Escape>", lambda e: janela.destroy())

    janela.mainloop()
