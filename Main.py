import math

import pygame
import sys
import os
from settings import *
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Golden Diver")
clock = pygame.time.Clock()

# Sprite class
class Diver(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pos = pygame.math.Vector2(PLAYER_START_X,PLAYER_START_Y)
        self.image = pygame.transform.rotozoom(pygame.image.load("Sprites/diver_idle/Diver1.png").convert_alpha(),0, PLAYERSIZE)
        self.base_image = self.image
        self.hitbox_rect = self.base_image.get_rect(center = self.pos)
        self.rect = self.hitbox_rect.copy()
    def diver_rotation(self):
        self.chords = pygame.mouse.get_pos()
        self.x_change_mouse = (self.chords[0] - self.hitbox_rect.centerx)
        self.y_change_mouse = (self.chords[1] - self.hitbox_rect.centery)
        self.angle = math.degrees(math.atan2(self.y_change_mouse, self.x_change_mouse))
        self.image = pygame.transform.rotate(self.base_image, -self.angle)
        self.rect = self.image.get_rect(center=self.hitbox_rect.center)
    def user_input(self):
        self.velocity_x = 0
        self.velocity_y = 0

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.velocity_y = - SPEED
        if keys[pygame.K_s]:
            self.velocity_y = SPEED
        if keys[pygame.K_d]:
            self.velocity_x = SPEED
        if keys[pygame.K_a]:
            self.velocity_x = - SPEED
        # Diagonal movemnt ikke er hurtigere.
        if self.velocity_x != 0 and self.velocity_y != 0:
            self.velocity_x /= math.sqrt(2)
            self.velocity_y /= math.sqrt(2)

    def move(self):
        self.pos += pygame.math.Vector2(self.velocity_x, self.velocity_y)
        self.hitbox_rect.center = self.pos
        self.rect.center = self.hitbox_rect.center
    def update(self):
        self.user_input()
        self.move()
        self.diver_rotation()

diver = Diver()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(WHITE)
    diver.update()
    clock.tick(FPS)
    screen.blit(diver.image, diver.pos)
    pygame.display.update()


pygame.quit()
sys.exit()
