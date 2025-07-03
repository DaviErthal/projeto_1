# Criando um tabuleiro de jogo da velha

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

def obter_jogada(jogador_atual, tabuleiro):
    """Obtém a jogada do jogador atual, valida e retorna a posição."""
    
    # Este dicionário ajuda a converter o input 1-9 para as coordenadas da matriz
    mapa_posicao = {
        1: (0, 0), 2: (0, 1), 3: (0, 2),
        4: (1, 0), 5: (1, 1), 6: (1, 2),
        7: (2, 0), 8: (2, 1), 9: (2, 2)
    }

    while True: # Loop até receber uma jogada válida
        try:
            posicao = int(input(f'Jogador "{jogador_atual}", escolha sua posição (1-9): '))
            
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

def jogar():
    """Função prnicipal que executa o jogo."""
    tabuleiro = criar_tabuleiro()
    jogador_atual = 'X'
    jogo_em_andamento = True

    print("Bem-vindo ao Jogo da Velha!")

    while jogo_em_andamento:
        exibir_tabuleiro(tabuleiro)
        linha, coluna = obter_jogada(jogador_atual, tabuleiro)
        tabuleiro[linha][coluna] = jogador_atual

        # Verifica se houve vencedor
        if verificar_vencedor(tabuleiro, jogador_atual):
            exibir_tabuleiro(tabuleiro)
            print(f'Jogador "{jogador_atual}" venceu"')
            jogo_em_andamento = False
        
        # Verifica se houve empate
        elif verificar_empate(tabuleiro):
            exibir_tabuleiro(tabuleiro)
            print("O jogo empatou!")
            jogo_em_andamento = False
        else:
            # Alterna o jogador
            jogador_atual = 'O' if jogador_atual == 'X' else 'X'


# Para iniciar o jogo, basta chamar a função jogar()
if __name__ == "__main__":
    print("Bem-vindo ao Jogo da Velha!")

    while True: # Loop para controlar se o jogador quer jogar NOVAMENTE
        jogar() # Executa uma partida completa

        # Pergunta se quer jogar de novo
        jogar_novamente = input("Deseja jogar novamente? (s/n): ").lower()
        if jogar_novamente != 's':
            break # Sai do loop se a resposta não for 's'
    
    print("\nObrigado por jogar! Até a próxima.")






