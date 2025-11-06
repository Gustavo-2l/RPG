import random

class Jogador:
    def __init__(self, nome, classe):
        self.nome = nome
        self.classe = classe
        self.nivel = 1
        self.xp = 0
        self.vida_max = 35
        self.vida = self.vida_max
        self.mana_max = 60
        self.mana = self.mana_max
        self.inventario = {"poção": 3}
        self.habilidade_desbloqueada = None
        self.habilidades = []  # Lista de habilidades que o jogador possui
        self.defendendo = False

    def atacar(self):
        # Retorna dano aleatório
        return random.randint(10, 20)

    def esquivar(self):
        # Chance de esquivar de um ataque: 30%
        chance = random.random()  # 0.0 a 1.0
        if chance <= 0.3:
            return True
        return False

    def usar_habilidade(self, inimigo):
        # Habilidade especial: dano maior que ataque normal, consome mana
        if self.habilidade_desbloqueada and self.mana >= 20:
            self.mana -= 20
            dano = random.randint(25, 40)
            inimigo.vida -= dano
            return dano
        return 0  # Caso não tenha mana ou habilidade

    def usar_item(self, item):
        if item in self.inventario and self.inventario[item] > 0:
            if item == "poção":
                cura = 30
                self.vida = min(self.vida + cura, self.vida_max)
                self.inventario[item] -= 1
                return f"{self.nome} usou uma poção e recuperou {cura} de vida!"
            # Aqui você pode adicionar outros itens, como "mana" ou "elixir"
        return f"{self.nome} não tem {item} no inventário."

    def ganhar_xp(self, xp):
        self.xp += xp
        if self.xp >= 100:
            self.nivel += 1
            self.xp -= 100
            self.vida_max += 20
            self.vida = self.vida_max
            self.mana_max += 10
            self.mana = self.mana_max
            return f"{self.nome} subiu para o nível {self.nivel}!"
        return None
