import random
import pygame
import time


TAMANHO_GRADE = 17
TAMANHO_BOX = 28
MARGEM = 2

PLAYER = 'P'
INIMIGO = 'I'
TIRO_PLAYER = '.'
COLISAO = 'X'
VAZIO = ' '
TAMANHO_TELA_CALCULADO = (TAMANHO_BOX + MARGEM) * TAMANHO_GRADE + MARGEM


tabuleiro = []

def cria_tabuleiro():
    for i in range(17):
        tabuleiro.append([]) #adiciona um array dentro do array
        for _ in range(17):
            tabuleiro[i].append(' ')
            
def posiciona_player(player_x, player_y):
    tabuleiro[player_y][player_x] = PLAYER

def posiciona_inimigos():
    colunas_inimigos = random.sample(range(17), 2) #sorteia 2 números do range para posicionar os inimigos
    for c in colunas_inimigos:
        tabuleiro[0][c] = INIMIGO
        
def conta_inimigos(tabuleiro):
    contador_total = 0
    for linha in tabuleiro:
        inimigos_ingame = linha.count(INIMIGO)
        contador_total = contador_total + inimigos_ingame
    return contador_total



def desenha_tabuleiro(screen, tabuleiro):
    for indice_linha in range(TAMANHO_GRADE):
        for indice_coluna in range (TAMANHO_GRADE):
            pos_x = indice_coluna * (TAMANHO_BOX + MARGEM) + MARGEM
            pos_y = indice_linha * (TAMANHO_BOX + MARGEM) + MARGEM
            cor = (40, 40, 40) 
            if tabuleiro[indice_linha][indice_coluna] == PLAYER:
                cor = (0, 255, 0)
            elif tabuleiro[indice_linha][indice_coluna] == INIMIGO:
                cor = (255, 0, 0)
            elif tabuleiro[indice_linha][indice_coluna] == TIRO_PLAYER:
                cor = (255, 255, 0)
            elif tabuleiro[indice_linha][indice_coluna] == COLISAO:
                cor = (255, 0, 255)
            pygame.draw.rect(screen, cor, (pos_x, pos_y, TAMANHO_BOX, TAMANHO_BOX)) # Onde desenhar, a cor, posicoes, largura, altura.

def move_inimigo(tabuleiro, player_x, player_y):
    for indice_linha in range(len(tabuleiro)-2, -1, -1):
        for indice_coluna in range(len(tabuleiro[indice_linha])):
            
            if tabuleiro[indice_linha][indice_coluna] == INIMIGO:
                linha_abaixo = indice_linha + 1
                
                if linha_abaixo == player_y and indice_coluna == player_x: # Se o inimigo encostou no player
                    tabuleiro[indice_linha][indice_coluna] = VAZIO
                    tabuleiro[player_y][player_x] = COLISAO
                    return True
                
                if tabuleiro[linha_abaixo][indice_coluna] == VAZIO: # Move para espaço vazio
                    tabuleiro[linha_abaixo][indice_coluna] = INIMIGO
                    tabuleiro[indice_linha][indice_coluna] = VAZIO
    
    ultima_linha= len(tabuleiro) -1
    for indice_coluna in range(len(tabuleiro[ultima_linha])): # Tira do tabuleiro inimigos que chegam no final
        if tabuleiro[ultima_linha][indice_coluna] == INIMIGO:
            tabuleiro[ultima_linha][indice_coluna] = VAZIO
    
    return False

def conta_tiros(tabuleiro):
    contador_total = 0
    for linha in tabuleiro:
        tiros_ingame = linha.count(TIRO_PLAYER)
        contador_total = contador_total + tiros_ingame
        
def atirar(tabuleiro, player_x, player_y):
    if conta_tiros(tabuleiro) == 0:
        if player_y > 0 and tabuleiro[player_y - 1][player_x] == VAZIO:
            tabuleiro[player_y - 1][player_x] = TIRO_PLAYER
            
