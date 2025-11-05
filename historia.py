import tkinter as tk
from tkinter import messagebox


def historia(jogador=None, fase=0):
    nome = jogador if jogador else "Aventureiro"

    # Textos e diálogos das fases
    historias = [
        f"""
👑 REINO DE ARDANIA — O INÍCIO

Bem-vindo, {nome}...

Um rei conquistador encontra paz ao formar uma família.
Durante a festa da vitória, o castelo é atacado por um guerreiro misterioso.
O príncipe tenta defender o reino, mas é derrotado e resgatado pela general,
enquanto o rei e a rainha tombam diante das chamas.

Sem lar e sem exército, o príncipe jura restaurar seu trono
e parte em busca das antigas Lendas — heróis esquecidos do tempo.
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

    # Escolhe o texto da fase
    if fase < len(historias):
        historia_texto = historias[fase]
    else:
        historia_texto = f"""
🌌 EPÍLOGO

{nome}, sua jornada terminou, mas as Lendas viverão em sua memória.
O reino renasceu das cinzas — e o mundo voltará a cantar seu nome.
"""
    # --- Criação da janela ---
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

    # --- Função para escrever o texto com efeito de digitação ---
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

    # --- Botão de fechar ---
    def encerrar():
        messagebox.showinfo("Fim", "A história começa agora, herdeiro das lendas...")
        janela.destroy()

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

    # Bloqueia a execução até a janela fechar
    janela.grab_set()
    janela.wait_window()
