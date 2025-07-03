# Criando um tabuleiro de jogo da velha

import time

jogador_humano = 'X'
jogador_ia = 'O'


def criar_tabuleiro():
    """Cria um tabuleiro vazio para o jogo da velha."""
    return [[' ' for _ in range(3)] for _ in range(3)]

def exibir_tabuleiro(tabuleiro):
    """Exibe o tabuleiro do jogo da velha."""
    print()
    print(' '+ tabuleiro[0][0] + ' | ' + tabuleiro[0][1] + ' | ' + tabuleiro[0][2])
    print('---|---|---')
    print(' '+ tabuleiro[1][0] + ' | ' + tabuleiro[1][1] + ' | ' + tabuleiro[1][2])
    print('---|---|---')
    print(' '+ tabuleiro[2][0] + ' | ' + tabuleiro[2][1] + ' | ' + tabuleiro[2][2])
    print()

def obter_jogada_humano( tabuleiro):
    """Obtém a jogada do jogador humano, valida e retorna a posição."""
    
    # Este dicionário ajuda a converter o input 1-9 para as coordenadas da matriz
    mapa_posicao = {
        1: (0, 0), 2: (0, 1), 3: (0, 2),
        4: (1, 0), 5: (1, 1), 6: (1, 2),
        7: (2, 0), 8: (2, 1), 9: (2, 2)
    }

    while True: # Loop até receber uma jogada válida
        try:
            posicao = int(input(f'Sua vez, "{jogador_humano}", escolha sua posição (1-9): '))
            
            # 1. Verifica se o número está entre 1 e 9
            if 1 <= posicao <= 9:
                # 2. Converte o número para linha e coluna
                linha, coluna = mapa_posicao[posicao]
                
                # 3. Verifica se o local no tabuleiro está vazio
                if tabuleiro[linha][coluna] == ' ':
                    return linha, coluna # Retorna a jogada válida
                else:
                    print("Essa posição já está ocupada. Tente novamente.")
            else:
                print("Posição inválida. Por favor, digite um número entre 1 e 9.")
        except ValueError:
            print("Entrada inválida. Por favor, digite um número.")
            
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
    if verificar_vencedor(tabuleiro, jogador_ia):
        return 10
    if verificar_vencedor(tabuleiro, jogador_humano):
        return -10
    if verificar_empate(tabuleiro):
        return 0
    
    # Recursao
    if is_maximizador: # jogada da IA (Quer maximizar a pontuação)
        melhor_pontuacao = -float('inf')
        for i in range(3):
            for j in range(3):
                if tabuleiro[i][j] == ' ':
                    tabuleiro[i][j] = jogador_ia
                    pontuacao = minimax(tabuleiro, profundidade + 1, False)
                    tabuleiro[i][j] = ' '
                    melhor_pontuacao = max(melhor_pontuacao, pontuacao)
        return melhor_pontuacao
    else: # jogada do humano (Quer minimizar a pontuacao)
        melhor_pontuacao = float('inf')
        for i in range(3):
            for j in range(3):
                if tabuleiro[i][j] == ' ':
                    tabuleiro[i][j] = jogador_humano
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
                tabuleiro[i][j] = jogador_ia
                pontuacao = minimax(tabuleiro, 0, False)
                tabuleiro[i][j] = ' ' 
                if pontuacao > melhor_pontuacao:
                    melhor_pontuacao = pontuacao
                    melhor_jogada = (i,j)
    return melhor_jogada

def jogar():
    """Função prnicipal que executa o jogo."""
    tabuleiro = criar_tabuleiro()
    jogador_atual = jogador_humano


    print("Bem-vindo ao Jogo da Velha!")

    while True:
        exibir_tabuleiro(tabuleiro)

        if jogador_atual == jogador_humano:
            linha, coluna = obter_jogada_humano(tabuleiro)
            tabuleiro[linha][coluna] = jogador_humano
        else:
            print(f'Vez da IA "{jogador_ia}"... pensando...')
            time.sleep(1)
            linha, coluna = encontrar_melhor_jogada(tabuleiro)
            tabuleiro[linha][coluna] = jogador_ia
            print(f'IA jogou na posição ({linha+1}, {coluna+1})')
        

        # Verifica se houve vencedor
        if verificar_vencedor(tabuleiro, jogador_atual):
            exibir_tabuleiro(tabuleiro)
            vencedor = "Você" if jogador_atual == jogador_humano else "A IA"
            print(f'Fimde jogo! "{vencedor}" venceu!"')
            break
        
        # Verifica se houve empate
        elif verificar_empate(tabuleiro):
            exibir_tabuleiro(tabuleiro)
            print("O jogo empatou!")
            break

        jogador_atual = jogador_ia if jogador_atual == jogador_humano else jogador_humano
       


# Para iniciar o jogo, basta chamar a função jogar()
if __name__ == "__main__":
    print("Bem-vindo ao Jogo da Velha! Você joga como 'X'.")

    while True: # Loop para controlar se o jogador quer jogar NOVAMENTE
        jogar() # Executa uma partida completa

        # Pergunta se quer jogar de novo
        jogar_novamente = input("Deseja jogar novamente? (s/n): ").lower()
        if jogar_novamente != 's':
            break # Sai do loop se a resposta não for 's'
    
    print("\nObrigado por jogar! Até a próxima.")

