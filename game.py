import pygame
import random
import math
from enum import Enum

pygame.init()

LARGURA = 800
ALTURA = 600
FPS = 60
VELOCIDADE_RATO = 4
PONTOS_MAXIMOS = 20

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (0, 200, 0)
AMARELO = (255, 255, 0)

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Rato e Queijo")
relogio = pygame.time.Clock()
fonte = pygame.font.Font(None, 36)
fonte_grande = pygame.font.Font(None, 72)

class Rato:
    def __init__(self):
        self.raio = 15
        self.x = LARGURA // 2
        self.y = ALTURA // 2
        try:
            self.imagem = pygame.image.load("rato.png")
            self.imagem = pygame.transform.scale(self.imagem, (40, 40))
        except:
            self.imagem = None
    
    def desenhar(self, superficie):
        if self.imagem:
            rect = self.imagem.get_rect(center=(int(self.x), int(self.y)))
            superficie.blit(self.imagem, rect)
        else:
            pygame.draw.circle(superficie, (150, 150, 150), (int(self.x), int(self.y)), self.raio)
    
    def mover_para(self, alvo_x, alvo_y):
        dx = alvo_x - self.x
        dy = alvo_y - self.y
        distancia = math.sqrt(dx**2 + dy**2)
        
        if distancia > 0:
            self.x += (dx / distancia) * VELOCIDADE_RATO
            self.y += (dy / distancia) * VELOCIDADE_RATO
        
        self.x = max(self.raio, min(LARGURA - self.raio, self.x))
        self.y = max(self.raio, min(ALTURA - self.raio, self.y))
    
    def colide_com(self, queijo):
        distancia = math.sqrt((self.x - queijo.x)**2 + (self.y - queijo.y)**2)
        return distancia < self.raio + queijo.raio

class Queijo:
    def __init__(self):
        self.raio = 12
        self.x = random.randint(self.raio + 50, LARGURA - self.raio - 50)
        self.y = random.randint(self.raio + 50, ALTURA - self.raio - 50)
        try:
            self.imagem = pygame.image.load("queijo.png")
            self.imagem = pygame.transform.scale(self.imagem, (40, 40))
        except:
            self.imagem = None
    
    def desenhar(self, superficie):
        if self.imagem:
            rect = self.imagem.get_rect(center=(int(self.x), int(self.y)))
            superficie.blit(self.imagem, rect)
        else:
            pygame.draw.circle(superficie, AMARELO, (int(self.x), int(self.y)), self.raio)
    
    def reaparecer(self):
        self.x = random.randint(self.raio + 50, LARGURA - self.raio - 50)
        self.y = random.randint(self.raio + 50, ALTURA - self.raio - 50)

def desenhar_pontos(superficie, pontos):
    texto = fonte.render(f"Pontos: {pontos} / {PONTOS_MAXIMOS}", True, PRETO)
    superficie.blit(texto, (10, 10))

def desenhar_vitoria(superficie):
    texto = fonte_grande.render("VOCÊ VENCEU!", True, VERDE)
    rect = texto.get_rect(center=(LARGURA // 2, ALTURA // 2 - 50))
    superficie.blit(texto, rect)
    
    texto_restart = fonte.render("Pressione R para recomeçar", True, PRETO)
    rect_restart = texto_restart.get_rect(center=(LARGURA // 2, ALTURA // 2 + 50))
    superficie.blit(texto_restart, rect_restart)

def main():
    rato = Rato()
    queijo = Queijo()
    pontos = 0
    vitoria = False
    
    executando = True
    while executando:
        relogio.tick(FPS)
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r and vitoria:
                    pontos = 0
                    vitoria = False
                    rato = Rato()
                    queijo = Queijo()
        
        if not vitoria:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            rato.mover_para(mouse_x, mouse_y)
            
            if rato.colide_com(queijo):
                pontos += 1
                queijo.reaparecer()
                
                if pontos >= PONTOS_MAXIMOS:
                    vitoria = True
        
        tela.fill(BRANCO)
        rato.desenhar(tela)
        queijo.desenhar(tela)
        desenhar_pontos(tela, pontos)
        
        if vitoria:
            desenhar_vitoria(tela)
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()
