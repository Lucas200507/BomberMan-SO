import pygame
from pygame.locals import *
from variaveis import *
from sys import exit

pygame.init()
pygame.display.set_caption('BomberMan')

tela = pygame.display.set_mode((larguraTela, alturaTela))
pygame.mixer.music.set_volume(0.5)

# musica_fundo = pygame.mixer.music.load('musica_telaInicial.mp3')
# pygame.mixer_music.play(-1)

# VARIAVEIS PARA CONTROLE DE LOOPS
rodar = True
rodarFase1 = False
Rodandomenu = True
menuMusicaTocando = False

class Fases:
    def __init__(self, background, dificuldade, musica):
        self.background = background
        self.dificuldadeFase = dificuldade
        self.musica = musica  
        self.musicaTocando = False              

    def mostrarFase(self):
        tela.fill(self.background)                
       
    def iniciarMusicaFase(self):
        if not self.musicaTocando:
             pygame.mixer.music.load(self.musica)
             pygame.mixer_music.play(-1)
             self.musicaTocando = True
        
    def gerarBordas(self, larguraBlocks, alturaBlocks):
        self.larguraBlocks = larguraBlocks
        self.alturaBlocks = alturaBlocks                               
        i = 1
        # gerar as bordas                 
        while i <= 4: 
            # borda top
            if i == 1:
                x = 0
                y = 0
                pygame.draw.rect(tela, CINZA, (x, y, larguraTela, self.alturaBlocks))
            # borda right
            if i == 2:
                x = larguraTela - self.larguraBlocks
                y = 0
                pygame.draw.rect(tela, CINZA, (x, y, self.larguraBlocks, alturaTela))
            # borda left                
            if i == 3:
                x = 0
                y = 0
                pygame.draw.rect(tela, CINZA, (x, y, self.larguraBlocks, alturaTela))
            # borda bottom                
            if i == 4:
                x = 0
                y = alturaTela - self.larguraBlocks
                pygame.draw.rect(tela, CINZA, (x, y, larguraTela, self.alturaBlocks))
            i = i + 1   
            

            

class Menu:
    def __init__(self, musica, FPS):
        self.musica = musica
        self.fps = FPS
        
        self.clock = pygame.time.Clock()
        
        # variaveis para rotacionar a logo
        self.angulo = 0
        self.direcao_rotacao = 1  # 1 para direita, -1 para a esquerda
        self.velRotacaoLogo = 2
        self.amplitude_rotacaoLogo = 5
        self.frequencia_rotacaoLogo = 0.05
        
    def mostrarMenu(self):
        tela.fill(BRANCO)
        self.clock.tick(self.fps)
        #Colocando a logo na tela
        self.logo = pygame.image.load(MenuLogo)
        self.logoRedimensionado = pygame.transform.scale(self.logo, tamanhoLogo)                                                       
        
        #Rotacionar a Logo na tela        
        self.angulo += self.velRotacaoLogo * self.direcao_rotacao

        if(self.angulo > self.amplitude_rotacaoLogo):
             self.angulo = self.amplitude_rotacaoLogo
             self.direcao_rotacao = -1
        elif self.angulo < -self.amplitude_rotacaoLogo:
             self.angulo = -self.amplitude_rotacaoLogo
             self.direcao_rotacao = 1
                          
        self.logoRotacionado = pygame.transform.rotate(self.logoRedimensionado, self.angulo)             
        self.Dimens_logoRotacionado = self.logoRotacionado.get_rect()
        largura_logoRotacionado = self.Dimens_logoRotacionado[2]
        altura_logoRotacionado = self.Dimens_logoRotacionado[3]   
        self.posX_logoRotacionado = ((larguraTela // 2) - (largura_logoRotacionado // 2))
        self.posY_logoRotacionado = ((alturaTela // 2) - (altura_logoRotacionado // 2) - 100)                     
        tela.blit(self.logoRotacionado, (self.posX_logoRotacionado, self.posY_logoRotacionado))
        
        
    
        # CRIANDO O TEXTO NA TELA
        self.fontPressR = pygame.font.SysFont(TPressR_FontFamily, TPressR_Syze, TPressR_Bold, TPressR_Italic)
        self.TextPressR = 'Pressione R para iniciar a fase'
        self.FormatacaoTextPressR = self.fontPressR.render(self.TextPressR, False, PRETO)
        self.DimensoesTextPressR = self.FormatacaoTextPressR.get_rect()
        self.larguraTextPressR = self.DimensoesTextPressR[2]
        self.alturaTextPressR = self.DimensoesTextPressR[3]
        self.PosX_TextPressR = (larguraTela // 2)  - (self.larguraTextPressR // 2)
        self.PosY_TextPressR = 700
        tela.blit(self.FormatacaoTextPressR, (self.PosX_TextPressR, self.PosY_TextPressR))                                                                       
                
def lerEvento(eventos):           
        for event in eventos:
            if event.type == KEYDOWN:
                if event.key == K_r:                    
                   return True                
        return  False

class player:
    def __init__(self, largura, altura, frame):
        self.tamanhoPlayer = (largura, altura)        
        self.framePlayer = frame
        
    def criarPlayer(self):       
        self.playerImg = pygame.image.load(self.framePlayer)
        self.playerRedimensionado = pygame.transform.scale(self.playerImg, self.tamanhoPlayer)
        # self.playerDimens = self.playerRedimensionado.get_rect()
        if not hasattr(self, 'posX'):
            self.posX = 500
            self.posY = 600

        # Movimentação do player
        velocidade = 0.5  # Define a velocidade do movimento
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            self.posX -= velocidade
        if teclas[pygame.K_RIGHT]:
            self.posX += velocidade
        if teclas[pygame.K_UP]:
            self.posY -= velocidade
        if teclas[pygame.K_DOWN]:
            self.posY += velocidade

        tela.blit(self.playerRedimensionado, (self.posX, self.posY))        
        
    

# 3333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333                
#instaciando
fase1 = Fases(VERDE_ESCURO, 1, 'musica_jogatina.mp3')     
menu = Menu('musica_telaInicial.mp3', FPSmenu)   
p1 = player(30, 30, 'player_teste.png')



# ############################################################################################################################
while rodar:
    eventos = pygame.event.get()
    for event in eventos:                
        if event.type == QUIT:
            pygame.quit()
            exit()
            rodar = False 
# SAI DO JOGO CASO CLIQUE ESC  
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
                rodar = False 
             
    if Rodandomenu:                                
        if not menuMusicaTocando:
            # Agora a musica irá rodar apenas uma vez, quando verificar que o menu está rodando
            pygame.mixer.music.load(menu.musica)
            pygame.mixer_music.play(-1) 
            menuMusicaTocando = True
        menu.mostrarMenu()  
            
                              
        if lerEvento(eventos):
                rodarFase1 = True
                Rodandomenu = False
                pygame.mixer.music.stop() # Pare a música do menu
                menuMusicaTocando = False # Resete a flag do menu                
                fase1.iniciarMusicaFase() # Inicie a música da fase

                
    elif rodarFase1:
        fase1.mostrarFase() 
        fase1.gerarBordas(30,30)
        p1.criarPlayer()
                 
                
    pygame.display.update()
    