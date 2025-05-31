import pygame
import random
import threading
import time
from pygame.locals import *
from sys import exit

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO = (25, 0, 0)
VERDE_ESCURO = (0, 100, 0)
cor_fundoFase = VERDE_ESCURO

limite_bombas = threading.Semaphore(3)

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

FPS = 60
relogio = pygame.time.Clock()
pygame.mixer.music.set_volume(0.5)

largura = 1123
altura = 861

pygame.display.set_caption('TESTE2')
tela = pygame.display.set_mode((largura, altura))

velocidade_player = 4
tamanho_bloco = 66
tamanho_player = 60
posXInicial = 75
posYInicial = 70


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
    def __init__(self, x, y, tamanho, img, destrutivel=False):
        self.block = pygame.Rect(x, y, tamanho, tamanho)
        self.backgroundImg = pygame.transform.scale(pygame.image.load(img), (tamanho, tamanho))
        self.destruivel = destrutivel
        self.ativo = True

    def desenhar(self, tela):
        if self.ativo:
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
                    self.blocos.append(Blocos(x * self.tamanho_bloco, y * self.tamanho_bloco, self.tamanho_bloco, "imagens/tijolos.png", destrutivel=True))
                elif valor == 4:
                    self.blocos.append(Blocos(x * self.tamanho_bloco, y * self.tamanho_bloco, self.tamanho_bloco, "imagens/Bloco_Indestrutivel2.png"))

    def desenhar(self, tela):
        for bloco in self.blocos:
            bloco.desenhar(tela)

