import random

class Jogador:
    def __init__(self, nome, classe):
        self.nome = nome
        self.classe = classe
        self.nivel = 1
        self.xp = 0
        self.xp_proximo_nivel = 100
        self.ouro = 50
        self.reliquias = 0
        self.habilidade_desbloqueada = None
        self.mana_max = 60 if classe == "Homem" else 100

        if classe == "Homem":
            self.vida_max = 60
            self.forca = 5
            self.defesa = 6
            self.agilidade = 4
            self.inteligencia = 7
        elif classe == "Mulher":
            self.vida_max = 60
            self.forca = 5
            self.defesa = 6
            self.agilidade = 4
            self.inteligencia = 7

        self.vida = self.vida_max
        self.mana = self.mana_max
        self.inventario = {"poção de vida": 4, "poção de mana": 4}

        # Buffs temporários
        self.furia_ativa = False
        self.reflexos_ativos = 0
        self.muralha_ativa = 0

    # === Ações de combate ===
    def atacar(self):
        dano = self.forca + random.randint(1, 10)
        print(f"\n⚔️ {self.nome} ataca causando {dano} de dano!")
        return dano

    def defender_acao(self):
        bonus = random.randint(5, 12)
        self.defesa += bonus
        print(f"\n🛡️ {self.nome} se defende, aumentando a defesa em {bonus} pontos!")
        return bonus

    def restaurar_defesa(self, bonus):
        self.defesa -= bonus

    def defender(self, dano_recebido):
        dano_final = max(dano_recebido - self.defesa, 0)
        self.vida -= dano_final
        if dano_final > 0:
            print(f"💥 {self.nome} sofreu {dano_final} de dano após defesa!")
        else:
            print(f"🛡️ {self.nome} bloqueou totalmente o ataque!")
        return dano_final

    def esquivar(self):
        chance_esquiva = min(self.agilidade * 10, 100)
        rolagem = random.randint(1, 100)
        print(f"\n🌀 {self.nome} tenta se esquivar! (Chance: {chance_esquiva}%)")

        if rolagem <= chance_esquiva:
            print(f"✨ {self.nome} desvia do ataque!")
            return True
        else:
            print(f"💥 {self.nome} foi atingido!")
            return False

    def usar_item(self, item):
        if item in self.inventario and self.inventario[item] > 0:
            self.inventario[item] -= 1
            if item == "poção de vida":
                cura = random.randint(20, 40)
                self.vida = min(self.vida + cura, self.vida_max)
                print(f"\n💖 Você recuperou {cura} de vida!")
            elif item == "poção de mana":
                mana_recuperada = random.randint(20, 40)
                self.mana = min(self.mana + mana_recuperada, self.mana_max)
                print(f"\n🔮 Você recuperou {mana_recuperada} de mana!")
        else:
            print("\n❌ Item não disponível!")

    # === Experiência e evolução ===
    def ganhar_xp(self, xp):
        self.xp += xp
        print(f"\n🎯 Você ganhou {xp} XP!")
        if self.xp >= self.xp_proximo_nivel:
            self.subir_nivel()

    def subir_nivel(self):
        self.nivel += 1
        self.xp = 0
        self.xp_proximo_nivel += 50
        self.vida_max += 20
        self.mana_max += 10
        self.forca += 3
        self.defesa += 3
        self.agilidade += 2
        self.inteligencia += 2
        self.vida = self.vida_max
        self.mana = self.mana_max

        print(f"\n🎉 PARABÉNS {self.nome}! Subiu para o nível {self.nivel}!")
        input("Pressione ENTER para continuar...")

    # === Habilidades ===
    def usar_habilidade(self, inimigo):
        habilidades = {
            "Gourdrak": {"nome": "Golpe Assombrado", "descricao": "Ataque sombrio poderoso", "custo_mana": 20},
            "Skorgar": {"nome": "Fúria da Floresta", "descricao": "Aumenta dano temporariamente", "custo_mana": 25},
            "Septinara": {"nome": "Regeneração Felina", "descricao": "Aumenta chance de esquiva", "custo_mana": 20},
            "Caçadora Sangravil": {"nome": "Tiro Preciso", "descricao": "Dano crítico massivo", "custo_mana": 30},
            "Mago Zarion": {"nome": "Nevasca Mágica", "descricao": "Dano mágico direto", "custo_mana": 35},
        }

        if not self.habilidade_desbloqueada:
            print("\n❌ Nenhuma habilidade desbloqueada!")
            return False

        habilidade = habilidades.get(self.habilidade_desbloqueada)
        if not habilidade or self.mana < habilidade["custo_mana"]:
            print(f"\n❌ Mana insuficiente para usar {habilidade['nome']}!")
            return False

        self.mana -= habilidade["custo_mana"]
        print(f"\n✨ {self.nome} usa {habilidade['nome']}! {habilidade['descricao']}")

        if habilidade["nome"] == "Golpe Assombrado":
            dano = self.forca + 25 + random.randint(5, 15)
            inimigo.vida -= dano
            print(f"O ataque causa {dano} de dano!")

        elif habilidade["nome"] == "Tiro Preciso":
            dano = self.forca * 3 + random.randint(20, 40)
            inimigo.vida -= dano
            print(f"O ataque crítico causa {dano} de dano!")

        elif habilidade["nome"] == "Nevasca Mágica":
            dano = 40 + self.inteligencia * 2
            inimigo.vida -= dano
            print(f"O ataque mágico causa {dano} de dano!")

        return True
def curar_pos_batalha(jogador):
    jogador.vida = jogador.vida_max
    jogador.mana = jogador.mana_max
    print(f"\n💖 {jogador.nome} foi totalmente curado após a batalha!")
