import pygame
from pygame.locals import *
import random
import threading
import time
import datetime
from sys import exit
from variaveis import *

grupo_bombas=[]
pygame.init()

relogio = pygame.time.Clock() # ininiando o relógio
pygame.mixer.music.set_volume(0.5) # definindo o volume da música
pygame.display.set_caption('TESTE') # definindo o nome do título da janela
tela = pygame.display.set_mode((largura, altura)) # criando a tela principal, com largura e altura

#  Criando a tela Menu
class Menu:
    def __init__(self, background, logo, texto, musica):
        self.cor_fundo = background
        self.texto = texto
        self.logo = pygame.transform.scale(pygame.image.load(logo), (500, 320)) # rendenizanod o tamanho da logo
        self.musica = musica
        self.musicaTocando = False

    def iniciarMusicaMenu(self):
        if not self.musicaTocando:
            pygame.mixer.music.load(self.musica)
            pygame.mixer.music.play(-1) # declarando a musíca como um loop infinito
            self.musicaTocando = True

    #   Desenhando na tela principal 
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
                # array blocos recebendo de acordo com o valor da matriz do mapa
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
    def __init__(self, x, y, largura_player, altura_player, frame, vivo):        
        self.sprites = pygame.image.load(frame)        
        self.spritesMorte = pygame.image.load('imagens/sprites/morte_player.png')
        self.spritesMorte = pygame.transform.scale(self.spritesMorte, (512, 98))
        self.player = pygame.Rect(x, y, largura_player, altura_player)    
        # PARA RECORTAR O FRAME PLAYER
        self.x_sprites = 0
        self.y_sprites = 0
        self.vivo = vivo      
        # PARA ANIMAR MORTE DO PLAYER]        
        self.ultimo_frame_morte = 0
        self.intervalo_morte = delay_morte_player
        self.morte_frame = 0
        self.tempo_morte = 0 
        self.velocidade = velocidade_player
        self.metadePlayer = pygame.Rect(x, y + (altura_player // 2), largura_player - 10, altura_player // 2)
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
        # Para a movimentação e animação do               
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
            
            if not fase.porta.aberta:
              if self.metadePlayer.colliderect(fase.porta.portinha):
               self.player.x -= mover_x
               self.atualizar_metadePlayer()

            self.player.y += mover_y
            self.atualizar_metadePlayer()
            if self.colidiu(blocos, fase.bombas):
                self.player.y -= mover_y
            
            if not fase.porta.aberta:
             if self.metadePlayer.colliderect(fase.porta.portinha):
               self.player.y -= mover_y
               self.atualizar_metadePlayer()

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
                if vidas_player >= 1:
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
                    tela.blit(self.spritesInimigo, (self.x * self.tamanho, self.y * self.tamanho), (int(self.morte_frame * 64), 0, 64, 64))
                    self.morte_frame += 1
                else:
                    tela.blit(self.spritesInimigo, (self.x * self.tamanho, self.y * self.tamanho), (int(self.morte_frame * 64), 0, 64, 64))
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
        
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-2, 0), (2, 0), (0, -2), (0, 2)]:
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
            global vidas_player
            vidas_player -= 1 

        for inimigo in self.fase.inimigos:
            if (inimigo.x, inimigo.y) in self.explosoes:
                inimigo.vivo = False
                global pontos
                pontos += 50

        #após a explosão, liberamos o recurso do semáforo e permitimos que outra bomba seja colocada 
        self.fase.limite_bombas.release()
        # limite_bombas.release() 
        time.sleep(0.5)
        self.fase.bombas.remove(self)  

class Porta:
    def __init__(self, imagem, pos):
        self.imagem = pygame.image.load(imagem)
        self.pos = pos
        self.aberta = False
        self.portinha = pygame.Rect(self.pos[0], self.pos[1], tamanho_bloco, tamanho_bloco)
             
    def abrir(self, imagem_aberta):
        self.imagem = pygame.image.load(imagem_aberta)
        self.aberta = True
    
    def desenhar(self, tela):
        tela.blit(self.imagem, self.pos)                
        