def move_tiros(tabuleiro):
    linha_topo = 0
    for indice_coluna in range(TAMANHO_GRADE): 
        if tabuleiro[linha_topo][indice_coluna] == TIRO_PLAYER:
            tabuleiro[linha_topo][indice_coluna] = VAZIO
    
    for indice_linha in range(1, TAMANHO_GRADE):
        for indice_coluna in range(TAMANHO_GRADE):
            
            if tabuleiro[indice_linha][indice_coluna] == TIRO_PLAYER:
                linha_acima = indice_linha - 1
                
                if tabuleiro[linha_acima][indice_coluna] == INIMIGO:
                   tabuleiro[linha_acima][indice_coluna] = VAZIO #remove inimigo
                   tabuleiro[indice_linha][indice_coluna] = VAZIO #remove tiro
                   
                elif tabuleiro[linha_acima][indice_coluna] == VAZIO:
                    tabuleiro[linha_acima][indice_coluna] = TIRO_PLAYER
                    tabuleiro[indice_linha][indice_coluna] = VAZIO
                
                else:
                    tabuleiro[indice_linha][indice_coluna] = VAZIO

def tela_start(screen):
    imagem = pygame.image.load("start.png")
    imagem = pygame.transform.scale(imagem, (screen.get_width(), screen.get_height()))
    rect = imagem.get_rect(screen.get_width() // 2, screen.get_height() // 2)
    esperando = True
    while esperando:
        screen.fill((0, 0, 0))
        screen.blit(imagem, rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                esperando = False
                
def tela_nome_jogador(screen):
    fonte = pygame.font.SysFont("bold", 48)
    nome = ""
    ativo = True
    while ativo:
        screen.fill((0, 0, 0))
        texto = fonte.render("Digite seu nome:", True, (255, 255, 255))
        rect = texto.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 40))
        screen.blit(texto, rect)
        texto_nome = fonte.render(nome, True, (0, 255, 0))
        rect_nome = texto_nome.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 20))
        screen.blit(texto_nome, rect_nome)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(nome) > 0:
                    ativo = False
                elif event.key == pygame.K_BACKSPACE:
                    nome = nome[:-1]
                else:
                    if len(nome) < 12 and event.unicode.isprintable():
                        nome += event.unicode
    return nome


def atualiza_ranking(jogador, pontuacao): 
    NOME_ARQUIVO = "ranking.txt"
    ranking = []
    
    try:
        with open("ranking.txt", "r") as arquivo:
            linhas = arquivo.readlines()
            for linha in linhas:
                partes = linha.strip().split(';')
                if len(partes) == 2:
                    ranking.append((partes[0], int(partes[1])))
    except FileNotFoundError:
        pass
    
    ranking.append((jogador, pontuacao))
    ranking = sorted(ranking, key = lambda x: x[1], reverse = True)[:5]
    
    with open("ranking.txt", "w") as arquivo:
        for nome, pontos in ranking:
            arquivo.write(f"{nome};{pontos}\n")
            
    return ranking

