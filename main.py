import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import json, os
from jogador import Jogador
from inimigo import Inimigo
from combate import combate
from historia import historia
from fases import carregar_fases

PROGRESSO_PATH = "progresso.json"


class Jogo:
    def __init__(self, root):
        self.root = root
        self.root.title("🌌 LEGENDARUM 🌌")
        self.root.geometry("700x500")
        self.root.configure(bg="#1e1e2f")

        self.frame_atual = None
        self.jogador = None
        self.fases = []
        self.fase_atual = 0

        self.mostrar_menu_inicial()

    # ------------------- TROCAR DE FRAME -------------------
    def trocar_frame(self, novo_frame):
        if self.frame_atual:
            self.frame_atual.pack_forget()
        self.frame_atual = novo_frame
        self.frame_atual.pack(fill="both", expand=True)

    # ------------------- MENU INICIAL -------------------
    def mostrar_menu_inicial(self):
        frame = tk.Frame(self.root, bg="#1e1e2f")

        titulo = tk.Label(frame, text="⚔️ LEGENDARUM ⚔️",
                          font=("Georgia", 22, "bold"), bg="#1e1e2f", fg="#FFD700")
        titulo.pack(pady=20)

        tk.Label(frame, text="Digite seu nome:", font=("Arial", 12),
                 bg="#1e1e2f", fg="white").pack()
        nome_entry = tk.Entry(frame, font=("Arial", 12))
        nome_entry.pack(pady=5)

        tk.Label(frame, text="Escolha sua classe:", font=("Arial", 12),
                 bg="#1e1e2f", fg="white").pack(pady=(10, 0))
        classe_var = tk.StringVar()
        ttk.Radiobutton(frame, text="Homem", variable=classe_var, value="Homem").pack()
        ttk.Radiobutton(frame, text="Mulher", variable=classe_var, value="Mulher").pack()

        img_label = tk.Label(frame, bg="#1e1e2f")
        img_label.pack(pady=10)

        def atualizar_imagem(*_):
            caminho = os.path.join("assets", "imagempersonagem.png" if classe_var.get() == "Homem" else "imagemmulher.png")
            if os.path.exists(caminho):
                img = Image.open(caminho).resize((120, 120))
                img_tk = ImageTk.PhotoImage(img)
                img_label.config(image=img_tk)
                img_label.image = img_tk

        classe_var.trace("w", atualizar_imagem)

        def novo_jogo():
            nome = nome_entry.get().strip()
            classe = classe_var.get()
            if not nome or not classe:
                return
            self.jogador = Jogador(nome, classe)
            self.fases = carregar_fases()
            self.fase_atual = 0
            self.salvar_progresso()
            self.iniciar_historia()

        def carregar_jogo():
            if not os.path.exists(PROGRESSO_PATH):
                return
            with open(PROGRESSO_PATH, "r") as f:
                data = json.load(f)
            self.jogador = Jogador(data["nome"], data["classe"])
            self.jogador.vida = data["vida"]
            self.jogador.mana = data["mana"]
            self.jogador.xp = data["xp"]
            self.jogador.inventario = data["inventario"]
            self.jogador.habilidades = data["habilidades"]
            self.fases = carregar_fases()
            self.fase_atual = data["fase"]
            self.iniciar_historia()

        tk.Button(frame, text="🎮 Novo Jogo", font=("Arial", 14, "bold"),
                  bg="#4CAF50", fg="white", command=novo_jogo).pack(pady=10)
        tk.Button(frame, text="💾 Continuar", font=("Arial", 14, "bold"),
                  bg="#2196F3", fg="white", command=carregar_jogo).pack()

        self.trocar_frame(frame)

    # ------------------- HISTÓRIA -------------------
    def iniciar_historia(self):
        frame = tk.Frame(self.root, bg="#0f0f1f")
        label = tk.Label(frame, text="📜 História",
                         font=("Georgia", 20, "bold"), fg="#FFD700", bg="#0f0f1f")
        label.pack(pady=20)

        historia_texto = historia(self.jogador.nome, self.fase_atual)
        texto = tk.Text(frame, wrap="word", bg="#111122", fg="white",
                        font=("Consolas", 12), height=12)
        texto.insert("1.0", historia_texto)
        texto.config(state="disabled")
        texto.pack(padx=30, pady=20)

        tk.Button(frame, text="➡️ Continuar", bg="#4CAF50", fg="white",
                  font=("Arial", 14, "bold"), command=self.iniciar_fase).pack(pady=10)

        self.trocar_frame(frame)

    # ------------------- FASE E COMBATE -------------------
    def iniciar_fase(self):
        if self.fase_atual >= len(self.fases):
            self.fim_do_jogo()
            return

        fase = self.fases[self.fase_atual]
        self.iniciar_combate(fase.inimigos, fase.boss)

    def iniciar_combate(self, inimigos, boss):
        frame = tk.Frame(self.root, bg="#1a1a1a")
        label = tk.Label(frame, text=f"⚔️ Fase {self.fase_atual + 1}",
                         font=("Georgia", 18, "bold"), fg="#FFD700", bg="#1a1a1a")
        label.pack(pady=10)

        log = tk.Text(frame, width=80, height=15, bg="#0d0d0d", fg="white",
                      font=("Consolas", 10))
        log.pack(pady=10)

        frame_botoes = tk.Frame(frame, bg="#1a1a1a")
        frame_botoes.pack()

        def registrar(msg):
            log.insert(tk.END, msg + "\n")
            log.see(tk.END)

        inimigos_lista = inimigos + [boss]
        inimigo_atual = [0]

        def proximo_inimigo():
            if inimigo_atual[0] < len(inimigos_lista):
                inimigo = inimigos_lista[inimigo_atual[0]]
                registrar(f"\n👹 Um {inimigo.nome} aparece!")
                combate(self.jogador, inimigo, registrar, proximo_inimigo)
                inimigo_atual[0] += 1
            else:
                self.fase_atual += 1
                self.salvar_progresso()
                self.iniciar_historia()

        tk.Button(frame_botoes, text="▶️ Iniciar Batalha", bg="#4CAF50",
                  fg="white", font=("Arial", 12, "bold"),
                  command=proximo_inimigo).pack(pady=10)

        self.trocar_frame(frame)

    # ------------------- FIM DO JOGO -------------------
    def fim_do_jogo(self):
        frame = tk.Frame(self.root, bg="#101020")
        tk.Label(frame, text="🏁 Fim do Jogo!",
                 font=("Georgia", 22, "bold"), fg="#FFD700", bg="#101020").pack(pady=30)
        tk.Label(frame, text=f"Parabéns {self.jogador.nome}, você completou LEGENDARUM!",
                 font=("Arial", 14), fg="white", bg="#101020").pack(pady=10)
        tk.Button(frame, text="🔁 Jogar Novamente", bg="#4CAF50", fg="white",
                  font=("Arial", 14, "bold"), command=self.mostrar_menu_inicial).pack(pady=20)
        self.trocar_frame(frame)

    # ------------------- SALVAR -------------------
    def salvar_progresso(self):
        data = {
            "nome": self.jogador.nome,
            "classe": self.jogador.classe,
            "vida": self.jogador.vida,
            "mana": self.jogador.mana,
            "xp": self.jogador.xp,
            "inventario": self.jogador.inventario,
            "habilidades": self.jogador.habilidades,
            "fase": self.fase_atual
        }
        with open(PROGRESSO_PATH, "w") as f:
            json.dump(data, f, indent=4)


# ------------------- EXECUÇÃO -------------------
if __name__ == "__main__":
    root = tk.Tk()
    jogo = Jogo(root)
    root.mainloop()
