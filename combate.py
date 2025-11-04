import random
import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk  # certifique-se de ter Pillow instalado: pip install pillow

def curar_pos_batalha(jogador):
    cura_vida = int(jogador.vida_max * 0.3)
    cura_mana = int(jogador.mana_max * 0.2)
    jogador.vida = min(jogador.vida + cura_vida, jogador.vida_max)
    jogador.mana = min(jogador.mana + cura_mana, jogador.mana_max)
    messagebox.showinfo("Recuperação", f"{jogador.nome} recuperou {cura_vida} de vida e {cura_mana} de mana!")


def combate(jogador, inimigo):
    janela = tk.Tk()
    janela.title("⚔️ Batalha RPG")
    janela.geometry("650x420")
    janela.config(bg="#1a1a1a")

    combate_ativo = True

    # --- IMAGEM DO PERSONAGEM ---
    try:
        img = Image.open("imagempersonagem.png")  # nome do arquivo que você enviou
        img = img.resize((120, 160))  # ajusta o tamanho da imagem
        img_tk = ImageTk.PhotoImage(img)
        label_imagem = tk.Label(janela, image=img_tk, bg="#1a1a1a")
        label_imagem.image = img_tk
        label_imagem.place(x=20, y=100)  # posiciona à esquerda
    except Exception as e:
        print("Erro ao carregar imagem do personagem:", e)

    # --- STATUS E INTERFACE ---
    label_status = tk.Label(
        janela,
        text=f"{jogador.nome} vs {inimigo.nome}",
        font=("Arial", 16, "bold"),
        fg="white",
        bg="#1a1a1a"
    )
    label_status.pack(pady=10)

    label_jogador = tk.Label(janela, fg="lime", bg="#1a1a1a", font=("Consolas", 12))
    label_jogador.pack()

    label_inimigo = tk.Label(janela, fg="red", bg="#1a1a1a", font=("Consolas", 12))
    label_inimigo.pack()

    log = tk.Text(janela, width=70, height=10, bg="#0d0d0d", fg="white", font=("Consolas", 10))
    log.pack(pady=10)

    # --- FUNÇÕES DE SUPORTE ---
    def atualizar_status():
        label_jogador.config(
            text=f"{jogador.nome}: ❤️ {jogador.vida}/{jogador.vida_max} | 🔵 {jogador.mana}/{jogador.mana_max}"
        )
        label_inimigo.config(
            text=f"{inimigo.nome}: ❤️ {inimigo.vida}/{inimigo.vida_max}"
        )

    def registrar(texto):
        log.insert(tk.END, texto + "\n")
        log.see(tk.END)

    # --- TURNO DO INIMIGO ---
    def turno_inimigo():
        nonlocal combate_ativo
        if not combate_ativo:
            return

        if inimigo.vida <= 0:
            combate_ativo = False
            registrar(f"\n🎉 {jogador.nome} venceu a batalha!")
            jogador.ganhar_xp(inimigo.xp_inimigo)
            jogador.ouro += inimigo.ouro_inimigo
            registrar(f"💰 Ganhou {inimigo.ouro_inimigo} de ouro!")
            curar_pos_batalha(jogador)
            messagebox.showinfo("Vitória!", "Você venceu a batalha!")
            janela.destroy()
            return

        acao = random.choice(["atacar", "defender", "ataque_forte"])
        if acao == "defender":
            registrar(f"{inimigo.nome} se defende e reduz o próximo dano.")
            inimigo.defendendo = True
        else:
            dano = inimigo.atacar()
            if acao == "ataque_forte":
                dano *= 1.2
                if random.random() < 0.25:
                    dano *= 1.5
                    registrar(f"💥 {inimigo.nome} acerta um golpe CRÍTICO!")
            if getattr(inimigo, "defendendo", False):
                dano *= 0.7
                inimigo.defendendo = False
            jogador.defender(dano)
            registrar(f"{inimigo.nome} causa {int(dano)} de dano!")

        if jogador.vida <= 0:
            combate_ativo = False
            registrar(f"\n💀 {jogador.nome} foi derrotado!")
            messagebox.showerror("Derrota", "Fim de jogo!")
            janela.destroy()
            return

        atualizar_status()

    # --- AÇÕES DO JOGADOR ---
    def atacar():
        if not combate_ativo:
            return
        dano = jogador.atacar()
        inimigo.vida -= dano
        registrar(f"{jogador.nome} ataca causando {dano} de dano!")
        atualizar_status()
        janela.after(1000, turno_inimigo)

    def defender():
        if not combate_ativo:
            return
        jogador.defender_acao()
        registrar(f"{jogador.nome} assume posição defensiva!")
        atualizar_status()
        janela.after(1000, turno_inimigo)

    def esquivar():
        if not combate_ativo:
            return
        if jogador.esquivar():
            registrar(f"💨 {jogador.nome} esquiva com sucesso!")
        else:
            registrar("⚠️ Esquiva falhou!")
            jogador.defender(inimigo.atacar())
        atualizar_status()
        janela.after(1000, turno_inimigo)

    def usar_item():
        if not combate_ativo:
            return
        items = "\n".join([f"{i}: {q}" for i, q in jogador.inventario.items()])
        item = simpledialog.askstring("Inventário", f"Escolha um item:\n{items}")
        if item:
            jogador.usar_item(item.lower())
            registrar(f"{jogador.nome} usou {item}!")
            atualizar_status()
            janela.after(1000, turno_inimigo)

    def habilidade():
        if not combate_ativo:
            return
        if jogador.usar_habilidade(inimigo):
            registrar(f"{jogador.nome} usa uma habilidade lendária!")
        else:
            registrar("⚠️ Mana insuficiente ou habilidade em recarga!")
        atualizar_status()
        janela.after(1000, turno_inimigo)

    # --- BOTÕES ---
    frame_botoes = tk.Frame(janela, bg="#1a1a1a")
    frame_botoes.pack(pady=10)

    botoes = [
        ("⚔️ Atacar", atacar),
        ("🛡️ Defender", defender),
        ("💨 Esquivar", esquivar),
        ("🧪 Usar Item", usar_item),
        ("🌟 Habilidade", habilidade),
    ]
    for texto, cmd in botoes:
        tk.Button(
            frame_botoes,
            text=texto,
            command=cmd,
            width=12,
            height=2,
            bg="#333",
            fg="white",
            font=("Arial", 10, "bold")
        ).pack(side=tk.LEFT, padx=5)

    atualizar_status()
    registrar("⚔️ Combate Iniciado!")

    janela.mainloop()
