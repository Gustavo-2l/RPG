import random

class Jogador:
    def __init__(self, nome, classe):
        self.nome = nome
        self.classe = classe
        self.nivel = 1
        self.xp = 0
        self.vida_max = 100
        self.vida = self.vida_max
        self.mana_max = 60
        self.mana = self.mana_max
        self.inventario = {"poção": 3}
        self.habilidades = ["Golpe Forte"]  # Para o seu label de habilidades
        self.defendendo = False

    def atacar(self):
        # Retorna dano aleatório
        return random.randint(10, 20)

    def ganhar_xp(self, xp):
        self.xp += xp
        if self.xp >= 100:
            self.nivel += 1
            self.xp -= 100
            self.vida_max += 20
            self.vida = self.vida_max
            self.mana_max += 10
            self.mana = self.mana_max

    # Você pode adicionar outros métodos como habilidade especial, esquiva, etc.
