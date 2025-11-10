import tkinter as tk
from models.inimigo import Inimigo
import os


class Fase:
    def __init__(self, nome, inimigos=None, boss=None, lendas=None, historia=None, caminho_fundo="assets/Florestaprofunda.png"):
        self.nome = nome
        self.inimigos = inimigos
        self.boss = boss
        self.lendas = lendas
        self.historia = historia
        self.caminho_fundo = caminho_fundo

    def iniciar(self, jogador, combate_func, ao_terminar=None):
        """
        Executa os combates da fase em sequência (inimigos -> boss),
        e depois chama o callback `ao_terminar(resultado)`.
        """

        janela_historia = tk.Toplevel()
        janela_historia.title(f"📖 {self.nome}")
        janela_historia.geometry("600x400")
        janela_historia.configure(bg="#1e1e2f")

        texto = tk.Text(janela_historia, bg="#1e1e2f", fg="white",
                        wrap="word", font=("Georgia", 12))
        texto.pack(fill="both", expand=True, padx=20, pady=20)

        for linha in self.historia:
            texto.insert(tk.END, linha + "\n\n")
        texto.config(state="disabled")

        def iniciar_batalhas():
            janela_historia.destroy()
            executar_batalha(0)

        tk.Button(
            janela_historia, text="▶ Continuar", bg="#4CAF50", fg="white",
            font=("Arial", 12, "bold"), command=iniciar_batalhas
        ).pack(pady=10)

        # --- Lógica de combates sequenciais ---
        def executar_batalha(indice_inimigo):
            """Executa o combate contra o inimigo no índice atual."""
            if indice_inimigo < len(self.inimigos):
                inimigo = self.inimigos[indice_inimigo]

                def fim_inimigo(resultado):
                    if resultado == "derrota":
                        if ao_terminar:
                            ao_terminar("derrota")
                        return
                    # Próximo inimigo
                    executar_batalha(indice_inimigo + 1)

                combate_func(jogador, inimigo, self.caminho_fundo, on_fim=fim_inimigo)

            else:
                # Todos inimigos normais derrotados → boss
                if self.boss:
                    def fim_boss(resultado):
                        if resultado == "derrota":
                            if ao_terminar:
                                ao_terminar("derrota")
                            return

                        # Conquistou a fase
                        for lenda in self.lendas:
                            if lenda not in jogador.habilidades:
                                jogador.habilidades.append(lenda)

                        if ao_terminar:
                            ao_terminar("vitoria")

                    combate_func(jogador, self.boss, self.caminho_fundo, on_fim=fim_boss)
                else:
                    if ao_terminar:
                        ao_terminar("vitoria")


# --- Fases de exemplo ---
def carregar_fases():
    fases = []

    # 🏞️ FASE 1 - Floresta das Cinzas
    inimigos_fase1 = [
        Inimigo("Lobo Selvagem", 30, 5, 10),
        Inimigo("Lobo Alfa", 40, 7, 20),
    ]
    boss1 = Inimigo("Caçador de Recompensa", 45, 10, 30)
    lendas1 = ["Mago Criomante"]
    historia1 = [
        "Você entra na Floresta das Cinzas...",
        "O ar é denso e cheio de névoa. Sons de criaturas ecoam entre as árvores.",
        "Entre o nevoeiro, surge um mago misterioso...",
        "Ele se apresenta como o Mago Criomante e observa seus passos com atenção."
    ]
    fase1 = Fase(
        "Floresta das Cinzas",
        inimigos=inimigos_fase1,
        boss=boss1,
        lendas=lendas1,
        historia=historia1,
        caminho_fundo="assets/Florestaprofunda.png"
    )

    # ❄️ FASE 2 - Montanhas Geladas
    inimigos_fase2 = [
        Inimigo("Lobo Selvagem", 45, 8, 25),
        Inimigo("Caçadora Fantasma", 50, 9, 30),
    ]
    boss2 = Inimigo("Lobisomem Alfa", 80, 12, 60)
    lendas2 = ["Lobisomem", "Caçadora"]
    historia2 = [
        "As montanhas geladas se erguem diante de você.",
        "O vento uiva como um lamento distante...",
        "Entre as neves, você sente presenças antigas — a Caçadora e o Lobisomem Alfa te observam.",
        "Após a batalha, ambos reconhecem sua força e decidem se unir à sua jornada."
    ]
    fase2 = Fase(
        "Montanhas Geladas",
        inimigos=inimigos_fase2,
        boss=boss2,
        lendas=lendas2,
        historia=historia2,
        caminho_fundo="assets/MontanhasGeladas.png"
    )

    fases.append(fase1)
    fases.append(fase2)

    return fases
