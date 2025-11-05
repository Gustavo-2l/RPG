import tkinter as tk
from inimigo import Inimigo

class Fase:
    def __init__(self, nome, inimigos, boss, lendas, historia):
        self.nome = nome
        self.inimigos = inimigos
        self.boss = boss
        self.lendas = lendas
        self.historia = historia

    def iniciar(self, jogador, combate_func):
        """
        Executa os combates em sequência (inimigos -> boss).
        Retorna True se o jogador venceu tudo, False se morreu.
        """
        for inimigo in self.inimigos:
            resultado = combate_func(jogador, inimigo)
            if not resultado:
                return False  # jogador foi derrotado

        # Combate contra o boss
        if self.boss:
            resultado_boss = combate_func(jogador, self.boss)
            if not resultado_boss:
                return False

        # Recruta lendas após vencer
        for lenda in self.lendas:
            if lenda not in jogador.habilidades:
                jogador.habilidades.append(lenda)

        return True


# --- Fases de exemplo ---
def carregar_fases():
    fases = []

    # Fase 1
    inimigos_fase1 = [
        Inimigo("Goblin", 30, 5, 20),
        Inimigo("Orc", 40, 7, 30),
    ]
    boss1 = Inimigo("Mago das Chamas", 60, 10, 50)
    lendas1 = ["Mago Criomante"]
    historia1 = [
        "Você entra na floresta das cinzas...",
        "Entre o nevoeiro surge um mago misterioso...",
        "Ele se apresenta como o Mago Criomante e decide juntar-se a você!"
    ]
    fase1 = Fase("Floresta das Cinzas", inimigos_fase1, boss1, lendas1, historia1)

    # Fase 2
    inimigos_fase2 = [
        Inimigo("Lobo Selvagem", 45, 8, 25),
        Inimigo("Caçadora Fantasma", 50, 9, 30),
    ]
    boss2 = Inimigo("Lobisomem Alfa", 80, 12, 60)
    lendas2 = ["Lobisomem", "Caçadora"]
    historia2 = [
        "As montanhas geladas guardam segredos sombrios...",
        "Após derrotar o Alfa, o Lobisomem e a Caçadora unem forças com você."
    ]
    fase2 = Fase("Montanhas Geladas", inimigos_fase2, boss2, lendas2, historia2)

    fases.append(fase1)
    fases.append(fase2)

    return fases
