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
delay_framePlayer = 100
delay_morte_player = 150
delay_morte_inimigo = 200
delay_frameInimigo = 0.06


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
    def __init__(self, x, y, largura, altura, frame, vivo):        
        self.sprites = pygame.image.load(frame)        
        self.spritesMorte = pygame.image.load('imagens/sprites/morte_player.png')
        self.spritesMorte = pygame.transform.scale(self.spritesMorte, (512, 98))
        self.player = pygame.Rect(x, y, largura, altura)    
        # PARA RECORTAR O FRAME PLAYER
        self.x_sprites = 0
        self.y_sprites = 0
        self.vivo = vivo      
        # PARA ANIMAR MORTE DO PLAYER
        self.ultimo_frame_morte = 0
        self.intervalo_morte = delay_morte_player
        self.morte_frame = 0
        self.tempo_morte = 0 
        self.velocidade = velocidade_player
        self.metadePlayer = pygame.Rect(x, y + (altura // 2), largura - 5, altura // 2)
        # PARA DEIXAR A ANIMAÇÃO MAIS FLUÍDA
        self.frame_atual = 0
        self.tempo_ultimo_frame = pygame.time.get_ticks()
        self.intervalo_animacao = delay_framePlayer # em milissegundos
        
    def atualizar_animacao(self):
        agora = pygame.time.get_ticks()
        if agora - self.tempo_ultimo_frame > self.intervalo_animacao:
            self.x_sprites += 1
            self.tempo_ultimo_frame = agora
        
    def mover(self, teclas, blocos, fase):
        mover_x, mover_y = 0, 0      
               
        if self.vivo:                            
            if teclas[pygame.K_LEFT]:
                mover_x -= self.velocidade            
                self.atualizar_animacao()
                self.y_sprites = 1
                if self.x_sprites > 6:
                    self.x_sprites = 2 
            elif teclas[pygame.K_RIGHT]:
                mover_x = self.velocidade
                self.atualizar_animacao()
                self.y_sprites = 0
                if self.x_sprites > 3:
                    self.x_sprites = 0   
            if teclas[pygame.K_UP]:
                mover_y = -self.velocidade
                self.atualizar_animacao()        
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
                self.atualizar_animacao()    
                if self.x_sprites < 7 and self.x_sprites > 4:
                    self.y_sprites = 0  
                else:     
                    if self.x_sprites > 6:
                        self.x_sprites = 0                           
                        self.y_sprites = 1
                    if self.x_sprites > 1:
                        self.x_sprites = 5
                        self.y_sprites = 0  
        
            self.player.x += mover_x
            self.atualizar_metadePlayer()        
            if self.colidiu(blocos, fase.bombas):
                self.player.x -= mover_x

            self.player.y += mover_y
            self.atualizar_metadePlayer()
            if self.colidiu(blocos, fase.bombas):
                self.player.y -= mover_y

            self.atualizar_metadePlayer()
        else:
            self.player.x -= mover_x
            self.player.y -= mover_y

    def atualizar_metadePlayer(self):
        self.metadePlayer.x = self.player.x
        self.metadePlayer.y = self.player.y + (self.player.height // 2)

    def colidiu(self, blocos, bombas=[]):
        for b in blocos:
            if self.metadePlayer.colliderect(b.block):
                return True
        for bom in bombas:
            if not bom.atravessavel and self.metadePlayer.colliderect(bom.pegar_dims()):
                return True
        return False
        #return any(self.metadePlayer.colliderect(b.block) for b in blocos)

    def desenhar(self, tela):
        if self.vivo:
         tela.blit(self.sprites, (self.player.topleft), (int(self.x_sprites*64), self.y_sprites*98, 64, 98))       
        else:
            agora = pygame.time.get_ticks()
            if self.morte_frame < 6:                 
                # SÓ MUDA O FRAME SE PASSOU O INTERVALO
                if agora - self.ultimo_frame_morte > self.intervalo_morte:
                    self.ultimo_frame_morte = agora               
                    tela.blit(self.spritesMorte, self.player.topleft, (int(self.morte_frame*64), 0, 64, 98))        
                    self.morte_frame += 1
                else:
                   tela.blit(self.spritesMorte, self.player.topleft, (int(self.morte_frame*64), 0, 64, 98))   
            else:     
                self.vivo = True
                self.player.x = posXInicial
                self.player.y = posYInicial
                tela.blit(self.sprites, (self.player.topleft), (int(self.x_sprites*64), self.y_sprites*98, 64, 98)) 
                self.morte_frame = 0

class Inimigo:
    def __init__(self, x, y, velocidade=0.1):
        self.x = x
        self.y = y
        self.velocidade = velocidade
        self.vivo = True
        self.tamanho = tamanho_bloco
        self.spritesInimigo = pygame.image.load('imagens/sprites/balao.png') # 64 x 64
        self.inimigo = pygame.Rect(self.x, self.y, tamanho_bloco, tamanho_bloco)
        self.posX_sprites = 0
        self.posY_sprites = 0
        # PARA ANIMAR A MORTE DO INIMIGO
        self.ultimo_frame_morte = 0
        self.ultimo_movimento = pygame.time.get_ticks()
        self.morte_frame = 6
        self.tempo_morte = 0
        self.intervalo_morte = delay_morte_inimigo
        # PARA DEIXAR A ANIMAÇÃO MAIS FLUÍDA
        self.frame_atual = 0
        self.intervalo_movimento = 500  

    def mover(self, mapa, fase):        
            agora = pygame.time.get_ticks()
            if agora - self.ultimo_movimento < self.intervalo_movimento:
                return  
            self.ultimo_movimento = agora

            direcoes = ['cima', 'baixo', 'esquerda', 'direita']
            random.shuffle(direcoes)
            for direcao in direcoes:
                if self.pode_mover(direcao, mapa, fase):
                    self._atualiza_posicao(direcao)
                    break


    def pode_mover(self, direcao, mapa, fase):
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
        for bomba in fase.bombas:
            if (nova_x, nova_y) == (bomba.posX_bomba, bomba.posY_bomba):
                return False
        return mapa[nova_y][nova_x] == 1

    def atualizar_animacao(self):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_movimento > self.intervalo_movimento:
            self.posX_sprites += 1
            self.ultimo_movimento = agora

    def _atualiza_posicao(self, direcao):        
        if direcao == 'cima':
            self.y -= 1
            self.atualizar_animacao()
            if self.posX_sprites > 2:
                self.posX_sprites = 0 
        elif direcao == 'baixo':
            self.y += 1
            self.atualizar_animacao()
            self.posX_sprites = 3
            if self.posX_sprites > 5:
                self.posX_sprites = 3            
        elif direcao == 'esquerda':
            self.x -= 1
            self.atualizar_animacao()
            self.posX_sprites = 3
            if self.posX_sprites > 5:
                self.posX_sprites = 3            
        elif direcao == 'direita':
            self.x += 1             
            self.atualizar_animacao()
            if self.posX_sprites > 2:
                self.posX_sprites = 0   
                
                            

    def verificar_morte(self, explosoes):        
        if (self.x, self.y) in explosoes:            
            self.x += 0
            self.y += 0                
            self.vivo = False            

    def __repr__(self):
        return f"Inimigo(x={self.x}, y={self.y}, vivo={self.vivo})"

    def desenhar(self, tela):
        if self.vivo:        
            tela.blit(self.spritesInimigo, (self.x * self.tamanho, self.y * self.tamanho), (int(self.posX_sprites*64), self.posY_sprites, 64, 64))
        else:
            agora = pygame.time.get_ticks()  
            if self.morte_frame < 10:
                if agora - self.ultimo_frame_morte > self.intervalo_morte:                    
                    self.ultimo_frame_morte = agora       
                    tela.blit(self.spritesInimigo, (self.morte_frame * self.tamanho, 0), (int(self.posX_sprites*64), self.posY_sprites, 64, 64))
                    self.morte_frame += 1
                else:
                    tela.blit(self.spritesInimigo, (self.morte_frame * self.tamanho, 0), (int(self.posX_sprites*64), self.posY_sprites, 64, 64))
            else:
                self.morte_frame = 0
        
        
class Bomb:
    # Atribuindo imagens da bomba e explosões    
    bomb_img = pygame.image.load("imagens/bomba.png")
    bomb_img = pygame.transform.scale(bomb_img, (tamanho_bloco, tamanho_bloco)) 
    # sprites explosão 48 x 44.6
    explosion_img = pygame.image.load("imagens/explosion.png")
    explosion_img = pygame.transform.scale(explosion_img, (tamanho_bloco, tamanho_bloco))
    
    def __init__(self, x, y, fase):                
        self.delay_bomba = 2
        self.posX_bomba = x
        self.posY_bomba = y
        self.fase = fase
        self.explosoes = []
        self.atravessavel = True
#         teste
        self.blocos = []
        
    # Para o inimigo e o player não passam pela bomba antes de explodir
    def pegar_dims(self):
        return pygame.Rect(self.posX_bomba * tamanho_bloco, self.posY_bomba * tamanho_bloco, tamanho_bloco, tamanho_bloco)
            
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
                            time.sleep(0.3)                    
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
        
        # MORTE DO PLAYER E INIMIGO PELAS EXPLOSÕES        
        if (jogador_x, jogador_y) in self.explosoes:
            self.fase.player.vivo = False         

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
        self.player = Player(posXInicial, posYInicial, largura_player, altura_player, 'imagens/Sprites_player.png', True)
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
            if inimigo.vivo and self.player.player.colliderect(
                pygame.Rect(inimigo.x * tamanho_bloco, inimigo.y * tamanho_bloco, tamanho_bloco, tamanho_bloco)
            ):
                # O QUE ACONTECE QUANDO O PLAYER COLIDE COM O INIMIGO:
                self.player.vivo = False
               

    def colocar_bomba(self,grupo_bombas):
        if self.player.vivo:
            grid_x = self.player.player.x // tamanho_bloco
            grid_y = (self.player.player.y + altura_player // 2) // tamanho_bloco
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
        self.player.mover(teclas, self.mapa.blocos, self)
        for inimigo in self.inimigos:
            if inimigo.vivo and self.player.vivo:
                inimigo.mover(self.mapa_layout, self)
        self.verificarColisaoEntrePlayerOuInimigos()
        if teclas[pygame.K_SPACE]:
           self.colocar_bomba(grupo_bombas)
        for bomba in self.bombas:
            if bomba.atravessavel: 
                player_grid_x = self.player.player.x // tamanho_bloco
                player_grid_y = (self.player.player.y + altura_player // 2) // tamanho_bloco
                if (player_grid_x, player_grid_y) != (bomba.posX_bomba, bomba.posY_bomba):                    
                    for bomba in self.bombas:
                        if bomba.atravessavel:
                            bomba_rect = bomba.pegar_dims()
                            if not self.player.metadePlayer.colliderect(bomba_rect):
                                bomba.atravessavel = False                         
                
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