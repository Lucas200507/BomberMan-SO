import pygame
import math
from pygame.locals import *
from variaveis import *
from sys import exit

pygame.init()

tela = pygame.display.set_mode((larguraTela, alturaTela))
#Altera o nome da janela
pygame.display.set_caption('Bommm')
clock = pygame.time.Clock()
#MUSICAS
pygame.mixer.music.set_volume(0.35)
musica_telaInicial = pygame.mixer.music.load('musica_telaInicial.mp3')
# tocar a musica repetidamente
pygame.mixer.music.play(-1)

# NAVEGAÇAO DE TELAS##############################
#Classe para a criação das telas
#classe para controle de alteração entre telas
# atribui como parãmetro o objeto cena para que todos os objetos tenham acesso ás suas funções
class cenas:
    def __init__(self, tela):
        self.tela_atual = tela

    def obter_telaAtual(self):
        return self.tela_atual
    
    def Alterar_tela(self, tela):
        self.tela_atual = tela    

class construtor:
    # Indicação dos parâmetros para a criação das telas
    def __init__(self, display, cor, objeto_cena):
        self.tela = display        
        self.cor = cor
        self.cena = objeto_cena
    def run(self):
        self.tela.fill(self.cor)

# CRIAÇÃO DA TELA INICIAL    
class telaInicial:
    # Método construtor indica onde será apresentado
    def __init__(self, display, objeto_cena):
        self.tela = display
        self.cena = objeto_cena
        #Logo do jogo (tela Inicial)
        self.logo = pygame.image.load('logoBao.png')
        self.DimensoesLogo = self.logo.get_rect() 
        print(self.DimensoesLogo)
        #rect(0, 0, 5000, 1272)
        # DimensõesLogo[0] = posX; DimensõesLogo[1] = posY; DimensõesLogo[2] = largura; DimensõesLogo[3] = altura
        self.larguraLogo = self.DimensoesLogo[2]# 512
        self.alturaLogo = self.DimensoesLogo[3]# 252
        self.posXLogo = larguraTela/2  # colocar no meio do eixo x
        self.posYLogo =  200 + self.alturaLogo / 2 # colocar no alto do eixo y    
         # ANIMACAO LOGO        
        self.angulo = 0
        self.direcao_rotacao = 1 # 1 para direita, -1 para a esquerdaF
        self.velocidade_rotacao = 0.05
        self.amplitude_rotacao = 5
        self.frequencia_rotacao = 0.05
        # Texto Press Enter
        self.fontePress = pygame.font.SysFont('Arial', 50, True, False)
        self.textoPress = f'Pressione Enter para Iniciar'
        self.FormatacaoPress = self.fontePress.render(self.textoPress, False, (0,0,0))
        self.DimensoesPress = self.FormatacaoPress.get_rect()
        # print(self.DimensoesPress)
        self.larguraPress = self.DimensoesPress[2]
        # colocando no meio da tela
        self.posXPress = larguraTela/2 - self.larguraPress/2
        self.posYPress = 600
        
        
    def run(self):        
        self.tela.fill(BRANCO)        
        # Atualiza o ângulo de rotação
        self.angulo += self.velocidade_rotacao * self.direcao_rotacao
        # Inverte a direção se atingir os limites da amplitude
        if self.angulo > self.amplitude_rotacao:
            self.angulo = self.amplitude_rotacao
            self.direcao_rotacao = -1
        elif self.angulo < -self.amplitude_rotacao:
            self.angulo = -self.amplitude_rotacao
            self.direcao_rotacao = 1

        #rotacione a imagem
        logo_rotacionada = pygame.transform.rotate(self.logo, self.angulo)
        rect_rotacionado = logo_rotacionada.get_rect(center=(self.posXLogo,self.posYLogo))
        self.tela.blit(logo_rotacionada, rect_rotacionado)
        self.tela.blit(self.FormatacaoPress, (self.posXPress, self.posYPress))        
                                          
        for event in pygame.event.get():
            if event.type == QUIT:
                    pygame.quit()
                    exit()
            # verifica se a tecla foi clicada       
            if event.type == pygame.KEYDOWN:
                #verifica se a tecla clicada é o enter
                if event.key == pygame.K_RETURN:
                        barulho_click = pygame.mixer.Sound('sound_click.wav')
                        barulho_click.set_volume(1) # entre 1 e 0
                        barulho_click.play()
                        self.cena.Alterar_tela('menu')
           
# INSTACIAR ******************************************
cena = cenas("telaInicial")
TelaInicial = telaInicial(tela, cena)
menu = construtor(tela, AZUL, cena)
tela1 = construtor(tela, ROXO, cena)
telaPontos = construtor(tela, VERMELHO, cena)

fases = {"telaInicial":TelaInicial, "menu":menu, "Pontuacões":telaPontos, "fase1":tela1}

# ********************************************************

# --- LOOP PRINCIPAL ---
while True:    
    clock.tick(FPS)
    # # Pintando a tela de Branco
    tela.fill(BRANCO)       
    # #Verifica se o usuário clicou em sair da tela
    for event in pygame.event.get():
        if event.type == QUIT: 
            pygame.quit()
            exit()
      
    # fases["telaInicial"].run()
    fases[cena.obter_telaAtual()].run() 
    # Atualiza o jogo a cada interação
    pygame.display.update()
    

    
