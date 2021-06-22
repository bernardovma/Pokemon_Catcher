import pygame
from pygame.locals import (KEYDOWN,
                           KEYUP,
                           K_LEFT,
                           K_RIGHT,
                           QUIT,
                           K_ESCAPE, K_UP, K_DOWN, K_RCTRL, K_LCTRL, K_p, K_c, K_q, K_BACKSPACE
                           )
from fundo import Fundo
from elementos import ElementoSprite
import random
import os

lista = ['bullbasaur.png', 'charmander.png', 'eevee.png', 'jigglypuff.png', 'snorlax.png', 'squirtle.png', 'pikachu.png']

branco = (255, 255, 255)
preto = (0, 0, 0)
vermelho = (255, 0, 0)
verde = (0, 255, 0)
azul = (16, 4, 28) 
roxo = (153, 51, 153)

class Jogo:
    def __init__(self, size=(1000, 800), fullscreen=False):
        self.elementos = {}
        pygame.init()
        pygame.mixer.music.set_volume(0.1)
        musica_de_fundo = pygame.mixer.music.load('musicas_Pokemon.mp3')
        pygame.mixer.music.play(-1)
        flags = pygame.DOUBLEBUF
        if fullscreen:
            flags |= pygame.FULLSCREEN
        self.tela = pygame.display.set_mode(size, flags=flags, depth=16)
        self.fundo = Fundo()
        self.jogador = None
        self.smallfont = pygame.font.SysFont("Gill Sans MT", 25)
        self.medfont = pygame.font.SysFont("Gill Sans MT", 50)
        self.largefont = pygame.font.SysFont("Segoe UI Black", 75)
        self.interval = 0
        self.nivel = 0
        self.paused = False
        pygame.font.init()
        self.fonte = pygame.font.SysFont('Algerian', 42)


        self.screen_size = self.tela.get_size()
        pygame.mouse.set_visible(0)
        pygame.display.set_caption('Pokémon Catcher')
        self.run = True


    def escreve_placar(self):
        score = self.fonte.render(f'Score: {self.jogador.pontos}', 1, (255, 255, 0), (0, 0, 0))
        self.tela.blit(score, (self.screen_size[0] - 300, 30))

    def manutenção(self):
        r = random.randint(0, 100)
        x = random.randint(1, self.screen_size[0])
        virii = self.elementos["virii"]
        if r > (10 * len(virii)):
            enemy = Virus([0, 0])
            size = enemy.get_size()
            enemy.set_pos([min(max(x, size[0] / 2), self.screen_size[0] - size[0] / 2), size[1] / 2])
            colisores = pygame.sprite.spritecollide(enemy, virii, False)
            if colisores:
                return
            self.elementos["virii"].add(enemy)

    def muda_nivel(self):
        xp = self.jogador.get_pontos()
        if xp > 10 and self.level == 0:
            self.fundo = Fundo("tile2.png")
            self.nivel = 1
            self.jogador.set_lives(self.jogador.get_lives() + 3)
        elif xp > 50 and self.level == 1:
            self.fundo = Fundo("tile3.png")
            self.nivel = 2
            self.jogador.set_lives(self.player.get_lives() + 6)

    def atualiza_elementos(self, dt):
        self.fundo.update(dt)
        for v in self.elementos.values():
            v.update(dt)

    def desenha_elementos(self):
        self.fundo.draw(self.tela)
        for v in self.elementos.values():
            v.draw(self.tela)

    def verifica_impactos(self, elemento, list, action):
        if isinstance(elemento, pygame.sprite.RenderPlain):
            hitted = pygame.sprite.groupcollide(elemento, list, 1, 0)
            for v in hitted.values():
                for o in v:
                    action(o)
            return hitted

        elif isinstance(elemento, pygame.sprite.Sprite):
            if pygame.sprite.spritecollide(elemento, list, 1):
                action()
            return elemento.morto

    def ação_elemento(self):
        self.verifica_impactos(self.jogador, self.elementos["tiros_inimigo"],
                               self.jogador.alvejado)
        if self.jogador.morto:
            self.run = False
            return

        self.verifica_impactos(self.jogador, self.elementos["virii"],
                               self.jogador.colisão)
        if self.jogador.morto:
            self.run = False
            return

        hitted = self.verifica_impactos(self.elementos["tiros"],
                                        self.elementos["virii"],
                                        Virus.alvejado)


        self.jogador.set_pontos(self.jogador.get_pontos() + len(hitted))

    def texto_objetos(self, texto, cor, tamanho):
        if tamanho == "small":
            textsurf = self.smallfont.render(texto, True, cor)
        elif tamanho == "medium":
            textsurf = self.medfont.render(texto, True, cor)
        elif tamanho == "large":
            textsurf = self.largefont.render(texto, True, cor)
        return textsurf, textsurf.get_rect()

    def mensagem(self, msg, cor, y_axis = 0, tamanho = "small", largura = 1000, altura = 800):
        texto_superficie, texto_rect = self.texto_objetos(msg, cor, tamanho)
        texto_rect.center = (largura/2), (altura/2) + y_axis
        self.tela.blit(texto_superficie, texto_rect)

    def pause(self, size = (1000, 800), image = 'space3.jpg'):
        while self.paused:
            event = pygame.event.poll()
            if event.type == KEYDOWN:
                key = event.key
                if key == K_BACKSPACE:
                    self.paused = False
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == KEYDOWN:
                key = event.key
                if key == K_ESCAPE:
                    self.run = False
                    self.paused = False
            bg2 = pygame.image.load(image)
            self.tela.blit(bg2, (0, 0))
            self.mensagem('Jogo Pausado', azul, -250, "large")
            self.mensagem('Aperte Backspace para continuar', branco, -20, "medium")
            self.mensagem('Aperte Esc para sair', branco, 20, "medium")
            pygame.display.update()

    def tela_inicial(self, image = 'space1.jpg', size = (800, 700)):
        self.intro = True
        while self.intro:
            event = pygame.event.poll()
            if event.type == KEYDOWN:
                key = event.key
                if key == K_ESCAPE:
                    self.run = False
                    self.intro = False
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == KEYDOWN:
                key = event.key
                if key == K_p:
                    self.intro = False
            self.tela = pygame.display.set_mode(size)
            bg = pygame.image.load(image)
            self.tela.blit(bg, (0, 0))
            self.mensagem('Pokémon Catcher', branco, -100, "large", 800, 700)
            self.mensagem('Aperte P para jogar', azul, 0, "medium", 800, 700)
            self.mensagem('Aperte Esc para sair', azul, 80, "medium", 800, 700)
            self.mensagem('Aperte Ctrl para atirar Pokebolas', azul, 160, "small", 800, 700)
            self.mensagem('Aperte Backspace para pausar', azul, 200, "small", 800, 700)
            pygame.display.update()

    def trata_eventos(self):
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            self.run = False

        if event.type in (KEYDOWN, KEYUP):
            key = event.key
            if key == K_ESCAPE:
                self.run = False
            elif key in (K_LCTRL, K_RCTRL):
                self.interval = 0
                self.jogador.atira(self.elementos["tiros"])
        if event.type == KEYDOWN:
            key = event.key
            if key == K_UP:
                self.jogador.accel_top()
            elif key == K_DOWN:
                self.jogador.accel_bottom()
            elif key == K_RIGHT:
                self.jogador.accel_right()
            elif key == K_LEFT:
                self.jogador.accel_left()
        if event.type == KEYDOWN:
            if key == K_BACKSPACE:
                self.paused = True

        keys = pygame.key.get_pressed()
        if self.interval > 10:
            self.interval = 0
            if keys[K_RCTRL] or keys[K_LCTRL]:
                self.jogador.atira(self.elementos["tiros"])

    def loop(self, size = (1000, 800)):
        clock = pygame.time.Clock()
        dt = 16
        self.elementos['virii'] = pygame.sprite.RenderPlain(Virus([120, 50]))
        self.jogador = Jogador([200, 400], 5)
        self.elementos['jogador'] = pygame.sprite.RenderPlain(self.jogador)
        self.elementos['tiros'] = pygame.sprite.RenderPlain()
        self.elementos['tiros_inimigo'] = pygame.sprite.RenderPlain()
        self.tela = pygame.display.set_mode(size)
        while self.run:
            clock.tick(1000 / dt)

            self.pause()
            self.trata_eventos()
            self.ação_elemento()
            self.manutenção()
            # Atualiza Elementos
            self.atualiza_elementos(dt)

            # Desenhe no back buffer
            self.desenha_elementos()
            self.escreve_placar()
            # texto = self.fonte.render(f"Vidas: {self.jogador.get_lives()}", True, (255, 255, 255), (0, 0, 0))

            pygame.display.flip()


