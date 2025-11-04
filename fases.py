import tkinter as tk
from tkinter import messagebox
from inimigo import Inimigo

class Fase:
    def __init__(self, nome, inimigos, boss, lendas, historia):
        self.nome = nome
        self.inimigos = inimigos
        self.boss = boss
        self.lendas = lendas  # Lista de lendas que podem ser recrutadas
        self.historia = historia  # Lista de intercessões
        self.janela = None
        self.texto_widget = None

    def iniciar(self, jogador, combate_callback):
        """Inicia a fase, mostrando a janela de diálogo inicial"""
        self.janela = tk.Tk()
        self.janela.title(f"Fase: {self.nome}")

        self.texto_widget = tk.Text(self.janela, width=60, height=10, font=("Arial", 12))
        self.texto_widget.pack(pady=10)

        self.dialogo(self.historia, callback=lambda: self.iniciar_combate(jogador, combate_callback))

        self.janela.mainloop()

    def dialogo(self, dialogos, index=0, callback=None):
        """Mostra os diálogos na janela"""
        if index >= len(dialogos):
            if callback:
                callback()
            return

        dialogo_atual = dialogos[index]
        self.texto_widget.delete("1.0", tk.END)
        self.texto_widget.insert(tk.END, f"{dialogo_atual.get('personagem', 'Narrador')}: {dialogo_atual.get('fala', '')}\n")

        # Remove botões antigos
        for widget in self.janela.winfo_children():
            if isinstance(widget, tk.Button):
                widget.destroy()

        # Cria botões de resposta
        for resp in dialogo_atual.get("respostas", [{"texto": "Continuar", "proximo": index + 1}]):
            btn = tk.Button(
                self.janela,
                text=resp["texto"],
                font=("Arial", 12, "bold"),
                bg="#2b2b4f",
                fg="white",
                width=25,
                height=2,
                command=lambda p=resp["proximo"]: self.dialogo(dialogos, p, callback)
            )
            btn.pack(pady=5)

    def iniciar_combate(self, jogador, combate_callback):
        """Chama o callback de combate depois do diálogo"""
        self.janela.destroy()
        combate_callback(jogador, self.inimigos, self.boss, self.lendas)
