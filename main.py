# ==========================================
# Title:  Tron
# Author: Megaterion
# ==========================================

import sys
import pygame
import os
from pygame.locals import *


class Player:
    def __init__(self, x, y, b, c):
        self.x = x  # x-Pos
        self.y = y  # y-Pos
        self.speed = 1  # Geschwindigkeit
        self.bearing = b  # Ausrichtung
        self.colour = c
        self.boost = False
        self.lasercount = True
        self.boostlimit = 300
        self.rect = pygame.Rect(self.x, self.y, 2, 2)

        self.i = False
        self.j = 0

    def move(self):
        self.x += self.bearing[0]
        self.y += self.bearing[1]

    def draw(self):
        self.rect = pygame.Rect(self.x, self.y, 2, 2)
        pygame.draw.rect(WIN, self.colour, self.rect, 0)

    def coll(self):
        if self.rect.collidelist(wall_rects) > -1 or self.rect.collidelist(path) > -1:
            pygame.mixer.Sound.play(crash_sound)
            objects.remove(self)
            if len(objects) == 1:
                if objects[0].colour == P1_COLOUR:
                    player_score[0] += 1
                    lost_label = lost_font.render("Spieler 1 gewinnt!", 1, (255, 255, 255))
                    WIN.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2, 350))

                elif objects[0].colour == P2_COLOUR:
                    player_score[1] += 1
                    lost_label = lost_font.render("Spieler 2 gewinnt!", 1, (255, 255, 255))
                    WIN.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2, 350))

                elif objects[0].colour == P3_COLOUR:
                    player_score[2] += 1
                    lost_label = lost_font.render("Spieler 3 gewinnt!", 1, (255, 255, 255))
                    WIN.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2, 350))

                objects.clear()
                las.clear()
                path.clear()
                path_colour.clear()
                pygame.display.update()
                pygame.time.wait(1500)
                summonPlayer()

        else:
            path.append(self.rect)
            path_colour.append(self.colour)

    def shoot(self):
        if self.lasercount:
            self.lasercount = False
            laser = Laser(self.x, self.y, self.bearing)
            las.append(laser)
            pygame.mixer.Sound.play(laser_sound)


class Laser:
    def __init__(self, x, y, b):
        self.x = x
        self.y = y
        self.bearing = b
        self.colour = WHITE
        self.rect = pygame.Rect(self.x - 3, self.y - 3, 6, 6)

    def move(self):
        self.x += self.bearing[0]
        self.y += self.bearing[1]

    def draw(self):
        self.rect = pygame.Rect(self.x - 3, self.y - 3, 6, 6)
        pygame.draw.rect(WIN, self.colour, self.rect, 0)

    def coll(self):
        if self.rect.collidelist(wall_rects) > -1:
            las.remove(self)
        for p in range(len(path) - 2):
            if self.rect.colliderect(path[p]):
                path.remove(path[p])
                path_colour.remove(path_colour[p])


def summonPlayer():
    p1 = Player(WIDTH / 3, (HEIGHT - offset) / 2, (2, 0), P1_COLOUR)
    p2 = Player((WIDTH / 3) * 2, (HEIGHT - offset) / 2, (-2, 0), P2_COLOUR)
    objects.append(p1)
    objects.append(p2)

    if player_count >= 3:
        p3 = Player(WIDTH / 2, HEIGHT * 0.75, (0, -2), P3_COLOUR)
        objects.append(p3)


def main_menu():
    pygame.mixer.music.load(menu_music)
    pygame.mixer.music.play(-1)

    click = False

    while True:
        WIN.blit(BG, (0, 0))

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(WIDTH * 0.41, HEIGHT * 0.58, WIDTH * 0.18, HEIGHT * 0.06)
        button_2 = pygame.Rect(WIDTH * 0.375, HEIGHT * 0.71, WIDTH * 0.245, HEIGHT * 0.06)
        button_3 = pygame.Rect(WIDTH * 0.43, HEIGHT * 0.837, WIDTH * 0.14, HEIGHT * 0.05)

        if button_1.collidepoint((mx, my)):
            if click:
                game()
        if button_2.collidepoint((mx, my)):
            if click:
                options()
        if button_3.collidepoint((mx, my)):
            if click:
                pygame.quit()
                sys.exit()

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(FPS)


