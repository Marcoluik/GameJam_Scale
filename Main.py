import math

import pygame
import sys
import os
from settings import *
import numpy as np
import random
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Golden Diver")
clock = pygame.time.Clock()
diver_images = []
bullet_image = pygame.image.load("Sprites/Bullets/HARPOON.png")
enemy_images = []
weapon_images = []
weapon_reload_images = []

def image_load():
    for i in range(1,15):
        image = pygame.image.load(f"Sprites/Diver_idle_ver2/Diver_idle_ver{i}.png")
        scaled_image = pygame.transform.scale(image, (
        HEIGHT/6, HEIGHT/6))
        diver_images.append(scaled_image)

    for i in range(1, 13):
        image = pygame.image.load(f"Sprites/Harpoon/Harpoon_idle/Harpooon_idle{i}.png")
        scaled_image = pygame.transform.scale(image, (HEIGHT/6, HEIGHT/6))
        weapon_images.append(scaled_image)


    for i in range(1, 14):
        image = pygame.image.load(f"Sprites/Harpoon/Harpoon_reload/Harpoon_reload{i}.png")
        scaled_image = pygame.transform.scale(image, (HEIGHT/6, HEIGHT/6))
        weapon_reload_images.append(scaled_image)


    for i in range(1, 11):
        image = pygame.image.load(f"Sprites/Enemy/Enemy{i}.png")
        scaled_image = pygame.transform.scale(image, (HEIGHT/6, HEIGHT/6))
        enemy_images.append(scaled_image)
# Sprite class
class Diver(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pos = pygame.math.Vector2(PLAYER_START_X, PLAYER_START_Y)
        self.diver_images = diver_images  # Assign loaded images
        self.unrotated_image = self.diver_images[0]  # Initialize with the first image
        self.image = self.unrotated_image
        self.base_image = self.unrotated_image
        self.hitbox_rect = self.base_image.get_rect(center=self.pos)
        self.rect = self.hitbox_rect.copy()
        self.shoot_cooldown = 0
        self.animation_speed = 5
        self.animation_frame = 0
        self.animation_timer = 0

    def animate(self):
        # Update the animation frame based on the animation speed
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % len(self.diver_images)
            self.unrotated_image = self.diver_images[self.animation_frame]
            self.image = pygame.transform.rotate(self.unrotated_image, -self.angle)
            self.rect = self.image.get_rect(center=self.hitbox_rect.center)
    def diver_rotation(self):
        self.chords = pygame.mouse.get_pos()
        self.x_change_mouse = (self.chords[0] - self.hitbox_rect.centerx)
        self.y_change_mouse = (self.chords[1] - self.hitbox_rect.centery)
        self.angle = math.degrees(math.atan2(self.y_change_mouse, self.x_change_mouse))
        self.image = pygame.transform.rotate(self.unrotated_image, -self.angle)
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

        if pygame.mouse.get_pressed() == (1,0,0) or keys[pygame.K_SPACE]:
            self.shoot = True
            self.is_shooting()
        else:
            self.shoot = False
    def is_shooting(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = SHOOT_COOLDOWN
            bullet_start_pos = self.pos
            self.bullet = Bullet(bullet_start_pos[0],bullet_start_pos[1],self.angle)
            print(self.angle)
            bullet_group.add(self.bullet)
            all_sprites_group.add(self.bullet)
    def move(self):
        self.pos += pygame.math.Vector2(self.velocity_x, self.velocity_y)
        self.hitbox_rect.center = self.pos
        self.rect.center = self.hitbox_rect.center

    def update(self):
        self.user_input()
        self.move()
        self.diver_rotation()
        self.animate()

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

class Tiles(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        tile_size = 32
        rows = HEIGHT // tile_size + 1
        cols = WIDTH // tile_size + 1
        self.tiles = []
        for i in range(cols):
            for k in range(rows):
                tile_chords = (i*tile_size, k*tile_size)
                tile_rect = pygame.Rect(tile_chords[0], tile_chords[1], tile_size, tile_size)
                # Calculate the depth based on the position
                offset = random.randint(-20, 20)  # Adjust the offset range as needed
                depth = (HEIGHT - tile_chords[1]) / HEIGHT * 255 + offset # Deeper areas are closer to the bottom
                depth = max(0, min(235, depth))
                # Calculate the color based on depth
                if depth < 50:
                    tile_color = (0, depth, 0)  # Darker green for seagrass
                else:

                    tile_color = (0, 0, depth)  # Lighter blue for water


                tile = {"rect": tile_rect, "color": tile_color}
                self.tiles.append(tile)
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.image = pygame.image.load("Sprites/Bullets/HARPOON.png").convert_alpha()
        self.base_image = pygame.transform.rotozoom(self.image, 0, BULLET_SCALE)
        self.angle = angle
        self.image = pygame.transform.rotate(self.base_image, -self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x = x
        self.y = y
        self.time = 0
        self.speed = BULLET_SPEED
        #angle convert to radians by, 2*pi/360
        self.x_velocity = math.cos(self.angle * (2*math.pi/360)) * self.speed
        self.y_velocity = math.sin(self.angle * (2 * math.pi / 360)) * self.speed

    def bullet_movement(self):
        self.x += self.x_velocity
        self.y += self.y_velocity

        #Conbert to int
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def update(self):
        self.bullet_movement()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__()
        self.diver_x = x
        self.diver_y = y
        self.type = type
        self.angle = math.degrees(math.atan2(self.diver_x, self.diver_y))
        self.image = pygame.image.load("Sprites/Bullets/HARPOON.png").convert_alpha()
        self.base_image = pygame.transform.rotozoom(self.image, 0, BULLET_SCALE)
        self.image = pygame.transform.rotate(self.base_image, -self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.diver_x+ 100, self.diver_y+ 100)

    def move(self):
        # Calculate the angle to the diver's position
        dx = self.diver_x - self.x
        dy = self.diver_x - self.y
        angle = math.atan2(dy, dx)
        angle = math.degrees(angle)

        # Calculate the new position based on the angle and a speed factor
        speed = 2  # Adjust the speed as needed
        self.x += speed * math.cos(math.radians(angle))
        self.y += speed * math.sin(math.radians(angle))

        # Update the sprite's position
        self.rect.center = (self.x, self.y)
    def update(self):
        self.move()

image_load()
diver = Diver()
tiles = Tiles()

all_sprites_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
all_sprites_group.add(diver)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    for tile_data in tiles.tiles:
        pygame.draw.rect(screen, tile_data["color"], tile_data["rect"])
    #hitbox check
    #pygame.draw.rect(screen, "red", diver.hitbox_rect, width=2)
    #pygame.draw.rect(screen, "yellow", diver.rect, width=2)
    clock.tick(FPS)
    all_sprites_group.draw(screen)
    all_sprites_group.update()
    pygame.display.update()


pygame.quit()
sys.exit()
