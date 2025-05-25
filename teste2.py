import pygame
from pygame.locals import *
from sys import exit

PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO = (25, 0, 0)
VERDE_ESCURO = (0,100,0)
cor_fundoFase = VERDE_ESCURO

mapa1 = [
        [4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4],
        [4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4],
        [4, 1, 3, 1, 3, 1, 3, 1, 3, 2, 3, 2, 3, 1, 3, 2, 4],
        [4, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4],
        [4, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 4],
        [4, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4],
        [4, 1, 3, 1, 3, 2, 3, 1, 3, 1, 3, 1, 3, 1, 3, 2, 4],
        [4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4],
        [4, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 4],
        [4, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 4],
        [4, 2, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 4],
        [4, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4],       
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
]
pygame.init()

FPS = 60
relogio = pygame.time.Clock()
pygame.mixer.music.set_volume(0.5)

largura = 1123
altura = 861

pygame.display.set_caption('TESTE2')
tela = pygame.display.set_mode((largura, altura))


class Menu:
    def __init__(self, background, logo, texto, musica):
        self.cor_fundo = background        
        self.texto = texto
        self.logo = pygame.transform.scale(pygame.image.load(logo), (500, 320))
        self.musica = musica
        self.musicaMenu = False
        
     
    def iniciarMusicaMenu(self):
        if not self.musicaMenu:
            pygame.mixer.music.load(self.musica)
            pygame.mixer_music.play(-1)
            self.musicaTocando = True        
                    
    def desenhar(self, tela):
        tela.fill(self.cor_fundo)
        self.fonteText = pygame.font.SysFont('Arial', 40, False, False)
        self.Formatacao = self.fonteText.render(self.texto, False, PRETO)
        dimensText = self.Formatacao.get_rect()
        self.larguraText = dimensText[2]
        
        #colocar no meio da tela
        tela.blit(self.logo, ((largura // 2 - 500 // 2), (altura // 2 - 320)))
        tela.blit(self.Formatacao, ((largura // 2 - self.larguraText // 2), 600))
        
    def interacao(self, tecla):
        if tecla == pygame.K_r:
            return True
        return False
    
class Blocos:
    def __init__(self, x, y, tamanho, img):
        self.block = pygame.Rect(x, y, tamanho, tamanho)
        self.backgroundImg = pygame.transform.scale(pygame.image.load(img), (tamanho, tamanho))
        
    def desenhar(self, tela):
         tela.blit(self.backgroundImg, self.block.topleft)
         
class Mapa:
    def __init__(self, layout, tamanho_bloco):
        self.blocos = []
        self.tamanho_bloco = tamanho_bloco
        self.carregar_layout(layout)

    def carregar_layout(self, layout):
        for y, linha in enumerate(layout):
            for x, valor in enumerate(linha):
                if valor == 3:
                    self.blocos.append(Blocos(x * self.tamanho_bloco, y * self.tamanho_bloco, self.tamanho_bloco, "imagens/Bloco_indestrutivel.png"))
                elif valor == 2:
                    self.blocos.append(Blocos(x * self.tamanho_bloco, y * self.tamanho_bloco, self.tamanho_bloco, "imagens/tijolos.png")) 
                elif valor == 4:
                    self.blocos.append(Blocos(x * self.tamanho_bloco, y * self.tamanho_bloco, self.tamanho_bloco, "imagens/Bloco_Indestrutivel2.png")) 

    def desenhar(self, tela):
        for bloco in self.blocos:
            bloco.desenhar(tela)
                            
            
class Player:
    def __init__(self, x, y, tamanho, frame):
        self.player = pygame.Rect(x, y, tamanho, tamanho)
         # Carrega e redimensiona a imagem
        self.playerImg = pygame.image.load(frame)
        self.playerRedimensionado = pygame.transform.scale(self.playerImg, (tamanho, tamanho))
        self.velocidade = 5
        
        
    def mover(self, teclas, blocos):               
        mover_x, mover_y = 0, 0
        if teclas[pygame.K_LEFT]:
            mover_x = -self.velocidade
        elif teclas[pygame.K_RIGHT]:
            mover_x = self.velocidade
        elif teclas[pygame.K_UP]:
            mover_y = -self.velocidade
        elif teclas[pygame.K_DOWN]:
            mover_y = self.velocidade
            
        self.player.x += mover_x
        if self.colidiu(blocos): self.player.x -= mover_x
        
        self.player.y += mover_y
        if self.colidiu(blocos): self.player.y -= mover_y
        
    def colidiu(self, blocos):
        return any(self.player.colliderect(b.block) for b in blocos)
    
    def desenhar(self, tela):
        tela.blit(self.playerRedimensionado, self.player.topleft)
         
class Fases:
    def __init__(self, mapa, cor_fundo, musica):
        tela.fill(cor_fundo)
        self.mapa_layout = mapa
        self.mapa = Mapa(self.mapa_layout, 66)
        self.player = Player(70, 70, 55, 'imagens/robo_parado1.png')
        self.musicaTocando = False
        self.musica = musica
        
    def atualizar(self, teclas):
        self.player.mover(teclas, self.mapa.blocos)
    
    def iniciarMusicaFase(self):
        if not self.musicaTocando:
            pygame.mixer.music.load(self.musica)
            pygame.mixer_music.play(-1)
            self.musicaTocando = True
            
    def desenhar(self, tela):
        tela.fill(cor_fundoFase) 
        self.mapa.desenhar(tela)
        self.player.desenhar(tela)        
        
# ===================================================
menu = Menu(BRANCO, 'imagens/logoBao.png', 'Clique ENTER para iniciar o jogo', 'sons/musica_telaInicial.mp3')
fase1 = Fases(mapa1, cor_fundoFase, 'sons/musica_jogatina.mp3')

estado = "menu"
menuMusicaTocando = False


rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
                
        if evento.type == pygame.KEYDOWN and estado == "menu":
            if evento.key == pygame.K_RETURN:
                estado = "jogo"
                pygame.mixer.music.stop()
            
            
    teclas = pygame.key.get_pressed()                
    if estado == "menu":
        menu.desenhar(tela)        
        if not menuMusicaTocando:
             pygame.mixer.music.load(menu.musica)
             pygame.mixer_music.play(-1)
             menuMusicaTocando = True
    elif estado == "jogo":        
        menuMusicaTocando = False
        fase1.atualizar(teclas)
        fase1.desenhar(tela)
        fase1.iniciarMusicaFase()
        
    relogio.tick(FPS)    
    pygame.display.flip()
        
pygame.quit()        
        