Sobre o Projeto
 
LEGENDARUM é um jogo de RPG em Python que combina história interativa, combates por turnos e interface visual para criar uma experiência imersiva e divertida.
 
O jogador cria seu personagem (nome e gênero), vive uma narrativa envolvente e enfrenta inimigos através de fases progressivas, com imagens e mensagens que marcam a evolução do herói.
 -------------------------------------------------------------------------------------------------------------------------------------------------------------
 Tecnologias Utilizadas
Tecnologia  Função
Python  Linguagem principal do projeto
Tkinter Criação da interface gráfica (menus, botões, janelas)
Pillow (PIL)  Exibição e manipulação de imagens dos personagens
Módulos internos (jogador, inimigo, combate, historia, fases) Organização do código em partes reutilizáveis e separadas
 --------------------------------------------------------------------------------------------------------------------------------------------------------------
 Como o Jogo Funciona
 
O jogador insere seu nome.
 
Escolhe o gênero/classe do personagem (Homem ou Mulher).
 
Uma história introdutória é exibida, preparando para a aventura.
 
O jogo carrega as fases e inicia os combates sequenciais.
 
O jogador vence inimigos, desbloqueia habilidades e avança até o final.
 
Caso a vida do jogador chegue a 0, é exibido o Game Over.
 
Ao vencer todas as fases, o jogador recebe uma mensagem de conclusão épica
 ----------------------------------------------------------------------------------------------------------------------------------------------------------------
 
 Interface Visual
 
A interface é criada inteiramente com Tkinter, priorizando:
 
Design temático (cores sombrias e minimalistas);
 
Leitura intuitiva;
 
Componentes organizados (título, entrada de nome, seleção de classe, imagem e botão de início).
 
Estrutura Visual:
 
Título → “⚔️ LEGENDARUM ⚔️”
 
Entrada de nome → campo de texto
 
Seleção de classe → botões “Homem” / “Mulher”
 
Imagem do personagem → atualiza conforme a classe escolhida
 
Botão "Iniciar Jogo" → inicia a aventura
 
 Organização do Código
LEGENDARUM/
├── main.py           # Arquivo principal (interface e lógica inicial)
├── jogador.py        # Classe Jogador (atributos, vida, habilidades)
├── inimigo.py        # Classe Inimigo (dados dos adversários)
├── combate.py        # Função de combate (mecânica de luta)
├── historia.py       # História e introdução narrativa
├── fases.py          # Carrega e executa as fases do jogo
└── assets/
    ├── imagempersonagem.png
    ├── imagemmulher.png
    └── fundos / (opcional)
 
 Como Executar o Jogo Localmente
Pré-requisitos:
 
Ter Python 3.10+ instalado.
 
Instalar as dependências com:
 
pip install pillow
 
Rodando o jogo:
 
Baixe ou clone o projeto:
 
git clone https://github.com/seu-usuario/legendarum.git
 
 
Acesse a pasta:
 
cd legendarum
 
 
Execute o arquivo principal:
 
python main.py
 
 
Divirta-se!
 ----------------------------------------------------------------------------------------------------------------------------------------------------------------
Imagens e Personagens
 
O código exibe a imagem do personagem conforme a classe escolhida:
 
🧔 Homem: assets/imagempersonagem.png
 
👩 Mulher: assets/imagemmulher.png
 
Caso as imagens não existam, o console exibirá um aviso:
 
⚠️ Imagem não encontrada: assets/imagempersonagem.png
 
 Principais Funções
iniciar_jogo()
 
Responsável por:
 
Validar nome e classe escolhida;
 
Iniciar a história e carregar fases;
 
Controlar o fluxo de jogo (vitória, derrota e transição entre fases).
 
atualizar_personagem()
 
Atualiza a imagem do personagem quando o jogador troca de classe.
 
 Design e Experiência
 
O estilo da interface foi pensado para remeter a um ambiente medieval e mágico, com:
 
Fundo escuro (#1e1e2f);
 
Detalhes em dourado e verde (energia, vitória, poder);
 
Tipografia elegante (Georgia e Arial).
 
  Mensagens Interativas
 
O jogo utiliza messagebox do Tkinter para interações amigáveis:
 
Avisos: entrada de nome e seleção de classe
 
Progresso: fases concluídas e início das próximas
 
Resultados: vitória final ou game over
 
Essas mensagens mantêm o jogador imerso e guiado pela narrativa.
 
-----------------------------------------------------------------------------------------------------------------------------------------------------------------
 Conclusão
 
LEGENDARUM é mais que um simples RPG em Python —
é uma jornada que une história, tecnologia e emoção, mostrando como é possível criar experiências imersivas usando ferramentas simples como Tkinter.
 
💛 “Toda lenda começa com um nome… o seu.”


Criados por: Gustavo, Lyan e Maria Julia
 
