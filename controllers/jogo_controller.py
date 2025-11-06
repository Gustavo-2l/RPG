import tkinter as tk
from tkinter import messagebox
from models.jogador import Jogador
from views.main_view import MainView
from combate import combate
from historia import historia
from fases import carregar_fases


class JogoController:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.view = MainView(root, self.iniciar_jogo)

    # --- Função principal do jogo ---
    def iniciar_jogo(self, nome, classe):
        if not nome:
            messagebox.showwarning("Aviso", "Digite o nome do seu personagem!")
            return
        if not classe:
            messagebox.showwarning("Aviso", "Escolha o gênero do seu personagem!")
            return

        jogador = Jogador(nome, classe)
        self.root.withdraw()  # Fecha menu inicial

        historia(jogador.nome)
        fases = carregar_fases()

        if not fases:
            messagebox.showerror("Erro", "Nenhuma fase foi carregada!")
            self.root.deiconify()
            return

        self.iniciar_fase(jogador, fases)

    # --- Gerencia as fases ---
    def iniciar_fase(self, jogador, fases, indice_fase=0):
        if indice_fase >= len(fases):
            messagebox.showinfo("🏁 Fim do Jogo", f"Parabéns {jogador.nome}! Você completou todas as fases!")
            self.root.destroy()
            return

        fase = fases[indice_fase]
        inimigos = fase.inimigos + ([fase.boss] if fase.boss else [])
        indice_inimigo = 0

        def iniciar_proximo_inimigo():
            nonlocal indice_inimigo
            if indice_inimigo >= len(inimigos):
                for lenda in fase.lendas:
                    if lenda not in jogador.habilidades:
                        jogador.habilidades.append(lenda)
                print(f"✅ Fase {fase.nome} concluída!")
                self.iniciar_fase(jogador, fases, indice_fase + 1)
                return

            inimigo_atual = inimigos[indice_inimigo]

            def ao_terminar(resultado=None):
                nonlocal indice_inimigo
                if resultado == "derrota" or jogador.vida <= 0:
                    messagebox.showinfo("💀 Derrota", f"{jogador.nome} foi derrotado!")
                    self.root.destroy()
                    return

                indice_inimigo += 1
                iniciar_proximo_inimigo()

            combate(jogador, inimigo_atual, fase.caminho_fundo, on_fim=ao_terminar)

        iniciar_proximo_inimigo()
