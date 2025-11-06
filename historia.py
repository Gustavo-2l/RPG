import tkinter as tk
from tkinter import messagebox


def historia(jogador=None, fase=0):
    nome = jogador if jogador else "Aventureiro"

    historias = [
        f"""
👑 REINO DE ARDANIA — O INÍCIO

Bem-vindo, {nome}...

Um rei conquistador encontra paz ao formar uma família.
Durante uma festa em celebração à paz, o castelo é atacado por um guerreiro misterioso.
O príncipe tenta defender o reino, mas é derrotado e resgatado pela general, enquanto o rei e a rainha morrem.
Sozinho e rejeitado por outros reinos, o príncipe decide buscar as lendas antigas, heróis capazes de ajudá-lo a restaurar o reino e derrotar o inimigo sombrio.
""",
        f"""
🌲 FLORESTA DE LUNYSSE — PRIMEIRO DESPERTAR

{nome} atravessa florestas densas onde o tempo parece não passar.
As árvores sussurram seu nome... e uma voz responde.

🧙‍♂️ Sábio Ancião: "Você busca poder, jovem príncipe... ou redenção?"

👤 {nome}: "Busco justiça. Meu reino caiu, e só as Lendas podem me ajudar."

🧙‍♂️ Sábio Ancião: "Então prove ser digno. Derrote os espíritos guardiões
e as Lendas talvez escutem seu chamado."
""",
        f"""
🏰 RUÍNAS DE VALKAR — ECO DAS ESPADAS

Os ecos de antigas batalhas ressoam pelas paredes quebradas.
Entre elas, o espírito de um guerreiro surge, empunhando uma lâmina flamejante.

🔥 Lenda do Fogo: "Você... ousa perturbar meu descanso?"

👤 {nome}: "Não vim roubar teu poder. Vim lutar ao teu lado."

🔥 Lenda do Fogo: "Então lute, mortal. Mostre se é digno de portar uma chama eterna!"
""",
        f"""
🌋 FORTALEZA DAS SOMBRAS — CONFRONTO FINAL

As muralhas tremem. Raios cortam o céu escarlate.
O inimigo de outrora, o Guerreiro Negro, aguarda.

⚔️ Guerreiro Negro: "Você cresceu, príncipe. Mas coragem não é poder."

👤 {nome}: "Não preciso de poder. Tenho fé nas Lendas... e no legado do meu pai!"

⚔️ Guerreiro Negro: "Então venha! Mostre-me a força do seu destino!"

O destino do mundo será decidido agora...
"""
    ]

    if fase < len(historias):
        historia_texto = historias[fase]
    else:
        historia_texto = f"""
🌌 EPÍLOGO

{nome}, sua jornada terminou, mas as Lendas viverão em sua memória.
O reino renasceu das cinzas — e o mundo voltará a cantar seu nome.
"""

    # --- Janela ---
    janela = tk.Toplevel()
    janela.title("🌌 LEGENDARUM 🌌")
    janela.geometry("800x600")
    janela.config(bg="#0d0d0d")

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
        relief="flat",
        state="disabled"
    )
    texto_widget.pack(pady=(0, 20))

    # --- Função para escrever o texto ---
    def escrever_texto(index=0):
        if not janela.winfo_exists():
            return
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
            botao_fechar.pack(pady=15)
            botao_pular.pack_forget()  # Esconde o botão pular após terminar

    # --- Botões ---
    def iniciar_historia():
        botao_iniciar.destroy()
        escrever_texto(0)

    def encerrar():
        messagebox.showinfo("Fim", "A história começa agora, herdeiro das lendas...")
        janela.destroy()

    def pular_historia():
        # Mostra mensagem rápida e fecha
        texto_widget.configure(state="normal")
        texto_widget.delete(1.0, tk.END)
        texto_widget.insert(tk.END, "História pulada...\n")
        texto_widget.configure(state="disabled")
        botao_fechar.pack(pady=15)
        botao_pular.pack_forget()  # Oculta botão após pular

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

    botao_pular = tk.Button(
        frame,
        text="⏩ Pular História",
        command=pular_historia,
        font=("Arial", 12, "bold"),
        bg="#333333",
        fg="#FFFFFF",
        width=20,
        height=2
    )
    botao_pular.pack(pady=10)

    janela.grab_set()
    janela.wait_window()