def game():
    global boost1, boost2, boost3
    running = True

    while running:
        pygame.mixer.music.load(game_music)
        pygame.mixer.music.play(-1)

        game = True
        objects.clear()
        las.clear()
        path.clear()
        path_colour.clear()
        summonPlayer()

        while game:
            for event in pygame.event.get():  # alle events im letzten tick
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYUP:
                    for o in objects:
                        # Player 1
                        if o.colour == P1_COLOUR and event.key == pygame.K_TAB:
                            o.boost = False
                        # Player 2
                        if o.colour == P2_COLOUR and event.key == pygame.K_RSHIFT:
                            o.boost = False
                        # Player 3
                        if o.colour == P3_COLOUR and event.key == pygame.K_u:
                            o.boost = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game = False
                        running = False

                        pygame.mixer.music.load(menu_music)
                        pygame.mixer.music.play(-1)

                    for o in objects:
                        # Player 1
                        if o.colour == P1_COLOUR:
                            if event.key == pygame.K_w and o.bearing != (0, 2):
                                o.bearing = (0, -2)
                            elif event.key == pygame.K_s and o.bearing != (0, -2):
                                o.bearing = (0, 2)
                            elif event.key == pygame.K_a and o.bearing != (2, 0):
                                o.bearing = (-2, 0)
                            elif event.key == pygame.K_d and o.bearing != (-2, 0):
                                o.bearing = (2, 0)
                            elif event.key == pygame.K_q:
                                o.boost = True
                            elif event.key == pygame.K_TAB:
                                o.shoot()

                        # Player 2
                        elif o.colour == P2_COLOUR:
                            if event.key == pygame.K_UP and o.bearing != (0, 2):
                                o.bearing = (0, -2)
                            elif event.key == pygame.K_DOWN and o.bearing != (0, -2):
                                o.bearing = (0, 2)
                            elif event.key == pygame.K_LEFT and o.bearing != (2, 0):
                                o.bearing = (-2, 0)
                            elif event.key == pygame.K_RIGHT and o.bearing != (-2, 0):
                                o.bearing = (2, 0)
                            elif event.key == pygame.K_RSHIFT:
                                o.boost = True
                            elif event.key == pygame.K_MINUS:
                                o.shoot()

                        # Player 3
                        elif o.colour == P3_COLOUR:
                            if event.key == pygame.K_i and o.bearing != (0, 2):
                                o.bearing = (0, -2)
                            elif event.key == pygame.K_k and o.bearing != (0, -2):
                                o.bearing = (0, 2)
                            elif event.key == pygame.K_j and o.bearing != (2, 0):
                                o.bearing = (-2, 0)
                            elif event.key == pygame.K_l and o.bearing != (-2, 0):
                                o.bearing = (2, 0)
                            elif event.key == pygame.K_u:
                                o.boost = True
                            elif event.key == pygame.K_z:
                                o.shoot()

            WIN.fill(BLACK)  # leert das Fensteer

            for w in wall_rects:
                pygame.draw.rect(WIN, (42, 42, 42), w, 0)  # Mauer erzeugen

            for p in range(len(path)):
                pygame.draw.rect(WIN, path_colour[p], path[p], 0)

            for l in las:
                l.move()
                l.draw()
                l.coll()

            for o in objects:
                if o.boost:
                    if o.boostlimit - 1 >= 0:
                        o.boostlimit = o.boostlimit - 1
                        o.speed = 2
                    else:
                        o.boost = False
                else:
                    o.speed = 1
                    if o.j != 20:
                        o.j = o.j + 1
                    else:
                        if o.boostlimit + 1 <= 300:
                            o.boostlimit = o.boostlimit + 1
                        o.j = 0

                if o.speed == 1:
                    if o.i:
                        o.move()
                        o.draw()
                        o.coll()
                        o.i = False
                    else:
                        o.i = True
                elif o.speed == 2:
                    o.move()
                    o.draw()
                    o.coll()

            if o.colour == P1_COLOUR:
                boost1 = o.boostlimit
            elif o.colour == P2_COLOUR:
                boost2 = o.boostlimit
            elif o.colour == P3_COLOUR:
                boost3 = o.boostlimit

            # Anzeige für 2 Spieler
            if player_count == 2:
                # zeigt die verbleibende Boostdauer an
                boost_text = boost_font.render('{0}                           {1}'.format(boost1, boost2), 1, (255, 153, 51))
                boost_text_pos = boost_text.get_rect()
                boost_text_pos.centerx = int(WIDTH / 2)
                boost_text_pos.centery = int(offset / 2)
                WIN.blit(boost_text, boost_text_pos)

                # Zeigt den aktuellen score an
                score_text = font.render('{0} : {1}'.format(player_score[0], player_score[1]), 1, (255, 153, 51))
                score_text_pos = score_text.get_rect()
                score_text_pos.centerx = int(WIDTH / 2)
                score_text_pos.centery = int(offset / 2)
                WIN.blit(score_text, score_text_pos)

            # Anzeige für 3 Spieler
            if player_count == 3:

                # zeigt die verbleibende Boostdauer an
                boost_text = boost_font.render('{0}       {1}     {2}'.format(boost1, boost2, boost3), 1, (255, 153, 51))
                boost_text_pos = boost_text.get_rect()
                boost_text_pos.centerx = int(WIDTH / 2)
                boost_text_pos.centery = int(offset / 2)
                WIN.blit(boost_text, boost_text_pos)

                # Zeigt den aktuellen score an
                score_text = font.render('{0} : {1} : {2}'.format(player_score[0], player_score[1], player_score[2]), 1,
                                         (255, 153, 51))
                score_text_pos = score_text.get_rect()
                score_text_pos.centerx = int(WIDTH / 2)
                score_text_pos.centery = int(offset / 2)
                WIN.blit(score_text, score_text_pos)

            pygame.display.flip()
            mainClock.tick(FPS)

        pygame.display.update()


