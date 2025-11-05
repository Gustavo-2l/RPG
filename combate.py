import tkinter as tk
from PIL import Image, ImageTk
import random

class JogoRPG:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🔥 RPG Lendário 🔥")
        self.root.geometry("700x500")
        self.root.config(bg="#1a1a1a")

        # Cria um frame principal — onde tudo será trocado
        self.frame_principal = tk.Frame(self.root, bg="#1a1a1a")
        self.frame_principal.pack(fill="both", expand=True)

        # Exemplo de jogador/inimigo (pode ser substituído pelo seu sistema)
        self.jogador = type("J", (), {"nome":"Herói", "vida":100, "vida_max":100, "mana":50, "mana_max":50,
                                      "atacar":lambda self: random.randint(10,20),
                                      "defender_acao":lambda self: None,
                                      "esquivar":lambda self: random.random()<0.3,
                                      "defender":lambda self,dano: setattr(self,"vida",max(0,self.vida-int(dano))),
                                      "usar_item":lambda self,i: None,
                                      "usar_habilidade":lambda self,ini: True,
                                      "inventario":{"poção":2}})()
        self.inimigo = type("I", (), {"nome":"Goblin", "vida":80, "vida_max":80, "forca":10,
                                      "atacar":lambda self: random.randint(5,15)})()

        # Começa na tela inicial
        self.mostrar_menu_inicial()

        self.root.mainloop()

    # --- Troca de telas ---
    def limpar_tela(self):
        for widget in self.frame_principal.winfo_children():
            widget.destroy()

    # --- Tela inicial ---
    def mostrar_menu_inicial(self):
        self.limpar_tela()
        tk.Label(self.frame_principal, text="🏰 Bem-vindo ao RPG Lendário",
                 font=("Arial", 18, "bold"), fg="white", bg="#1a1a1a").pack(pady=40)

        tk.Button(self.frame_principal, text="Iniciar Jogo", command=self.iniciar_fase,
                  bg="#333", fg="white", width=20, height=2).pack()

    # --- Tela da fase (pode exibir história, NPCs etc.) ---
    def iniciar_fase(self):
        self.limpar_tela()
        tk.Label(self.frame_principal, text="🌲 Fase 1: Floresta Sombria",
                 font=("Arial", 16, "bold"), fg="white", bg="#1a1a1a").pack(pady=20)
        tk.Button(self.frame_principal, text="Entrar em combate ⚔️",
                  command=self.iniciar_combate, bg="#444", fg="white", width=20, height=2).pack(pady=20)

    # --- Tela de combate ---
    def iniciar_combate(self):
        self.limpar_tela()

        self.log = tk.Text(self.frame_principal, width=80, height=10, bg="#0d0d0d", fg="white", font=("Consolas", 10))
        self.log.pack(pady=10)

        self.label_status = tk.Label(self.frame_principal, fg="lime", bg="#1a1a1a", font=("Consolas", 12))
        self.label_status.pack()

        self.label_inimigo = tk.Label(self.frame_principal, fg="red", bg="#1a1a1a", font=("Consolas", 12))
        self.label_inimigo.pack()

        self.frame_botoes = tk.Frame(self.frame_principal, bg="#1a1a1a")
        self.frame_botoes.pack(pady=10)

        botoes = [
            ("⚔️ Atacar", self.atacar),
            ("🛡️ Defender", self.defender),
            ("💨 Esquivar", self.esquivar),
            ("🧪 Usar Item", self.usar_item),
            ("🌟 Habilidade", self.habilidade),
        ]
        for texto, cmd in botoes:
            tk.Button(self.frame_botoes, text=texto, command=cmd,
                      width=12, height=2, bg="#333", fg="white",
                      font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)

        self.atualizar_status()
        self.registrar("💥 Combate iniciado!")

    def atualizar_status(self):
        self.label_status.config(
            text=f"{self.jogador.nome}: ❤️ {self.jogador.vida}/{self.jogador.vida_max} | 🔵 {self.jogador.mana}/{self.jogador.mana_max}"
        )
        self.label_inimigo.config(
            text=f"{self.inimigo.nome}: ❤️ {self.inimigo.vida}/{self.inimigo.vida_max}"
        )

    def registrar(self, texto):
        self.log.insert(tk.END, texto + "\n")
        self.log.see(tk.END)

    # --- Ações do jogador ---
    def atacar(self):
        dano = self.jogador.atacar()
        self.inimigo.vida -= dano
        self.registrar(f"{self.jogador.nome} ataca causando {dano} de dano!")
        if self.inimigo.vida <= 0:
            self.vitoria()
        else:
            self.root.after(1000, self.turno_inimigo)
        self.atualizar_status()

    def defender(self):
        self.jogador.defender_acao()
        self.registrar(f"{self.jogador.nome} se defende!")
        self.root.after(1000, self.turno_inimigo)

    def esquivar(self):
        if self.jogador.esquivar():
            self.registrar(f"{self.jogador.nome} esquivou com sucesso!")
        else:
            dano = self.inimigo.atacar()
            self.jogador.defender(dano)
            self.registrar(f"{self.jogador.nome} falhou e recebeu {dano} de dano!")
        self.root.after(1000, self.turno_inimigo)
        self.atualizar_status()

    def usar_item(self):
        self.registrar(f"{self.jogador.nome} usou uma poção! ❤️ +20")
        self.jogador.vida = min(self.jogador.vida + 20, self.jogador.vida_max)
        self.root.after(1000, self.turno_inimigo)
        self.atualizar_status()

    def habilidade(self):
        if self.jogador.usar_habilidade(self.inimigo):
            self.registrar("✨ Ataque especial usado!")
            self.inimigo.vida -= 30
        self.root.after(1000, self.turno_inimigo)
        self.atualizar_status()

    def turno_inimigo(self):
        if self.inimigo.vida <= 0:
            self.vitoria()
            return
        dano = self.inimigo.atacar()
        self.jogador.defender(dano)
        self.registrar(f"{self.inimigo.nome} causa {dano} de dano!")
        if self.jogador.vida <= 0:
            self.derrota()
        self.atualizar_status()

    # --- Fim de combate ---
    def vitoria(self):
        self.registrar("🏆 Vitória!")
        tk.Button(self.frame_principal, text="Continuar ▶️", command=self.iniciar_fase,
                  bg="#2e8b57", fg="white").pack(pady=20)

    def derrota(self):
        self.registrar("☠️ Você foi derrotado...")
        tk.Button(self.frame_principal, text="Tentar novamente", command=self.iniciar_combate,
                  bg="#8b0000", fg="white").pack(pady=20)

# --- Inicia o jogo ---
JogoRPG()
