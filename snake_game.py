import pygame
import random
import time
import sys

# Inicializa o pygame
pygame.init()

# Constantes
LARGURA, ALTURA = 600, 400
TAMANHO_GRADE = 20
LARGURA_GRADE = LARGURA // TAMANHO_GRADE
ALTURA_GRADE = ALTURA // TAMANHO_GRADE
BRANCO = (255, 255, 255)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
PRETO = (0, 0, 0)
AZUL = (0, 0, 255)
VELOCIDADE = 10

# Janela do jogo
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Jogo da Cobra')
relogio = pygame.time.Clock()

# Fonte para exibição da pontuação
fonte = pygame.font.SysFont('Arial', 25)

class Cobra:
    def __init__(self):
        self.posicoes = [(LARGURA_GRADE // 2, ALTURA_GRADE // 2)]
        self.direcao = (1, 0)  # Começa movendo para a direita
        self.crescer = False
        self.cor = VERDE
    
    def obter_posicao_cabeca(self):
        return self.posicoes[0]
    
    def atualizar(self):
        cabeca = self.obter_posicao_cabeca()
        x, y = self.direcao
        nova_posicao = ((cabeca[0] + x) % LARGURA_GRADE, (cabeca[1] + y) % ALTURA_GRADE)
        
        # Game over se a cobra colidir com ela mesma
        if nova_posicao in self.posicoes[1:]:
            return False
        
        self.posicoes.insert(0, nova_posicao)
        
        if not self.crescer:
            self.posicoes.pop()
        else:
            self.crescer = False
        
        return True
    
    def reiniciar(self):
        self.posicoes = [(LARGURA_GRADE // 2, ALTURA_GRADE // 2)]
        self.direcao = (1, 0)
        self.crescer = False
    
    def desenhar(self, superficie):
        for posicao in self.posicoes:
            retangulo = pygame.Rect(posicao[0] * TAMANHO_GRADE, posicao[1] * TAMANHO_GRADE, TAMANHO_GRADE, TAMANHO_GRADE)
            pygame.draw.rect(superficie, self.cor, retangulo)
            pygame.draw.rect(superficie, PRETO, retangulo, 1)
    
    def processar_teclas(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP and self.direcao != (0, 1):
                    self.direcao = (0, -1)
                elif evento.key == pygame.K_DOWN and self.direcao != (0, -1):
                    self.direcao = (0, 1)
                elif evento.key == pygame.K_LEFT and self.direcao != (1, 0):
                    self.direcao = (-1, 0)
                elif evento.key == pygame.K_RIGHT and self.direcao != (-1, 0):
                    self.direcao = (1, 0)

class Comida:
    def __init__(self):
        self.posicao = (0, 0)
        self.cor = VERMELHO
        self.posicao_aleatoria()
    
    def posicao_aleatoria(self):
        self.posicao = (random.randint(0, LARGURA_GRADE - 1), random.randint(0, ALTURA_GRADE - 1))
    
    def desenhar(self, superficie):
        retangulo = pygame.Rect(self.posicao[0] * TAMANHO_GRADE, self.posicao[1] * TAMANHO_GRADE, TAMANHO_GRADE, TAMANHO_GRADE)
        pygame.draw.rect(superficie, self.cor, retangulo)
        pygame.draw.rect(superficie, PRETO, retangulo, 1)

def desenhar_grade(superficie):
    for y in range(0, ALTURA, TAMANHO_GRADE):
        for x in range(0, LARGURA, TAMANHO_GRADE):
            retangulo = pygame.Rect(x, y, TAMANHO_GRADE, TAMANHO_GRADE)
            pygame.draw.rect(superficie, BRANCO, retangulo, 1)

def mostrar_fim_jogo(superficie, pontuacao):
    superficie.fill(PRETO)
    
    fonte_fim_jogo = pygame.font.SysFont('Arial', 50)
    texto_fim_jogo = fonte_fim_jogo.render('Fim de Jogo', True, VERMELHO)
    texto_pontuacao = fonte.render(f'Pontuação Final: {pontuacao}', True, BRANCO)
    texto_reiniciar = fonte.render('Pressione ESPAÇO para reiniciar', True, BRANCO)
    
    superficie.blit(texto_fim_jogo, (LARGURA // 2 - texto_fim_jogo.get_width() // 2, ALTURA // 2 - 50))
    superficie.blit(texto_pontuacao, (LARGURA // 2 - texto_pontuacao.get_width() // 2, ALTURA // 2))
    superficie.blit(texto_reiniciar, (LARGURA // 2 - texto_reiniciar.get_width() // 2, ALTURA // 2 + 50))
    
    pygame.display.update()
    
    aguardando = True
    while aguardando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    aguardando = False

def principal():
    cobra = Cobra()
    comida = Comida()
    pontuacao = 0
    fim_jogo = False
    
    while True:
        if fim_jogo:
            mostrar_fim_jogo(tela, pontuacao)
            cobra.reiniciar()
            comida.posicao_aleatoria()
            pontuacao = 0
            fim_jogo = False
        
        # Processa eventos continuamente
        cobra.processar_teclas()
        
        # Atualiza a posição da cobra
        if not cobra.atualizar():
            fim_jogo = True
            continue
        
        # Verifica se a cobra comeu a comida
        if cobra.obter_posicao_cabeca() == comida.posicao:
            cobra.crescer = True
            comida.posicao_aleatoria()
            pontuacao += 1
        
        # Desenha tudo
        tela.fill(PRETO)
        desenhar_grade(tela)
        cobra.desenhar(tela)
        comida.desenhar(tela)
        
        # Exibe a pontuação
        texto_pontuacao = fonte.render(f'Pontuação: {pontuacao}', True, BRANCO)
        tela.blit(texto_pontuacao, (5, 5))
        
        pygame.display.update()
        relogio.tick(VELOCIDADE)

if __name__ == "__main__":
    principal()