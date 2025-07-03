import pygame
import sys
import time
import math

JOGADOR_HUMANO = 'X'
JOGADOR_IA = 'O'


def verificar_vencedor(tabuleiro, jogador):
    """Verifica se o jogador atual venceu."""
    # Verifica linhas
    for i in range(3):
        if all([tabuleiro[i][j] == jogador for j in range(3)]):
            return True
    
    # Verifica colunas
    for j in range(3):
        if all([tabuleiro[i][j] == jogador for i in range(3)]):
            return True
    
    # Verifica diagonais
    if all([tabuleiro[i][i] == jogador for i in range(3)]):
        return True
    if all([tabuleiro[i][2-i] == jogador for i in range(3)]):
        return True
    
    return False

def verificar_empate(tabuleiro):
    """Verifica se o jogo empatou."""
    for linha in tabuleiro:
        if ' ' in linha:
            return False # Ainda há espaços vazios
    return True

def minimax(tabuleiro, profundidade, is_maximizador):
    """Algoritmo Minimax para determinar a pontuação de uma jogada."""
    if verificar_vencedor(tabuleiro, JOGADOR_IA):
        return 10
    if verificar_vencedor(tabuleiro, JOGADOR_HUMANO):
        return -10
    if verificar_empate(tabuleiro):
        return 0
    
    # Recursao
    if is_maximizador: # jogada da IA (Quer maximizar a pontuação)
        melhor_pontuacao = -float('inf')
        for i in range(3):
            for j in range(3):
                if tabuleiro[i][j] == ' ':
                    tabuleiro[i][j] = JOGADOR_IA
                    pontuacao = minimax(tabuleiro, profundidade + 1, False)
                    tabuleiro[i][j] = ' '
                    melhor_pontuacao = max(melhor_pontuacao, pontuacao)
        return melhor_pontuacao
    else: # jogada do humano (Quer minimizar a pontuacao)
        melhor_pontuacao = float('inf')
        for i in range(3):
            for j in range(3):
                if tabuleiro[i][j] == ' ':
                    tabuleiro[i][j] = JOGADOR_HUMANO
                    pontuacao = minimax(tabuleiro, profundidade + 1, True)
                    tabuleiro[i][j] = ' '
                    melhor_pontuacao = min(melhor_pontuacao, pontuacao)
        return melhor_pontuacao

def encontrar_melhor_jogada(tabuleiro):
    """Encontra a melhor jogada par a IA usando o algoritmo Minimax."""
    melhor_pontuacao = -float('inf')
    melhor_jogada = (-1,-1) # Inicializa com uma jogada inválida

    for i in range(3):
        for j in range(3):
            if tabuleiro[i][j] == ' ':
                tabuleiro[i][j] = JOGADOR_IA
                pontuacao = minimax(tabuleiro, 0, False)
                tabuleiro[i][j] = ' ' 
                if pontuacao > melhor_pontuacao:
                    melhor_pontuacao = pontuacao
                    melhor_jogada = (i,j)
    return melhor_jogada

pygame.init()

LARGURA, ALTURA = 600, 600
TAMANHO_LINHA = 15
COR_FUNDO = (28, 170, 156)
COR_LINHA = (23, 145, 135)
COR_X = (84,84,84)
COR_O = (242, 235, 211)
FONTE = pygame.font.SysFont('Consolas', 60)

# Configuracao da tela
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo da Velha - Você vs IA")

def desenhar_grade():
    """Desenha as linhas do tabuleiro na tela."""
    # Linhas horizontais
    pygame.draw.line(tela, COR_LINHA, (0, 200), (600,200), TAMANHO_LINHA)
    pygame.draw.line(tela, COR_LINHA, (0, 400), (600,400), TAMANHO_LINHA)
    # Linhas verticais
    pygame.draw.line(tela, COR_LINHA, (200, 0), (200,600), TAMANHO_LINHA)
    pygame.draw.line(tela, COR_LINHA, (400, 0), (400,600), TAMANHO_LINHA)

def desenhar_simbolos(tabuleiro):
    """Desenha 'X' e 'O' no tabuleiro com base na matriz."""
    for linha in range(3):
        for coluna in range(3):
            if tabuleiro[linha][coluna] == JOGADOR_HUMANO:
                pygame.draw.line(tela, COR_X, (coluna * 200 + 55, linha * 200 + 55), (coluna * 200 + 145, linha * 200 + 145), 25)
                pygame.draw.line(tela, COR_X, (coluna * 200 + 55, linha * 200 + 145), (coluna * 200 + 145, linha * 200 + 55), 25)
            elif tabuleiro[linha][coluna] == JOGADOR_IA:
                pygame.draw.circle(tela, COR_O, (coluna * 200 + 100, linha * 200 + 100), 60, 15)

def mostrar_mensagem_final(mensagem):
    """Exibe uma mensagem de fim de jogo na tela."""
    texto = FONTE.render(mensagem, True, (255,60,50))
    retangulo_texto = texto.get_rect(center=(LARGURA/2, ALTURA/2))

    fundo = pygame.Surface((retangulo_texto.width + 10, retangulo_texto.height + 10), pygame.SRCALPHA)
    fundo.fill((0,0,0, 128))
    tela.blit(fundo, (retangulo_texto.left - 10, retangulo_texto.top - 10))
    tela.blit(texto, retangulo_texto)
    pygame.display.flip()

def main():
    """Função principal que roda o loop do jogo."""
    tabuleiro = [[' ' for _ in range(3)] for _ in range(3)]
    jogador_atual = JOGADOR_HUMANO
    jogo_acabou = False
    mensagem = ""

    desenhar_grade()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN and not jogo_acabou:
                if jogador_atual == JOGADOR_HUMANO:
                    mouseX = event.pos[0] # Coordenada X do mouse
                    mouseY = event.pos[1] # Coordenada Y do mouse

                    linha_clicada = int(mouseY // 200)
                    coluna_clicada = int(mouseX // 200)

                    if tabuleiro[linha_clicada][coluna_clicada] == ' ':
                        tabuleiro[linha_clicada][coluna_clicada] = JOGADOR_HUMANO
                        if verificar_vencedor(tabuleiro, JOGADOR_HUMANO):
                            mensagem = "VOCE VENCEU!"
                            jogo_acabou = True
                        elif verificar_empate(tabuleiro):
                            mensagem = "EMPATE!"
                            jogo_acabou = True
                        jogador_atual = JOGADOR_IA

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: # Tecla 'r' para reiniciar o jogo
                    main() # Reinicia o jogo
            
            if jogador_atual == JOGADOR_IA and not jogo_acabou:
                linha, coluna = encontrar_melhor_jogada(tabuleiro)
                if tabuleiro[linha][coluna] == ' ':
                    time.sleep(0.5) # Simula o tempo de pensamento da IA
                    tabuleiro[linha][coluna] = JOGADOR_IA
                    if verificar_vencedor(tabuleiro, JOGADOR_IA):
                        mensagem = "A IA VENCEU!"
                        jogo_acabou = True
                    elif verificar_empate(tabuleiro):
                        mensagem = "EMPATE!"
                        jogo_acabou = True
                    jogador_atual = JOGADOR_HUMANO
            
            # Desenha
            tela.fill(COR_FUNDO)
            desenhar_grade()
            desenhar_simbolos(tabuleiro)

            if jogo_acabou:
                mostrar_mensagem_final(mensagem)
            
            pygame.display.flip()

if __name__ == '__main__':
    main()