class Fases:
    def __init__(self, mapa, cor_fundo, musica, qtd_bombas, qtd_inimigos, fase_atual, tempo_limite=120):
        self.fase_atual = fase_atual
        self.mapa_layout = mapa
        self.mapa = Mapa(self.mapa_layout, tamanho_bloco)
        self.player = Player(posXInicial, posYInicial, largura_player, altura_player, 'imagens/Sprites_player.png', True)
        self.musicaTocando = False
        self.musica = musica
        self.cor_fundo = cor_fundo
        self.inimigos = [
            Inimigo(5, 5),
            # Inimigo(5, 7),
            # Inimigo(10, 5),
        ]
        # tempo Partida
        self.tempo_limite = tempo_limite
        self.tempo_inicial = pygame.time.get_ticks() # identifica quanod a fase começou
        
        self.quantidade_bombas = qtd_bombas
        self.limite_bombas = threading.Semaphore(self.quantidade_bombas)
        self.quantidade_inimigos = qtd_inimigos
        Bomb
        self.bombas = []
        self.fimjogo = Fim_jogo
        self.porta = Porta("imagens/pcerta-1.png.png", (1110, 29)) 

        if self.todos_mortos():
         self.porta.abrir ("imagens/pcerta-2.png.png", (1110, 29))
        

    def todos_mortos(self):
        return all(not inimigo.vivo for inimigo in self.inimigos)    

    def verificarColisaoEntrePlayerOuInimigos(self):
        #usando if para ignorar o verificarColisão enquanto o player estiver morto, evitando a perda de vidas durante a animação de morte do player
        if self.player.vivo == False:
            return
        
        for inimigo in self.inimigos:
            if inimigo.vivo and self.player.player.colliderect(
                pygame.Rect(inimigo.x * tamanho_bloco, inimigo.y * tamanho_bloco, tamanho_bloco, tamanho_bloco)
            ):
                # O QUE ACONTECE QUANDO O PLAYER COLIDE COM O INIMIGO:
                self.player.vivo = False
                global vidas_player
                vidas_player -= 1 
                
               

    def colocar_bomba(self,grupo_bombas):                        
        if self.player.vivo:
            grid_x = self.player.player.x // tamanho_bloco
            grid_y = (self.player.player.y + altura_player // 2) // tamanho_bloco
            if not any(b.posX_bomba == grid_x and b.posY_bomba == grid_y for b in self.bombas):
                #condição para adquirir um recurso do semáforo. Quando todos forem utilizados, o acquire com "blocking=False" retorna o False imediatamente para o IF, evitando que o jogo fique esperando uma nova vaga surgir(o que faria o jogo travar)
                if self.limite_bombas.acquire(blocking=False):
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

        if self.todos_mortos() and not self.porta.aberta:
         self.porta.abrir("imagens/pcerta-2.png.png")

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
        if self.player.vivo:
            self.player.desenhar(tela)            
        
        for bomba in self.bombas:
            tela.blit(Bomb.bomb_img, (bomba.posX_bomba * tamanho_bloco, bomba.posY_bomba * tamanho_bloco))
            for ex, ey in bomba.explosoes:
                tela.blit(Bomb.explosion_img, (ex * tamanho_bloco, ey * tamanho_bloco))
        
        for inimigo in self.inimigos:
            if inimigo.vivo:
                inimigo.desenhar(tela)
            
        self.porta.desenhar(tela) 
        for inimigo in self.inimigos:
            if self.todos_mortos():
             self.porta.abrir("imagens/pcerta-2.png.png")
                
    def verificar_tempoRestante(self):
        tempo_atual = pygame.time.get_ticks()
        tempo_percorrido = (tempo_atual  - self.tempo_inicial) / 1000
        return max(0, self.tempo_limite - tempo_percorrido)            

class Telas:
    def __init__(self, tela):
        self.tela = tela

    def telaMorte(self):                                    
            self.tela.fill((0, 0, 0))  # tela preta
            fonte = pygame.font.SysFont('Arial', 80)
            texto = fonte.render('Você morreu!', True, VERMELHO)  # vermelho
            ret_texto = texto.get_rect(center=(self.tela.get_width()//2, self.tela.get_height()//2))
            self.tela.blit(texto, ret_texto)
            pygame.display.flip()
            pygame.time.delay(3000)  # pausa 3 segundos
            
    def telaAcabouTempo(self):                                    
            self.tela.fill((0, 0, 0))  # tela preta
            fonte = pygame.font.SysFont('Arial', 80)
            texto = fonte.render('Acabou o tempo!', True, AMARELO) 
            ret_texto = texto.get_rect(center=(self.tela.get_width()//2, self.tela.get_height()//2))
            self.tela.blit(texto, ret_texto)
            pygame.display.flip()
            pygame.time.delay(3000)  # pausa 3 segundos            
            

    def telaDerrota(self):
        fonte = pygame.font.SysFont('Arial', 80)
        texto = fonte.render('Você perdeu!', True, VERMELHO)
        self.tela.fill((0, 0, 0))
        pos_x = (self.tela.get_width() - texto.get_width()) // 2
        pos_y = (self.tela.get_height() - texto.get_height()) // 2
        self.tela.blit(texto, (pos_x, pos_y))
        pygame.display.flip()
        pygame.time.delay(3000)

    def telaDeLoading(self):
        self.tela.fill((0, 0, 0))
        fonte = pygame.font.SysFont('Arial', 50)
        texto = fonte.render('Carregando...', True, (255, 255, 255))
        pos_x = (self.tela.get_width() - texto.get_width()) // 2
        pos_y = (self.tela.get_height() - texto.get_height()) // 2
        self.tela.blit(texto, (pos_x, pos_y))
        pygame.display.flip()
        pygame.time.delay(3000)

    def telaContinuar(self):
        fonte = pygame.font.SysFont('Arial', 30)
        texto1 = fonte.render('Deseja continuar?', True, (255, 255, 255))
        texto2 = fonte.render('Pressione ENTER para continuar ou ESC para sair.', True, (255, 255, 255))

        while True:
            self.tela.fill((0, 0, 0))
            pos1_x = (self.tela.get_width() - texto1.get_width()) // 2
            pos1_y = self.tela.get_height() // 2 - 40
            pos2_x = (self.tela.get_width() - texto2.get_width()) // 2
            pos2_y = self.tela.get_height() // 2 + 10

            self.tela.blit(texto1, (pos1_x, pos1_y))
            self.tela.blit(texto2, (pos2_x, pos2_y))
            pygame.display.flip()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN:
                        return True
                    elif evento.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()

class Fim_jogo:
    def __init__(self,  lframes, fpos, inframes,  musica):
        self.cor_fundo = PRETO
        self.lframes = [pygame.image.load(arframes) for arframes in lframes]
        self.fpos = fpos
        self.inframes = inframes
        self.musica = musica
        self.musicaBomba = False
        self.cframe = 0 
        self.ftempo = 0
        

    def iniciarMusicaMano(self):
        if not self.musicaBomba:
            pygame.mixer.music.load(self.musica)
            pygame.mixer.music.play(-1)
            self.musicaBomba = True
            
    def atual(self):
        self.ftempo += 1
        if self.ftempo >= self.inframes:
            self.cframe = (self.cframe + 1) % len(self.lframes)
            self.ftempo = 0

    def desenhar(self, tela):
        tela.fill(self.cor_fundo)
        tela.blit(self.lframes[self.cframe], self.fpos)
       
frame_bacana = [
            "imagens/fr1-1.png.png",
            "imagens/fr1-2.png.png",
            "imagens/fr1-3.png.png",
            "imagens/fr1-4.png.png",
            "imagens/fr1-5.png.png",
            "imagens/fr1-6.png.png",
            "imagens/fr1-7.png.png"
        ]

# ===================================================
menu = Menu(BRANCO, 'imagens/logoBao.png', 'Clique ENTER para iniciar o jogo', 'sons/musica_telaInicial.mp3')
fase = Fases(mapa1, cor_fundoFase, 'sons/musica_jogatina.mp3', 1, 3, 1)
gif = Fim_jogo(frame_bacana, (10, 0), inframes=2, musica="sons/bombermusica.mp3")
estado = "menu"
menuMusicaTocando = False
telas = Telas(tela)

pygame.font.init()
acabou_tempo = False
rodando = True  

# GUARDAR A PONTUAÇÃO DA FASE
while rodando:
    iniciar_tempo = pygame.time.get_ticks()

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

    #   ESTATÍSTICAS:
    #vida
    fonteText = pygame.font.SysFont('Arial', 40)
    vidas = f'Vidas: {vidas_player}'  
    vidasFormatado= fonteText.render(vidas, True, BRANCO)
    #tempo    
    tempo_fase = fase.verificar_tempoRestante() # Precis alterar
    minutos, segundos = divmod(tempo_fase, 60)
    tempo = '{:0.0f}:{:0.0f}'.format(minutos, segundos)
    tempo = str (tempo)
    tempoFormatado = fonteText.render(tempo, True, BRANCO)
    # pontuação        
    pontos_player=f'Pontuação: {pontos}'         
    pontosFormatado= fonteText.render(pontos_player, True, BRANCO)

    if estado == "menu":
        menu.desenhar(tela)
        if not menuMusicaTocando:
            pygame.mixer.music.load(menu.musica)
            pygame.mixer.music.play(-1)
            menuMusicaTocando = True

    elif estado == "jogo":
        menuMusicaTocando = False
        fase.atualizar(teclas)
        fase.desenhar(tela)
        fase.iniciarMusicaFase()
        tela.blit(vidasFormatado, (950,40))
        tela.blit(tempoFormatado,(500,40))
        tela.blit(pontosFormatado,(150,40))

        tela.blit(vidasFormatado, (950,40))
    # FIM DO JOGO        
    elif estado == "fim":        
        gif.iniciarMusicaMano()
        gif.atual()
        gif.desenhar(tela)

        #VERIFICANDO QUANDO COLIDIU NA PORTA ABERTA E DE QUAL FASE ESTÁ
    if fase.porta.aberta and fase.player.metadePlayer.colliderect(fase.porta.portinha) and fase.fase_atual == 1:
     if estado != "fim":  # para evitar repetir
            pontos_fase1 = pontos
            fase = Fases(mapa2, ROXO, 'sons/musica_jogatina.mp3', 2, 2, 2)          
    elif fase.porta.aberta and fase.player.metadePlayer.colliderect(fase.porta.portinha) and fase.fase_atual == 2:
     if estado != "fim":  # para evitar repetir     
            pontos_fase2 = pontos_fase1 + pontos  
            fase = Fases(mapa3, AMARELO, 'sons/musica_jogatina.mp3', 3, 3, 3)            
    elif fase.porta.aberta and fase.player.metadePlayer.colliderect(fase.porta.portinha) and fase.fase_atual == 3:
        estado = "fim"
        
# VERIFICA SE O TEMPO ACABOU
    if tempo_fase <= 0:
        pygame.mixer.music.pause() 
        fase.player.vivo = False
        vidas_player = 0            
        telas.telaAcabouTempo()
        telas.telaDerrota()
        if telas.telaContinuar():
            telas.telaDeLoading()
            pontos = 0
            vidas_player = 3                
            fase = Fases(mapa1, cor_fundoFase, 'sons/musica_jogatina.mp3', 1, 1, 1)
            estado = "jogo"
            pygame.mixer.music.play(-1)
        else:
            pygame.quit()
            exit()
    else:
        # VERIFICA QUANOO O PLAYER MORREU          
        if not fase.player.vivo:                         
            pygame.mixer.music.pause()        
            telas.telaMorte()                       
                                    
            if fase.player is not None:                    
                fase.desenhar(tela)
                fase.iniciarMusicaFase()
                tela.blit(vidasFormatado, (950,40))
                            
            relogio.tick(FPS)    
            # VERIFICA QUANDO A VIDA DO JOGADOR ACABOU
            if vidas_player <= 0:
                telas.telaDeLoading()
                telas.telaDerrota()
                if telas.telaContinuar():
                    telas.telaDeLoading()
                    pontos = 0
                    vidas_player = 3                
                    fase = Fases(mapa1, cor_fundoFase, 'sons/musica_jogatina.mp3', 1, 3, 1)
                    estado = "jogo"
                    pygame.mixer.music.play(-1)
                else:
                    pygame.quit()
                    exit()
            # QUANDO O PLAYER MORRE MAS AINDA POSSUI VIDAS
            else:
                pygame.mixer.music.unpause()                          
                 # VERIFICA EM QUAL FASE ESTÁ ATUALMENTE
                if fase.fase_atual == 1:
                     pontos = 0
                     fase = Fases(mapa1, VERDE_ESCURO, 'sons/musica_jogatina.mp3', 1, 1, 1)
                elif fase.fase_atual == 2: 
                    pontos = pontos_fase1                   
                    fase = Fases(mapa2, ROXO, 'sons/musica_jogatina.mp3', 2, 2, 2)
                elif fase.fase_atual == 3:
                    pontos = 0
                    pontos = pontos_fase2
                    fase = Fases(mapa3, AMARELO, 'sons/musica_jogatina.mp3', 3, 3, 3)
                fase.desenhar(tela)
                fase.iniciarMusicaFase()
                tela.blit(vidasFormatado, (950, 40))    
                
        elif estado == "fim":
            gif.atual()
            gif.desenhar(tela)

    relogio.tick(FPS)
    pygame.display.flip()

pygame.quit()