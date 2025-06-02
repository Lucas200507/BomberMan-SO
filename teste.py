import pygame
from pygame.locals import *
import random
import threading
import time
from sys import exit

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO = (25, 0, 0)
VERDE_ESCURO = (0, 100, 0)
cor_fundoFase = VERDE_ESCURO

#criando um semáforo que irá guardar o limite de bombas que pode ser colocado no mapa por vez
limite_bombas = threading.Semaphore(3)
grupo_bombas=[]

mapa1 = [
    [4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4],
    [4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4],
    [4, 1, 3, 1, 3, 1, 3, 1, 3, 2, 3, 2, 3, 1, 3, 2, 4],
    [4, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 2, 1, 1, 4],
    [4, 1, 3, 1, 3, 2, 3, 2, 3, 1, 3, 1, 3, 1, 3, 1, 4],
    [4, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4],
    [4, 2, 3, 1, 3, 2, 3, 1, 3, 1, 3, 1, 3, 1, 3, 2, 4],
    [4, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4],
    [4, 1, 3, 1, 3, 1, 3, 2, 3, 1, 3, 1, 3, 1, 3, 1, 4],
    [4, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 2, 1, 4],
    [4, 2, 3, 1, 3, 1, 3, 2, 3, 2, 3, 1, 3, 1, 3, 1, 4],
    [4, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 4],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
]

pygame.init()

# SPRITES TIJOLOS = 192 x 64
# TAMANHO DE CADA SPRITE = 64 x 64
#           --- TOGLEFT ---
# SPRITE[0] = 0*64 x 0 | SPRITE[1] = 1*6

FPS = 30
relogio = pygame.time.Clock()
pygame.mixer.music.set_volume(0.5)

largura = 1250
altura = 960

pygame.display.set_caption('TESTE')
tela = pygame.display.set_mode((largura, altura))

velocidade_player = 15
tamanho_bloco = 74
altura_player = 98
largura_player = 64
posXInicial = 78
posYInicial = 70
delay_framePlayer = 0.07