class Nave(ElementoSprite):
    def __init__(self, position, lives=0, speed=[0, 0], image=None, new_size=[100, 110]):
        self.acceleration = [3, 3]
        if not image:
            image = "celular.png"
        super().__init__(image, position, speed, new_size)
        self.set_lives(lives)

    def get_lives(self):
        return self.lives

    def set_lives(self, lives):
        self.lives = lives

    def colisão(self):
        if self.get_lives() <= 0:
            self.kill()
        else:
            self.set_lives(self.get_lives() - 1)

    def atira(self, lista_de_tiros, image=None):
        s = list(self.get_speed())
        s[1] *= 2
        Tiro(self.get_pos(), s, image, lista_de_tiros)

    def alvejado(self):
        if self.get_lives() <= 0:
            self.kill()
        else:
            self.set_lives(self.get_lives() - 1)

    @property
    def morto(self):
        return self.get_lives() == 0

    def accel_top(self):
        speed = self.get_speed()
        self.set_speed((speed[0], speed[1] - self.acceleration[1]))

    def accel_bottom(self):
        speed = self.get_speed()
        self.set_speed((speed[0], speed[1] + self.acceleration[1]))

    def accel_left(self):
        speed = self.get_speed()
        self.set_speed((speed[0] - self.acceleration[0], speed[1]))

    def accel_right(self):
        speed = self.get_speed()
        self.set_speed((speed[0] + self.acceleration[0], speed[1]))



