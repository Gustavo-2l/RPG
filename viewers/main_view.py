import tkinter as tk
from PIL import Image, ImageTk
import os


class MainView:
    def __init__(self, root, on_iniciar):
        self.root = root
        self.on_iniciar = on_iniciar
        self.root.title("🌌 LEGENDARUM 🌌")
        self.root.geometry("420x480")
        self.root.configure(bg="#1e1e2f")

        self._montar_interface()

    def _montar_interface(self):
        titulo = tk.Label(
            self.root, text="⚔️ LEGENDARUM ⚔️",
            font=("Georgia", 18, "bold"), bg="#1e1e2f", fg="#FFD700"
        )
        titulo.pack(pady=20)

        # Nome do personagem
        tk.Label(self.root, text="Digite seu nome:", font=("Arial", 12),
                 bg="#1e1e2f", fg="white").pack()
        self.entrada_nome = tk.Entry(self.root, font=("Arial", 12))
        self.entrada_nome.pack(pady=5)

        # Escolha de classe
        tk.Label(self.root, text="Escolha sua classe:", font=("Arial", 12),
                 bg="#1e1e2f", fg="white").pack(pady=(10, 0))

        self.classe_var = tk.StringVar(value="")
        self.classe_var.trace("w", self._atualizar_personagem)

        frame_classes = tk.Frame(self.root, bg="#1e1e2f")
        frame_classes.pack(pady=5)

        tk.Radiobutton(frame_classes, text="Homem", variable=self.classe_var,
                       value="Homem", bg="#1e1e2f", fg="white", selectcolor="#333").pack(side="left", padx=10)
        tk.Radiobutton(frame_classes, text="Mulher", variable=self.classe_var,
                       value="Mulher", bg="#1e1e2f", fg="white", selectcolor="#333").pack(side="left", padx=10)

        self.label_personagem = tk.Label(self.root, bg="#1e1e2f")
        self.label_personagem.pack(pady=15)

        # Botão iniciar
        botao_iniciar = tk.Button(
            self.root, text=" Iniciar Jogo",
            font=("Arial", 14, "bold"), bg="#4CAF50", fg="white",
            command=self._iniciar
        )
        botao_iniciar.pack(pady=20)

    def _atualizar_personagem(self, *args):
        classe = self.classe_var.get()
        if not classe:
            return

        if classe == "Homem":
            caminho_imagem = os.path.join("assets", "imagempersonagem.png")
        else:
            caminho_imagem = os.path.join("assets", "imagemmulher.png")

        if not os.path.exists(caminho_imagem):
            print(f"⚠️ Imagem não encontrada: {caminho_imagem}")
            return

        imagem = Image.open(caminho_imagem).resize((120, 120))
        imagem_tk = ImageTk.PhotoImage(imagem)

        self.label_personagem.config(image=imagem_tk)
        self.label_personagem.image = imagem_tk

    def _iniciar(self):
        nome = self.entrada_nome.get().strip()
        classe = self.classe_var.get()
        self.on_iniciar(nome, classe)