def options():
    running = True
    while running:
        WIN.fill(BLACK)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        pygame.display.update()
        mainClock.tick(FPS)


###############

mainClock = pygame.time.Clock()
FPS = 120
pygame.init()

WIN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("TRON")
surface = pygame.display.get_surface()
WIDTH, HEIGHT = surface.get_width(), surface.get_height()
offset = 60

boost_font = pygame.font.SysFont(None, 36)
font = pygame.font.SysFont(None, 72)
lost_font = pygame.font.SysFont(None, 60)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255, 255)
P1_COLOUR = (0, 255, 255)
P2_COLOUR = (255, 187, 39)
P3_COLOUR = (210, 0, 3)

player_count = 3
player_score = [0, 0, 0]

path = []  # Liste mit allen Pfadteilen
path_colour = []  # Liste mit Farben der Pfadteile
objects = []  # Liste mit allen Playern
las = []  # Liste mit allen Lasern

wall_rects = [pygame.Rect([0, offset, 15, HEIGHT]),  # links
              pygame.Rect([0, offset, WIDTH, 15]),  # oben
              pygame.Rect([WIDTH - 15, offset, 15, HEIGHT]),  # rechts
              pygame.Rect([0, HEIGHT - 15, WIDTH, 15])  # unten
              ]

BG = pygame.transform.scale(pygame.image.load(os.path.join("Tron_Assets/Tron_Titlescreen.png")), (WIDTH, HEIGHT))
menu_music = "Tron_Assets/Tron_menu.mp3"
game_music = "Tron_Assets/Lightcycle_Race.mp3"
crash_sound = pygame.mixer.Sound("Tron_Assets/Crash_sound.mp3")
laser_sound = pygame.mixer.Sound("Tron_Assets/Laser_sound.mp3")

###############
main_menu()