class Menu:
    def __init__(self, background, logo, texto, musica):
        self.cor_fundo = background
        self.texto = texto
        self.logo = pygame.transform.scale(pygame.image.load(logo), (500, 320))
        self.musica = musica
        self.musicaTocando = False

    def iniciarMusicaMenu(self):
        if not self.musicaTocando:
            pygame.mixer.music.load(self.musica)
            pygame.mixer.music.play(-1)
            self.musicaTocando = True

    def desenhar(self, tela):
        tela.fill(self.cor_fundo)
        fonteText = pygame.font.SysFont('Arial', 40)
        formatacao = fonteText.render(self.texto, False, PRETO)
        larguraText = formatacao.get_width()

        # Centraliza texto e logo
        tela.blit(self.logo, ((largura // 2 - 500 // 2), (altura // 2 - 320)))
        tela.blit(formatacao, ((largura // 2 - larguraText // 2), 600))

    def interacao(self, tecla):
        return tecla == pygame.K_r


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
                    self.blocos.append(Blocos(x * self.tamanho_bloco, y * self.tamanho_bloco, self.tamanho_bloco,
                                              "imagens/Bloco_indestrutivel.png"))
                elif valor == 2:
                    self.blocos.append(Blocos(x * self.tamanho_bloco, y * self.tamanho_bloco, self.tamanho_bloco,
                                              "imagens/tijolos.png"))
                elif valor == 4:
                    self.blocos.append(Blocos(x * self.tamanho_bloco, y * self.tamanho_bloco, self.tamanho_bloco,
                                              "imagens/Bloco_Indestrutivel2.png"))

    def desenhar(self, tela):
        for bloco in self.blocos:
            bloco.desenhar(tela)


class Player:
    def __init__(self, x, y, largura, altura, frame):        
        self.sprites = pygame.image.load(frame)
        self.player = pygame.Rect(x, y, largura, altura)    
        # PARA RECORTAR O FRAME PLAYER
        self.x_sprites = 0
        self.y_sprites = 0
                
        self.velocidade = velocidade_player
        self.metadePlayer = pygame.Rect(x, y + (altura // 2), largura - 5, altura // 2)

    def mover(self, teclas, blocos):
        mover_x, mover_y = 0, 0      
        self.delay = delay_framePlayer        
        if teclas[pygame.K_LEFT]:
            mover_x -= self.velocidade            
            self.x_sprites += 1
            self.y_sprites = 1
            if self.x_sprites > 6:
                self.x_sprites = 2 
        elif teclas[pygame.K_RIGHT]:
            mover_x = self.velocidade
            self.x_sprites += 1
            self.y_sprites = 0
            if self.x_sprites > 3:
                self.x_sprites = 0   
        if teclas[pygame.K_UP]:
            mover_y = -self.velocidade
            self.x_sprites += 1          
            if self.x_sprites > 7:
                self.y_sprites = 2 
                self.x_sprites = 0
            elif self.x_sprites > 3:                                               
                    self.y_sprites = 1
                    self.x_sprites = 7 
            else:
                self.y_sprites = 2        
        elif teclas[pygame.K_DOWN]:           
            mover_y = self.velocidade
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
        time.sleep(self.delay)
        self.player.x += mover_x
        self.atualizar_metadePlayer()
        if self.colidiu(blocos):
            self.player.x -= mover_x

        self.player.y += mover_y
        self.atualizar_metadePlayer()
        if self.colidiu(blocos):
            self.player.y -= mover_y

        self.atualizar_metadePlayer()

    def atualizar_metadePlayer(self):
        self.metadePlayer.x = self.player.x
        self.metadePlayer.y = self.player.y + (self.player.height // 2)

    def colidiu(self, blocos):
        return any(self.metadePlayer.colliderect(b.block) for b in blocos)

    def desenhar(self, tela):
         tela.blit(self.sprites, (self.player.topleft), (int(self.x_sprites*64), self.y_sprites*98, 64, 98))       

class Inimigo:
    def __init__(self, x, y, velocidade=0.1):
        self.x = x
        self.y = y
        self.velocidade = velocidade
        self.vivo = True
        self.tamanho = tamanho_bloco
        self.imagem = pygame.image.load('imagens/inimigo.png')
        self.imagem = pygame.transform.scale(self.imagem, (self.tamanho, self.tamanho))
        self.ultimo_movimento = pygame.time.get_ticks()
        self.intervalo_movimento = 500  

    def mover(self, mapa):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_movimento < self.intervalo_movimento:
            return  
        self.ultimo_movimento = agora

        direcoes = ['cima', 'baixo', 'esquerda', 'direita']
        random.shuffle(direcoes)
        for direcao in direcoes:
            if self.pode_mover(direcao, mapa):
                self._atualiza_posicao(direcao)
                break


    def pode_mover(self, direcao, mapa):
        nova_x, nova_y = self.x, self.y
        if direcao == 'cima':
            nova_y -= 1
        elif direcao == 'baixo':
            nova_y += 1
        elif direcao == 'esquerda':
            nova_x -= 1
        elif direcao == 'direita':
            nova_x += 1
        # Verifica limites
        if nova_y < 0 or nova_y >= len(mapa) or nova_x < 0 or nova_x >= len(mapa[0]):
            return False
        return mapa[nova_y][nova_x] == 1


    def _atualiza_posicao(self, direcao):
        if direcao == 'cima':
            self.y -= 1
        elif direcao == 'baixo':
            self.y += 1
        elif direcao == 'esquerda':
            self.x -= 1
        elif direcao == 'direita':
            self.x += 1

    def verificar_morte(self, explosoes):
        if (self.x, self.y) in explosoes:
            self.vivo = False

    def __repr__(self):
        return f"Inimigo(x={self.x}, y={self.y}, vivo={self.vivo})"

    def desenhar(self, tela):
        tela.blit(self.imagem, (self.x * self.tamanho, self.y * self.tamanho))
        
class Bomb:
    # Atribuindo imagens da bomba e explosões    
    bomb_img = pygame.image.load("imagens/bomba.png")
    bomb_img = pygame.transform.scale(bomb_img, (tamanho_bloco, tamanho_bloco)) 
    explosion_img = pygame.image.load("imagens/explosion.png")
    explosion_img = pygame.transform.scale(explosion_img, (tamanho_bloco, tamanho_bloco))
    
    def __init__(self, x, y, fase):                
        self.delay_bomba = 3
        self.posX_bomba = x
        self.posY_bomba = y
        self.fase = fase
        self.explosoes = []
#         teste
        self.blocos = []

        
    def explodir(self):                
        time.sleep(self.delay_bomba)
        self.explosoes.append((self.posX_bomba, self.posY_bomba))
        
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0,1)]:
            # imprimir a explosão na tela
            nx, ny = self.posX_bomba + dx, self.posY_bomba + dy           
            if 0 <= ny < len(self.fase.mapa_layout) and 0 <= nx < len(self.fase.mapa_layout[0]):
                # tentando quebrar os tijolos                             
                tile = self.fase.mapa_layout[ny][nx]
                if tile == 2:      
                    # Percorrer a array de blocos
                    for j in self.fase.mapa.blocos:
                        if j.block.x == nx * tamanho_bloco and j.block.y == ny * tamanho_bloco:
                            j.backgroundImg = pygame.transform.scale(pygame.image.load("imagens/sprites/tijolos_destruidos1.png"), (tamanho_bloco, tamanho_bloco))
                            # remove o bloco pela posição da explosão              
                            time.sleep(0.4)                    
                            j.backgroundImg = pygame.transform.scale(pygame.image.load("imagens/sprites/tijolos_destruidos2.png"), (tamanho_bloco, tamanho_bloco))
                            time.sleep(0.2) 
                            self.fase.mapa.blocos.remove(j) 
                    # self.fase.mapa.blocos = [i for i in self.fase.mapa.blocos if i.block.x != nx * tamanho_bloco or i.block.y != ny * tamanho_bloco]
                    self.fase.mapa_layout[ny][nx] = 1
                elif tile in (3, 4):
                    continue
                self.explosoes.append((nx, ny))
                
      
        # VERIFICAÇÃO DA COLISÃO        
        jogador_x = self.fase.player.player.x // tamanho_bloco
        jogador_y = (self.fase.player.player.y + altura_player // 2) // tamanho_bloco
        
        if (jogador_x, jogador_y) in self.explosoes:
            self.fase.player.player.x = posXInicial
            self.fase.player.player.y = posYInicial

        for inimigo in self.fase.inimigos:
            if (inimigo.x, inimigo.y) in self.explosoes:
                inimigo.vivo = False

        #após a explosão, liberamos o recurso do semáforo e permitimos que outra bomba seja colocada 
        limite_bombas.release() 
        time.sleep(0.5)
        self.fase.bombas.remove(self)  
                  
        

class Fases:
    def __init__(self, mapa, cor_fundo, musica):
        self.mapa_layout = mapa
        self.mapa = Mapa(self.mapa_layout, tamanho_bloco)
        self.player = Player(posXInicial, posYInicial, largura_player, altura_player, 'imagens/Sprites_player.png')
        self.musicaTocando = False
        self.musica = musica
        self.cor_fundo = cor_fundo
        self.inimigos = [
            Inimigo(5, 5),
            Inimigo(5, 7),
            Inimigo(10, 5),
        ]
        self.bombas = []
        
    def verificarColisaoEntrePlayerOuInimigos(self):
        for inimigo in self.inimigos:
            if inimigo.vivo and self.player.player.colliderect(pygame.Rect(inimigo.x * tamanho_bloco, inimigo.y * tamanho_bloco, tamanho_bloco, tamanho_bloco)):
                self.player.player.x = posXInicial
                self.player.player.y = posYInicial
                self.player.atualizar_metadePlayer()

    def colocar_bomba(self,grupo_bombas):
        grid_x = (self.player.player.x // tamanho_bloco) 
        grid_y = (self.player.player.y // tamanho_bloco) + 1
        if not any(b.posX_bomba == grid_x and b.posY_bomba == grid_y for b in self.bombas):
            #condição para adquirir um recurso do semáforo. Quando todos forem utilizados, o acquire com "blocking=False" retorna o False imediatamente para o IF, evitando que o jogo fique esperando uma nova vaga surgir(o que faria o jogo travar)
            if limite_bombas.acquire(blocking=False):
                bomba = Bomb(grid_x, grid_y, self)
                self.bombas.append(bomba) 
                
                #ao ativar a bomba, a thread é criada para aquela bomba
                thBomba=threading.Thread(target=bomba.explodir)
                #guardando aqui as bomba criada
                grupo_bombas.append(bomba)
                thBomba.start()
                 
    def atualizar(self, teclas):
        self.player.mover(teclas, self.mapa.blocos)
        for inimigo in self.inimigos:
            if inimigo.vivo:
                inimigo.mover(self.mapa_layout)
        self.verificarColisaoEntrePlayerOuInimigos()
        if teclas[pygame.K_SPACE]:
           self.colocar_bomba(grupo_bombas)
                
    def iniciarMusicaFase(self):
        if not self.musicaTocando:
            pygame.mixer.music.load(self.musica)
            pygame.mixer.music.play(-1)
            self.musicaTocando = True
            
    def desenhar(self, tela):
        tela.fill(self.cor_fundo)
        self.mapa.desenhar(tela)
        self.player.desenhar(tela)
        
        for bomba in self.bombas:
            tela.blit(Bomb.bomb_img, (bomba.posX_bomba * tamanho_bloco, bomba.posY_bomba * tamanho_bloco))
            for ex, ey in bomba.explosoes:
                tela.blit(Bomb.explosion_img, (ex * tamanho_bloco, ey * tamanho_bloco))
        
        for inimigo in self.inimigos:
            if inimigo.vivo:
                inimigo.desenhar(tela)
                


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
             pygame.mixer.music.play(-1)
             menuMusicaTocando = True
    elif estado == "jogo":        
        menuMusicaTocando = False
        fase1.atualizar(teclas)
        fase1.desenhar(tela)
        fase1.iniciarMusicaFase()
        
    relogio.tick(FPS)    
    pygame.display.flip()
        
pygame.quit()      