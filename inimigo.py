import random
import time
from colorama import Fore, Style, init

# Inicializa o colorama para efeitos de cor no console
init(autoreset=True)

class Inimigo:
    def __init__(self, nome, vida, forca, xp_inimigo, tipo="Normal", descricao=None):
        self.nome = nome
        self.vida = vida
        self.vida_max = vida
        self.forca = forca
        self.xp_inimigo = xp_inimigo
        self.tipo = tipo  # Ex: "Boss", "Elite", "Normal"
        self.descricao = descricao or "Um inimigo misterioso aparece..."
        self.vivo = True

    # --- Métodos principais ---
    def atacar(self):
        """Inimigo realiza um ataque com dano variável baseado na força."""
        dano_base = random.randint(self.forca - 3, self.forca + 3)
        dano_bonus = random.randint(0, 5)
        dano_total = max(1, dano_base + dano_bonus)

        cor = Fore.RED if self.tipo == "Boss" else Fore.YELLOW
        print(f"\n{cor}👹 {self.nome} ataca ferozmente causando {dano_total} de dano!{Style.RESET_ALL}")
        time.sleep(0.4)
        return dano_total

    def receber_dano(self, dano):
        """Reduz a vida do inimigo ao ser atacado."""
        self.vida -= dano
        if self.vida <= 0:
            self.vida = 0
            self.vivo = False
            print(f"{Fore.LIGHTBLACK_EX}💀 {self.nome} foi derrotado!{Style.RESET_ALL}")
        else:
            print(f"{Fore.LIGHTRED_EX}⚔️ {self.nome} agora tem {self.vida}/{self.vida_max} de vida.{Style.RESET_ALL}")

    def resetar(self):
        """Restaura a vida do inimigo ao máximo (caso necessário em repetições de fase)."""
        self.vida = self.vida_max
        self.vivo = True

    def apresentar(self):
        """Exibe informações do inimigo com estilo."""
        cor = Fore.MAGENTA if self.tipo == "Boss" else Fore.CYAN
        print(f"\n{cor}=== ⚔️ {self.nome.upper()} ({self.tipo}) ⚔️ ==={Style.RESET_ALL}")
        print(f"❤️ Vida: {self.vida}/{self.vida_max}")
        print(f"💪 Força: {self.forca}")
        print(f"⭐ XP ao derrotar: {self.xp_inimigo}")
        print(f"📖 Descrição: {self.descricao}")
        print(f"{'-'*40}")

    def esta_vivo(self):
        """Retorna True se o inimigo ainda estiver vivo."""
        return self.vivo

    # --- Efeito especial para bosses ---
    def rugido(self):
        """Apenas Bosses executam um rugido de intimidação."""
        if self.tipo.lower() == "boss":
            print(f"\n{Fore.RED}🔥 {self.nome} solta um rugido ensurdecedor! Seu poder aumenta temporariamente! 🔥{Style.RESET_ALL}")
            bonus = random.randint(3, 6)
            self.forca += bonus
            print(f"{Fore.LIGHTYELLOW_EX}+{bonus} de força temporária!{Style.RESET_ALL}")
            time.sleep(0.5)