def tela_ranking(screen, ranking_lista):
    fonte_titulo = pygame.font.SysFont("bold", 64)
    fonte_texto = pygame.font.SysFont(None, 48)
    
    screen.fill((0 , 2, 0))
    
    titulo = fonte_titulo.render("Ranking - Top 5", True, (255, 255, 0))
    rect_titulo = titulo.get_rect(center=(screen.get_width() // 2, 80))
    screen.blit(titulo, rect_titulo)
    
    posicao_y = 160
    for indice, (nome, pontos) in enumerate(ranking_lista):
        texto_ranking = f"{indice + 1}. {nome} - {pontos}"
        
        superficie_texto = fonte_texto.render(texto_ranking, True, (255, 255, 255))
        rect_texto = superficie_texto.get_rect(center=(screen.get_width() // 2, posicao_y))
        screen.blit(superficie_texto, rect_texto)
        
        posicao_y += 60
        
    pygame.display.flip()
    time.sleep(4)
    
def tela_gameover(screen):
    fonte_go = pygame.font.SysFont(None, 64)
    texto_go = fonte_go.render("Game Over!", True, (255, 0, 0))
    rect_go = texto_go.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    
    screen.fill((0 , 0, 0))
    screen.blit(texto_go, rect_go)
    pygame.display.flip()
    time.sleep(3)
                         
def tela_continue(screen):
    fonte = pygame.font.SysFont(None, 40)
    esperando = True
    
    while esperando:
        screen.fill((0, 0, 0))
        
        texto_render = fonte.render("Pressione ENTER para jogar novamente ou ESC para sair")
        rect_texto = texto_render.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 ))
        screen.blit(texto_render, rect_texto)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        
        for event in pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return True
            if event.key == pygame.K_ESCAPE:
                return False
                         
                         



## Programa 

pygame.init()
screen = pygame.display.set_mode((TAMANHO_TELA_CALCULADO, TAMANHO_TELA_CALCULADO))
pygame.display.set_caption("Python Space Invadars - Matriz")
clock = pygame.time.Clock()

tela_start(screen)
jogador = tela_nome_jogador(screen)

jogando_app = True

while jogando_app:
    
    wave = 1
    max_waves = 5 #TODO:Alterar pra escolher a dificuldade
    game_over = False
    Vitoria = False
    font_wave = pygame.font.SysFont(None, 32)
    pontuacao = 0


    cria_tabuleiro()
    player_x = 9
    player_y = 16
    posiciona_player(player_x, player_y)
    posiciona_inimigos()
    inimigo_timer = 0
    inimigo_intervalo = 10
    
    
        
    while not game_over: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                jogando_app = False
                
        keys = pygame.key.get_pressed()
        
        #Teclas de movimento do player
        if keys[pygame.K_a] and player_x > 0:
            tabuleiro[player_y][player_x] =  VAZIO
            player_x = player_x - 1
            tabuleiro[player_y][player_x] = PLAYER
        elif keys[pygame.K_d] and player_x < TAMANHO_GRADE - 1 :
            tabuleiro[player_y][player_x] =  VAZIO
            player_x = player_x + 1
            tabuleiro[player_y][player_x] =  PLAYER
            
        #Tiro
        if keys[pygame.K_SPACE]:
            atirar(tabuleiro, player_x, player_y)
        
        inimigo_timer = inimigo_timer + 1
        if inimigo_timer >= inimigo_intervalo:
            if move_inimigo(tabuleiro, player_x, player_y):
                desenha_tabuleiro(screen, tabuleiro)
                pygame.display.flip()
                tela_gameover(screen)
                break
            inimigo_timer = 0
        move_tiros(tabuleiro)
        
        if conta_inimigos(tabuleiro) == 0:
            pontuacao += 100
            if wave < max_waves:
                wave = wave + 1
                
                for indice_linha in range(TAMANHO_GRADE):
                    for indice_coluna in range(TAMANHO_GRADE):
                        if tabuleiro[indice_linha][indice_coluna] in [INIMIGO, TIRO_PLAYER, COLISAO]:
                            tabuleiro[indice_linha][indice_coluna] = VAZIO
                posiciona_inimigos()
            else:
                vitoria = True
                game_over = True
        
        screen.fill((0, 0, 0))
        desenha_tabuleiro(screen, tabuleiro)
        
        texto_wave = font_wave.render(f'Wave: {wave}', True, (255, 255, 255))
        screen.blit(texto_wave, (10, 10))
        texto_score = font_wave.render(f'Score: {pontuacao}', True, (255, 255, 0))
        screen.blit(texto_score, (10, 40))
        
        pygame.display.flip()
        clock.tick(15)
        
        
        
        #Reiniciar o jogo
    
    if jogando_app:
        if vitoria:
            screen.fill((0, 0, 0))
            fonte_vitoria = pygame.font.SysFont(None, 64)
            texto_vitoria = fonte_vitoria.render('Vitória!!', True, (0, 255, 0))
            rect = texto_vitoria.get_rect(center = (screen.get_width() // 2, screen.get_height() // 2))
            screen.blit(texto_vitoria, rect)
            pygame.display.flip()
            time.sleep(3)
            
        ranking_atual = atualiza_ranking(jogador, pontuacao)
        tela_ranking(screen, ranking_atual)
        
        #Contiue
        jogando_app = tela_continue(screen)

pygame.quit()
exit()
            
    
