import pygame
import sys

pygame.init()

LARGURA, ALTURA = 600, 600
TAMANHO_BLOCO = 50

tela= pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('teste mapa')

PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERDE = (0, 255, 0)
CINZA = (200, 200, 200)

mapa_jogo = [
 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
 [1, 0, 1, 2, 1, 1, 0, 1, 0, 1, 1, 1],
 [1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1],
 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
 [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
 [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
] 

def criar_mapa():
    for linha in range(len (mapa_jogo)):
      for coluna in range(len(mapa_jogo[linha])):

        y = linha * TAMANHO_BLOCO
        x = coluna * TAMANHO_BLOCO

        if mapa_jogo[linha][coluna] == 1:
         pygame.draw.rect(tela, PRETO(y, x, TAMANHO_BLOCO, TAMANHO_BLOCO)) # type: ignore
    

        elif mapa_jogo[linha][coluna] == 2: 
         pygame.draw.rect(tela, BRANCO(y, x, TAMANHO_BLOCO, TAMANHO_BLOCO)) 


        else:
         pygame.draw.rect(tela, CINZA(y, x, TAMANHO_BLOCO, TAMANHO_BLOCO))     # type: ignore
         pygame.draw.rect(tela, VERDE(y + 5, x + 5, TAMANHO_BLOCO - 10, TAMANHO_BLOCO - 10))     # type: ignore
    
clock = pygame.time.Clock()

while True:

  for evento in pygame.event.get():
    if evento.type == pygame.QUIT:
      pygame.quit()
    sys.exit()

tela.fill(BRANCO)

criar_mapa()
pygame.display.flip()
clock.tick(30)

    