import tkinter as tk
import time
from tkinter import messagebox
from jogador import Jogador

def historia(jogador=None):
    nome = jogador if jogador else "Aventureiro"

    # Cria a janela principal
    janela = tk.Tk()
    janela.title("🌌 LEGENDARUM🌌")
    janela.geometry("800x600")
    janela.config(bg="#0d0d0d")

    # Frame para centralizar o conteúdo
    frame = tk.Frame(janela, bg="#0d0d0d")
    frame.pack(expand=True, fill="both", padx=40, pady=40)

    titulo = tk.Label(
        frame,
        text="🌌 LEGENDARUM 🌌",
        font=("Georgia", 20, "bold"),
        fg="#FFD700",
        bg="#0d0d0d"
    )
    titulo.pack(pady=(0, 20))

    texto_widget = tk.Text(
        frame,
        wrap="word",
        font=("Consolas", 12),
        fg="#FFFFFF",
        bg="#111111",
        height=20,
        width=80,
        relief="flat"
    )
    texto_widget.pack(pady=(0, 20))
    texto_widget.configure(state="disabled")

    def escrever_texto(texto, delay=40):
        """Efeito de digitação no texto"""
        texto_widget.configure(state="normal")
        for char in texto:
            texto_widget.insert(tk.END, char)
            texto_widget.see(tk.END)
            texto_widget.update()
            time.sleep(delay / 1000)
        texto_widget.insert(tk.END, "\n")
        texto_widget.configure(state="disabled")

    historia_texto = f"""
Bem-vindo, {jogador}!

Um rei conquistador encontra paz ao formar uma família.
Durante uma festa em celebração à paz, o castelo é atacado por um guerreiro misterioso.
O príncipe tenta defender o reino, mas é derrotado e resgatado pela general, enquanto o rei e a rainha morrem.
Sozinho e rejeitado por outros reinos, o príncipe decide buscar as lendas antigas, heróis capazes de ajudá-lo a restaurar o reino e derrotar o inimigo sombrio.
"""

    # Função para iniciar o texto com efeito de digitação
    def iniciar_historia():
        botao_iniciar.destroy()
        janela.after(200, lambda: escrever_texto(historia_texto, 25))

    botao_iniciar = tk.Button(
        frame,
        text="▶ Iniciar História",
        command=iniciar_historia,
        font=("Arial", 12, "bold"),
        bg="#333333",
        fg="#FFD700",
        width=20,
        height=2
    )
    botao_iniciar.pack()

    def encerrar():
        messagebox.showinfo("Fim", "A história começa agora, herdeiro das lendas...")
        janela.destroy()

    botao_sair = tk.Button(
        frame,
        text="Fechar",
        command=encerrar,
        font=("Arial", 10, "bold"),
        bg="#222",
        fg="white",
        width=10
    )
    botao_sair.pack(pady=(10, 0))

    janela.mainloop()