class Virus(Nave):
    def __init__(self, position, lives=None, speed=None, image=None, size=(50, 50)):
        if not image:
            image = random.choice(lista)
            if image == 'pikachu.png':
                lives=3
            else:
                lives=1
        super().__init__(position, lives, speed, image, size)


class Jogador(Nave):

    def __init__(self, position, lives=10, image=None, new_size=[100, 110]):
        if not image:
            image = "celular.png"
        super().__init__(position, lives, [0, 0], image, new_size)
        self.pontos = 0

    def update(self, dt):
        move_speed = (self.speed[0] * dt / 16,
                      self.speed[1] * dt / 16)
        self.rect = self.rect.move(move_speed)

        if (self.rect.right > self.area.right):
            self.rect.right = self.area.right

        elif (self.rect.left < 0):
            self.rect.left = 0

        if (self.rect.bottom > self.area.bottom):
            self.rect.bottom = self.area.bottom

        elif (self.rect.top < 0):
            self.rect.top = 0

    def get_pos(self):
        return (self.rect.center[0], self.rect.top)

    def get_pontos(self):
        return self.pontos

    def set_pontos(self, pontos):
        self.pontos = pontos

    def atira(self, lista_de_tiros, image=None):
        l = 1
        if self.pontos > 250:
            l = 2

        p = self.get_pos()
        speeds = self.get_fire_speed(l)
        for s in speeds:
            Tiro(p, s, image, lista_de_tiros)

    def get_fire_speed(self, shots):
        speeds = []

        if shots <= 0:
            return speeds

        if shots == 1:
            speeds += [(0, -5)]

        if shots > 1 and shots <= 3:
            speeds += [(0, -5)]
            speeds += [(-2, -3)]
            speeds += [(2, -3)]

        if shots > 3 and shots <= 5:
            speeds += [(0, -5)]
            speeds += [(-2, -3)]
            speeds += [(2, -3)]
            speeds += [(-4, -2)]
            speeds += [(4, -2)]

        return speeds


class Tiro(ElementoSprite):
    def __init__(self, position, speed=None, image=None, list=None, new_size = [35, 35]):
        if not image:
            image = "Pokemon.png"
        super().__init__(image, position, speed, new_size)
        if list is not None:
            self.add(list)


if __name__ == '__main__':
    J = Jogo(fullscreen=False)
    J.tela_inicial()
    J.loop()