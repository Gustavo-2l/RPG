import tkinter as tk
from tkinter import messagebox


def historia(jogador=None):
    nome = jogador if jogador else "Aventureiro"

    # Cria a janela principal
    janela = tk.Toplevel()  # usa Toplevel para não criar uma nova root
    janela.title("🌌 LEGENDARUM 🌌")
    janela.geometry("800x600")
    janela.config(bg="#0d0d0d")

    # Frame principal
    frame = tk.Frame(janela, bg="#0d0d0d")
    frame.pack(expand=True, fill="both", padx=40, pady=40)

    # Título
    titulo = tk.Label(
        frame,
        text="🌌 LEGENDARUM 🌌",
        font=("Georgia", 20, "bold"),
        fg="#FFD700",
        bg="#0d0d0d"
    )
    titulo.pack(pady=(0, 20))

    # Área de texto
    texto_widget = tk.Text(
        frame,
        wrap="word",
        font=("Consolas", 12),
        fg="#FFFFFF",
        bg="#111111",
        height=20,
        width=80,
        relief="flat",
        state="disabled"
    )
    texto_widget.pack(pady=(0, 20))

    historia_texto = f"""
Bem-vindo, {nome}!

Um rei conquistador encontra paz ao formar uma família.
Durante uma festa em celebração à paz, o castelo é atacado por um guerreiro misterioso.
O príncipe tenta defender o reino, mas é derrotado e resgatado pela general, enquanto o rei e a rainha morrem.
Sozinho e rejeitado por outros reinos, o príncipe decide buscar as lendas antigas, heróis capazes de ajudá-lo a restaurar o reino e derrotar o inimigo sombrio.
"""

    # --- Função para escrever o texto com efeito de digitação ---
    def escrever_texto(index=0):
        if not janela.winfo_exists():
            return  # Evita erros se a janela for fechada

        if index < len(historia_texto):
            texto_widget.configure(state="normal")
            texto_widget.insert(tk.END, historia_texto[index])
            texto_widget.see(tk.END)
            texto_widget.configure(state="disabled")
            janela.after(25, lambda: escrever_texto(index + 1))
        else:
            texto_widget.configure(state="normal")
            texto_widget.insert(tk.END, "\n\nAperte 'Fechar' para continuar sua jornada...")
            texto_widget.configure(state="disabled")

            # Exibe botão de encerrar após o texto
            botao_fechar.pack(pady=15)

    # --- Botão inicial ---
    def iniciar_historia():
        botao_iniciar.destroy()
        escrever_texto(0)

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

    # --- Botão de fechar (aparece só no final) ---
    def encerrar():
        messagebox.showinfo("Fim", "A história começa agora, herdeiro das lendas...")
        janela.destroy()  # Fecha a janela para continuar o jogo

    botao_fechar = tk.Button(
        frame,
        text="Fechar",
        command=encerrar,
        font=("Arial", 12, "bold"),
        bg="#550000",
        fg="#FFFFFF",
        width=15,
        height=2
    )

    # Bloqueia a execução do jogo até a janela fechar
    janela.grab_set()
    janela.wait_window()
