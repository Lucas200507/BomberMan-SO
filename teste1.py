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
        self.clock = pygame.time.Clock()
        self.clock.tick(FPSfases)
                       
    def mostrarFase(self):            
        tela.fill(self.background)
        
    def criar_mapa(self):             
        linhas = len(mapa_jogo) # todos os vetores, 13 
        colunas = len(mapa_jogo[0]) # quantidades de elementos de cada vetor, 17
        
        largura_mapa = colunas * TAMANHO_BLOCO
        altura_mapa = linhas * TAMANHO_BLOCO
        # centralizando x e y
        offset_x = (larguraTela - largura_mapa) // 2 
        offset_y = (alturaTela - altura_mapa) // 2
        
        # 3 == BLOCO INDESTRUTÍVEL    
        # 1 == NULL
        # 2 == MADEIRA (DESTRUTÍVEL)
        for linha in range(linhas):            
            for coluna in range(colunas):
                y = linha * TAMANHO_BLOCO + offset_y
                x = coluna * TAMANHO_BLOCO + offset_x
                # caso a posição da matriz seja 1, pinte de preto sem bordas
                if mapa_jogo[linha][coluna] == 1:
                    pygame.draw.rect(tela, VERDE_ESCURO, (x, y, TAMANHO_BLOCO, TAMANHO_BLOCO))
                # caso a posição da matriz seja 2, pinte de branco o bloco, sem bordas
                elif mapa_jogo[linha][coluna] == 2:
                    pygame.draw.rect(tela, BRANCO, (x, y, TAMANHO_BLOCO, TAMANHO_BLOCO))
                elif mapa_jogo[linha][coluna] == 3:
                    blocoIndestrutivel = [mapa_jogo[linha][coluna]]
                    # sobrepondo retangulos
                    pygame.draw.rect(tela, CINZA_ESCURO, (x, y, TAMANHO_BLOCO, TAMANHO_BLOCO)) # borda
                    pygame.draw.rect(tela, CINZA, (x + 5, y + 5, TAMANHO_BLOCO - 10, TAMANHO_BLOCO - 10)) # centro
class Blocos:
    def __init__(self):
        #verificando quantidades de blocos no mapa no total
        self.linhas = 221 
        self.colunas = 221
        self.tamanho = TAMANHO_BLOCO
                  

    def iniciarMusicaFase(self):
        if not self.musicaTocando:
            pygame.mixer.music.load(self.musica)
            pygame.mixer_music.play(-1)
            self.musicaTocando = True

    def gerarBordas(self, larguraBlocks, alturaBlocks):
        self.larguraBlocks = larguraBlocks
        self.alturaBlocks = alturaBlocks
        i = 1
        while i <= 4:
            if i == 1:
                pygame.draw.rect(tela, CINZA, (0, 0, larguraTela, self.alturaBlocks))
            if i == 2:
                pygame.draw.rect(tela, CINZA, (larguraTela - self.larguraBlocks, 0, self.larguraBlocks, alturaTela))
            if i == 3:
                pygame.draw.rect(tela, CINZA, (0, 0, self.larguraBlocks, alturaTela))
            if i == 4:
                pygame.draw.rect(tela, CINZA, (0, alturaTela - self.larguraBlocks, larguraTela, self.alturaBlocks))
            i = i + 1
            
      

class Menu:
    def __init__(self, musica, FPS):
        self.musica = musica
        self.fps = FPS
        self.clock = pygame.time.Clock()
        self.angulo = 0
        self.direcao_rotacao = 1
        self.velRotacaoLogo = 2
        self.amplitude_rotacaoLogo = 5

    def mostrarMenu(self):
        tela.fill(BRANCO)
        self.clock.tick(self.fps)
        self.logo = pygame.image.load(MenuLogo)
        self.logoRedimensionado = pygame.transform.scale(self.logo, tamanhoLogo)

        self.angulo += self.velRotacaoLogo * self.direcao_rotacao
        if self.angulo > self.amplitude_rotacaoLogo:
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

        self.fontPressR = pygame.font.SysFont(TPressR_FontFamily, TPressR_Syze, TPressR_Bold, TPressR_Italic)
        self.TextPressR = 'Pressione R para iniciar a fase'
        self.FormatacaoTextPressR = self.fontPressR.render(self.TextPressR, False, PRETO)
        self.DimensoesTextPressR = self.FormatacaoTextPressR.get_rect()
        self.PosX_TextPressR = (larguraTela // 2) - (self.DimensoesTextPressR[2] // 2)
        self.PosY_TextPressR = 700
        tela.blit(self.FormatacaoTextPressR, (self.PosX_TextPressR, self.PosY_TextPressR))

def lerEvento(eventos):
    for event in eventos:
        if event.type == KEYDOWN:
            if event.key == K_r:
                return True
    return False

class player:
    def __init__(self, largura, altura, frame):
        self.tamanhoPlayer = (largura, altura)
        self.framePlayer = frame
        self.posX = 500
        self.posY = 600

    def criarPlayer(self):
        self.playerImg = pygame.image.load(self.framePlayer)
        self.playerRedimensionado = pygame.transform.scale(self.playerImg, self.tamanhoPlayer)
        eventosMov = pygame.event.get()
        if not hasattr(self, 'posX'):
            self.posX = 500
            self.posY = 600

        # Movimentação do player
          # Define a velocidade do movimento
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            if self.posX.coliderect(blocoIndestrutivel):
                self.posX = 0
            self.posX -= velocidadePlayer
        if teclas[pygame.K_RIGHT]:
            self.posX += velocidadePlayer
        if teclas[pygame.K_UP]:
            self.posY -= velocidadePlayer
        if teclas[pygame.K_DOWN]:
            self.posY += velocidadePlayer
        tela.blit(self.playerRedimensionado, (self.posX, self.posY))

fase1 = Fases(VERDE_ESCURO, 1, 'musica_jogatina.mp3')
menu = Menu('musica_telaInicial.mp3', FPSmenu)
p1 = player(66, 66, 'player_teste.png')

while rodar:
    eventos = pygame.event.get()
    for event in eventos:
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            exit()
            rodar = False

    if Rodandomenu:        
        if not menuMusicaTocando:
            pygame.mixer.music.load(menu.musica)
            pygame.mixer_music.play(-1)
            menuMusicaTocando = True
        menu.mostrarMenu()
        if lerEvento(eventos):
            rodarFase1 = True
            Rodandomenu = False
            pygame.mixer.music.stop()
            menuMusicaTocando = False
            fase1.iniciarMusicaFase()  
               
    elif rodarFase1:                     
        fase1.mostrarFase()
        fase1.gerarBordas(65, 65)
        fase1.criar_mapa()
        p1.criarPlayer()
        

    pygame.display.update()
