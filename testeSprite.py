import pygame
from pygame.locals import *
from sys import exit

# Constantes
tamanho_player = 60
tamanho_tela = 800
velocidade_player = 15  # Use valor inteiro para movimento em pixels


# Inicialização
pygame.init()
tela = pygame.display.set_mode((tamanho_tela, tamanho_tela))
pygame.display.set_caption('Teste Sprites')
relogio = pygame.time.Clock()

class Player:
    def __init__(self, sprites):
        self.sprites = pygame.image.load(sprites)        
        self.player = self.sprites.get_rect()
        self.posX_player = 0
        self.posY_player = 0        
        self.velocidade = velocidade_player
        self.x_sprites = 0
        self.y_sprites = 0
        

    def mover(self, teclas):
        # x_sprites = largura do sprites_player / y_sprites altura do sprite_player
#                        x     -      y
        # direita (64*0 - 64*5, 98*0 - 98)
        # esquerda (64*2 - 64*7, 98*1 - 98*2)
        # cima (64 * 7) - (64-0 - 3) - 98*1 - 98*2
        # baixo ((64*0 - 64*1) - (64*5 - 64*6)) - (98*0 - 98*1)
        # ou seja, para direita o inidice começa com 0*64 e vai até 5*64
                        
                   
        if teclas[pygame.K_RIGHT]:
            self.posX_player += self.velocidade 
            self.x_sprites += 1
            self.y_sprites = 0
            if self.x_sprites > 5:
                self.x_sprites = 0           
        if teclas[pygame.K_LEFT]:            
            self.posX_player -= self.velocidade            
            self.x_sprites += 1
            self.y_sprites = 1
            if self.x_sprites > 6:
                self.x_sprites = 2                              
        if teclas[pygame.K_UP]:
            self.posY_player -= self.velocidade            
            self.x_sprites += 1          
            if self.x_sprites > 7:
                self.y_sprites = 2 
                self.x_sprites = 0
            elif self.x_sprites > 3:                                               
                    self.y_sprites = 1
                    self.x_sprites = 7 
            else:
                self.y_sprites = 2               
        if teclas[pygame.K_DOWN]:
            self.posY_player += self.velocidade
            self.x_sprites += 1          
            if self.x_sprites < 7 and self.x_sprites > 4:
                self.y_sprites = 0  
            else:     
                if self.x_sprites > 6:
                    self.x_sprites = 0                           
                    self.y_sprites = 1
                if self.x_sprites > 1:
                    self.x_sprites = 5
                    self.y_sprites = 0  
                                    
     
    def desenhar(self, tela):
        tela.blit(self.sprites, (self.posX_player, self.posY_player), (int(self.x_sprites*64), self.y_sprites*98, 64, 98))

#        self.player.topleft = (self.posX_player, self.posY_player)

# Instanciando o player
p1 = Player('imagens/Sprites_player.png')

# Loop principal
rodar = True
while rodar:
    tela.fill((0, 0, 0))
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodar = False
            pygame.quit()
            exit()

    teclas = pygame.key.get_pressed()
    p1.mover(teclas)
    p1.desenhar(tela)

    pygame.display.flip()
    relogio.tick(30)