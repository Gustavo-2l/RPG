import random

class Inimigo:
    def __init__(self, nome, vida, forca, xp_inimigo, ouro_inimigo):
        self.nome = nome
        self.vida = vida
        self.vida_max = vida
        self.forca = forca
        self.xp_inimigo = xp_inimigo
        self.ouro_inimigo = ouro_inimigo

    def atacar(self):
        dano = self.forca + random.randint(1, 10)
        print(f"\n👹 {self.nome} ataca causando {dano} de dano!")
        return dano