class Player:
    def __init__(self, x, y, tamanho, frame):
        self.player = pygame.Rect(x, y, tamanho, tamanho)
        self.playerImg = pygame.image.load(frame)
        self.playerRedimensionado = pygame.transform.scale(self.playerImg, (tamanho - 5, tamanho))
        self.velocidade = 4
        self.metadePlayer = pygame.Rect(x, y + (tamanho // 2), tamanho - 5, tamanho // 2)

    def mover(self, teclas, blocos):
        mover_x, mover_y = 0, 0
        if teclas[K_LEFT]: mover_x = -self.velocidade
        elif teclas[K_RIGHT]: mover_x = self.velocidade
        if teclas[K_UP]: mover_y = -self.velocidade
        elif teclas[K_DOWN]: mover_y = self.velocidade

        self.player.x += mover_x
        self.atualizar_metadePlayer()
        if self.colidiu(blocos): self.player.x -= mover_x

        self.player.y += mover_y
        self.atualizar_metadePlayer()
        if self.colidiu(blocos): self.player.y -= mover_y

    def atualizar_metadePlayer(self):
        self.metadePlayer.x = self.player.x
        self.metadePlayer.y = self.player.y + (self.player.height // 2)

    def colidiu(self, blocos):
        return any(self.metadePlayer.colliderect(b.block) for b in blocos)

    def desenhar(self, tela):
        tela.blit(self.playerRedimensionado, self.player.topleft)

class Inimigo:
    def __init__(self, x, y, velocidade=0.1):
        self.x = x
        self.y = y
        self.velocidade = velocidade
        self.tamanho = tamanho_bloco
        self.vivo = True
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
                self.atualiza_posicao(direcao)
                break

    def pode_mover(self, direcao, mapa):
        nova_x, nova_y = self.x, self.y
        if direcao == 'cima': nova_y -= 1
        elif direcao == 'baixo': nova_y += 1
        elif direcao == 'esquerda': nova_x -= 1
        elif direcao == 'direita': nova_x += 1
        
         # Verifica limites
        if nova_y < 0 or nova_y >= len(mapa) or nova_x < 0 or nova_x >= len(mapa[0]):
            return False
        return mapa[nova_y][nova_x] == 1


    def atualiza_posicao(self, direcao):
        if direcao == 'cima': self.y -= 1
        elif direcao == 'baixo': self.y += 1
        elif direcao == 'esquerda': self.x -= 1
        elif direcao == 'direita': self.x += 1

    def verificar_morte(self, explosoes):
        if (self.x, self.y) in explosoes:
            self.vivo = False

    def __repr__(self):
        return f"Inimigo(x={self.x}, y={self.y}, vivo={self.vivo})"

    def desenhar(self, tela):
        tela.blit(self.imagem, (self.x * self.tamanho, self.y * self.tamanho))

#criando a classe bomba
class Bomb:

    #atributos para as imagens
    bomb_img = pygame.image.load("imagens/bomba.png")
    bomb_img = pygame.transform.scale(bomb_img, (tamanho_bloco, tamanho_bloco)) 
    explosion_img = pygame.image.load("imagens/explosion.png")
    explosion_img = pygame.transform.scale(explosion_img, (tamanho_bloco, tamanho_bloco))
    

    def __init__(self, x, y, fase, delay=3):
        self.x = x
        self.y = y
        self.fase = fase
        self.delay = delay
        self.explosoes = []
        threading.Thread(target=self.explodir, daemon=True).start()

    
    def explodir(self):
        time.sleep(self.delay)
        self.explosoes.append((self.x, self.y))

        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = self.x + dx, self.y + dy
            if 0 <= ny < len(self.fase.mapa_layout) and 0 <= nx < len(self.fase.mapa_layout[0]):
                tile = self.fase.mapa_layout[ny][nx]
                if tile == 2:
                    self.fase.mapa_layout[ny][nx] = 1
                
                    for bloco in self.fase.mapa.blocos:
                            if bloco.block.x == nx * tamanho_bloco and bloco.block.y == ny * tamanho_bloco:
                                self.fase.mapa.blocos.remove(bloco)
                                break
                
                elif tile in (3, 4):
                    continue
                self.explosoes.append((nx, ny))

        jogador_x = self.fase.player.player.x // tamanho_bloco
        jogador_y = self.fase.player.player.y // tamanho_bloco
        if (jogador_x, jogador_y) in self.explosoes:
            self.fase.player.player.x = posXInicial
            self.fase.player.player.y = posYInicial

        for inimigo in self.fase.inimigos:
            if (inimigo.x, inimigo.y) in self.explosoes:
                inimigo.vivo = False
                print(f"Inimigo eliminado: {inimigo}")
        
        for blocos in self.fase.mapa.blocos:
            for ex, ey in self.explosoes:
                if (blocos.block.x // tamanho_bloco, blocos.block.y // tamanho_bloco) == (ex, ey) and blocos.destruivel:
                    blocos.ativo = False

        time.sleep(0.3)
        self.fase.bombas.remove(self)
    
    

class Fases:
    def __init__(self, mapa, cor_fundo, musica):
        self.mapa_layout = mapa
        self.mapa = Mapa(self.mapa_layout, tamanho_bloco)
        self.player = Player(posXInicial, posYInicial, tamanho_player, 'imagens/robo_parado1.png')
        self.musicaTocando = False
        self.musica = musica
        self.cor_fundo = cor_fundo
        self.inimigos = [
            Inimigo(3, 3),
            Inimigo(5, 7),
            Inimigo(10, 5),
        ]
        self.bombas = []
        self.blocos=[]

    def verificarColisaoEntrePlayerOuInimigos(self):
        for inimigo in self.inimigos:
            if inimigo.vivo and self.player.player.colliderect(pygame.Rect(inimigo.x * tamanho_bloco, inimigo.y * tamanho_bloco, tamanho_bloco, tamanho_bloco)):
                self.player.player.x = posXInicial
                self.player.player.y = posYInicial
                self.player.atualizar_metadePlayer()
    
    

    def colocar_bomba(self):
            grid_x = self.player.player.x // tamanho_bloco
            grid_y = self.player.player.y // tamanho_bloco
            if not any(b.x == grid_x and b.y == grid_y for b in self.bombas):
                bomba = Bomb(grid_x, grid_y, self)
                self.bombas.append(bomba)


    def atualizar(self, teclas):
        self.player.mover(teclas, self.mapa.blocos)
        for inimigo in self.inimigos:
            if inimigo.vivo:
                inimigo.mover(self.mapa_layout)
        self.verificarColisaoEntrePlayerOuInimigos()
        if teclas[pygame.K_SPACE]:
            self.colocar_bomba()

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
            tela.blit(Bomb.bomb_img, (bomba.x * tamanho_bloco, bomba.y * tamanho_bloco))
            for ex, ey in bomba.explosoes:
                tela.blit(Bomb.explosion_img, (ex * tamanho_bloco, ey * tamanho_bloco))
        
        for inimigo in self.inimigos:
            if inimigo.vivo:
                inimigo.desenhar(tela)
        
        for blocos in self.blocos:
            if (blocos.valor.x,blocos.valor.y == 2):
                if(blocos.x,blocos.y == True):
                    blocos.desenhar(tela)

              


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