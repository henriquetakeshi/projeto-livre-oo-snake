import pygame
import random
import time
import sys
from abc import ABC, abstractmethod

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

# Mixins
class Renderizavel:
    def desenhar(self, superficie):
        raise NotImplementedError("Método desenhar deve ser implementado")

class Movivel:
    def mover(self):
        raise NotImplementedError("Método mover deve ser implementado")

# Classe base abstrata
class Entidade(ABC):
    def __init__(self, posicao, cor):
        self.posicao = posicao
        self.cor = cor

    @abstractmethod
    def atualizar(self):
        pass

    @abstractmethod
    def desenhar(self, superficie):
        pass

# Classe para segmentos da cobra (Composição forte)
class Segmento:
    def __init__(self, posicao):
        self.posicao = posicao

# Classe para efeitos sonoros (Associação fraca)
class EfeitoSonoro:
    def __init__(self):
        self.som_comida = None
        self.som_game_over = None
        self.carregar_sons()

    def carregar_sons(self):
        # Aqui você pode adicionar sons reais
        pass

    def tocar_comida(self):
        if self.som_comida:
            self.som_comida.play()

    def tocar_game_over(self):
        if self.som_game_over:
            self.som_game_over.play()

# Classe para o placar (Associação fraca)
class Placar:
    def __init__(self):
        self.pontuacao = 0
        self.fonte = pygame.font.SysFont('Arial', 25)

    def incrementar(self):
        self.pontuacao += 1

    def resetar(self):
        self.pontuacao = 0

    def desenhar(self, superficie):
        texto = self.fonte.render(f'Pontuação: {self.pontuacao}', True, BRANCO)
        superficie.blit(texto, (5, 5))

class Cobra(Entidade, Renderizavel, Movivel):
    def __init__(self):
        super().__init__((LARGURA_GRADE // 2, ALTURA_GRADE // 2), VERDE)
        self.segmentos = [Segmento(self.posicao)]  # Composição forte
        self.direcao = (1, 0)
        self.crescer = False
        self.efeito_sonoro = EfeitoSonoro()  # Associação fraca

    def obter_posicao_cabeca(self):
        return self.segmentos[0].posicao

    def mover(self):
        cabeca = self.obter_posicao_cabeca()
        x, y = self.direcao
        nova_posicao = ((cabeca[0] + x) % LARGURA_GRADE, (cabeca[1] + y) % ALTURA_GRADE)
        return nova_posicao

    def atualizar(self):
        nova_posicao = self.mover()
        
        # Game over se a cobra colidir com ela mesma
        if nova_posicao in [seg.posicao for seg in self.segmentos[1:]]:
            self.efeito_sonoro.tocar_game_over()
            return False
        
        self.segmentos.insert(0, Segmento(nova_posicao))
        
        if not self.crescer:
            self.segmentos.pop()
        else:
            self.crescer = False
            self.efeito_sonoro.tocar_comida()
        
        return True

    def desenhar(self, superficie):
        for segmento in self.segmentos:
            retangulo = pygame.Rect(segmento.posicao[0] * TAMANHO_GRADE, 
                                  segmento.posicao[1] * TAMANHO_GRADE, 
                                  TAMANHO_GRADE, TAMANHO_GRADE)
            pygame.draw.rect(superficie, self.cor, retangulo)
            pygame.draw.rect(superficie, PRETO, retangulo, 1)

    def reiniciar(self):
        self.segmentos = [Segmento((LARGURA_GRADE // 2, ALTURA_GRADE // 2))]
        self.direcao = (1, 0)
        self.crescer = False

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

class Comida(Entidade, Renderizavel):
    def __init__(self):
        super().__init__((0, 0), VERMELHO)
        self.posicao_aleatoria()

    def posicao_aleatoria(self):
        self.posicao = (random.randint(0, LARGURA_GRADE - 1), 
                       random.randint(0, ALTURA_GRADE - 1))

    def atualizar(self):
        pass  # A comida não precisa de atualização

    def desenhar(self, superficie):
        retangulo = pygame.Rect(self.posicao[0] * TAMANHO_GRADE, 
                              self.posicao[1] * TAMANHO_GRADE, 
                              TAMANHO_GRADE, TAMANHO_GRADE)
        pygame.draw.rect(superficie, self.cor, retangulo)
        pygame.draw.rect(superficie, PRETO, retangulo, 1)

class Jogo:
    def __init__(self):
        self.cobra = Cobra()  # Composição forte
        self.comida = Comida()  # Composição forte
        self.placar = Placar()  # Associação fraca
        self.fim_jogo = False

    def desenhar_grade(self, superficie):
        for y in range(0, ALTURA, TAMANHO_GRADE):
            for x in range(0, LARGURA, TAMANHO_GRADE):
                retangulo = pygame.Rect(x, y, TAMANHO_GRADE, TAMANHO_GRADE)
                pygame.draw.rect(superficie, BRANCO, retangulo, 1)

    def mostrar_fim_jogo(self, superficie):
        superficie.fill(PRETO)
        
        fonte_fim_jogo = pygame.font.SysFont('Arial', 50)
        texto_fim_jogo = fonte_fim_jogo.render('Fim de Jogo', True, VERMELHO)
        texto_pontuacao = fonte.render(f'Pontuação Final: {self.placar.pontuacao}', True, BRANCO)
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

    def executar(self):
        while True:
            if self.fim_jogo:
                self.mostrar_fim_jogo(tela)
                self.cobra.reiniciar()
                self.comida.posicao_aleatoria()
                self.placar.resetar()
                self.fim_jogo = False
            
            # Processa eventos continuamente
            self.cobra.processar_teclas()
            
            # Atualiza a posição da cobra
            if not self.cobra.atualizar():
                self.fim_jogo = True
                continue
            
            # Verifica se a cobra comeu a comida
            if self.cobra.obter_posicao_cabeca() == self.comida.posicao:
                self.cobra.crescer = True
                self.comida.posicao_aleatoria()
                self.placar.incrementar()
            
            # Desenha tudo
            tela.fill(PRETO)
            self.desenhar_grade(tela)
            self.cobra.desenhar(tela)
            self.comida.desenhar(tela)
            self.placar.desenhar(tela)
            
            pygame.display.update()
            relogio.tick(VELOCIDADE)

if __name__ == "__main__":
    jogo = Jogo()
    jogo.executar()