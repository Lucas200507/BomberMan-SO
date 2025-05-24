global alturaTela, larguraTela
alturaTela = 870
larguraTela = 1240
FPSmenu = 5
FPSfases = 100

# 0 = quadrado com borda
# 1 = NULL
# 2 = quadrado sem borda
# 3 = bloco indestrutível
TAMANHO_BLOCO = 66
mapa_jogo = [
 [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
 [3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3],
 [3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3],
 [3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3],
 [3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3],
 [3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3],
 [3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3],
 [3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3],
 [3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3],
 [3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3],
 [3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3],
 [3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3],
 [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],

 
]



# variaveis Menu
MenuLogo = 'logoBao.png'
# MenuLogo = 'logoPacMan.png'
tamanhoLogo = (762, 502)
# variaveis fontes
#Text Press
TPressR_FontFamily = 'Arial'
TPressR_Syze = 50
TPressR_Bold = True
TPressR_Italic = False
# velocidade movimentação PLAYER
velocidadePlayer = 1


VERMELHO = (255,0,0)
AZUL = (0,0,255)
VERDE = (0,255,0)
BRANCO = (255,255,255)
PRETO = (0,0,0)
VERDE_ESCURO = (0,100,0)
CINZA = (211,211,211)
CINZA_ESCURO = (60,60,60)