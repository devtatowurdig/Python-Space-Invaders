import random
import pygame


TAMANHO_GRADE = 17
TAMANHO_BOX = 28
MARGEM = 2

PLAYER = 'P'
INIMIGO = 'I'
TIRO_PLAYER = '.'
COLISAO = 'X'
VAZIO = ' '



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

tamanho_grade = TAMANHO_GRADE
tamanho_box = TAMANHO_BOX
margem = MARGEM

def desenha_tabuleiro(screen, tabuleiro):
    for indice_linha in range(tamanho_grade):
        for indice_coluna in range (tamanho_grade):
            pos_x = indice_coluna * (tamanho_box + margem) + margem
            pos_y = indice_linha * (tamanho_box + margem) + margem
            cor = (40, 40, 40) 
            if tabuleiro[indice_linha][indice_coluna] == PLAYER:
                cor = (0, 255, 0)
            elif tabuleiro[indice_linha][indice_coluna] == INIMIGO:
                cor = (255, 0, 0)
            elif tabuleiro[indice_linha][indice_coluna] == TIRO_PLAYER:
                cor = (255, 255, 0)
            elif tabuleiro[indice_linha][indice_coluna] == TIRO_PLAYER:
                cor = (255, 0, 255)
            pygame.draw.rect(screen, cor, (pos_x, pos_y, tamanho_box, tamanho_box)) # Onde desenhar, a cor, posicoes, largura, altura.

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
    for indice_coluna in range(len(tabuleiro[0])): 
        if tabuleiro[linha_topo][indice_coluna] == TIRO_PLAYER:
            tabuleiro[linha_topo][indice_coluna] = VAZIO
    
    for indice_linha in range(1, len(tabuleiro)):
        for indice_coluna in range(len(tabuleiro[indice_linha])):
            if tabuleiro[indice_linha][indice_coluna] == TIRO_PLAYER:
                if tabuleiro[indice_linha - 1][indice_coluna] == INIMIGO:
                    tabuleiro[indice_linha - 1][indice_coluna] = VAZIO  #remove inimigo
                    tabuleiro[indice_linha][indice_coluna] = VAZIO      #remove tiro
                elif tabuleiro[indice_linha - 1][indice_coluna] == VAZIO:
                    tabuleiro[indice_linha - 1][indice_coluna] = TIRO_PLAYER 
                    tabuleiro[indice_linha][indice_coluna] = VAZIO   
                else:
                    tabuleiro[indice_linha][indice_coluna] = VAZIO #remove tiro se bater no alvo   
                