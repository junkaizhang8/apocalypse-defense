import pygame
import sys
import time
import random

class Zombie(pygame.sprite.Sprite):
    def __init__(self,image,x_value,y_value,x_change,health):
        pygame.sprite.Sprite.__init__(self)
        self.x_value = x_value
        self.y_value = y_value
        self.x_change = x_change
        self.health = health
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.center = [x_value,y_value]
        
    def update(self):
        self.x_value = self.x_value + self.x_change
        self.rect.center = (self.x_value, self.y_value)
        if self.x_value <= 300 or self.health <= 0:
            self.kill()
        

class Bullet(Zombie):
    def __init__(self,image,x_value,y_value,x_change,damage):
        super().__init__(image,x_value,y_value,x_change,damage)
    def update(self):
        self.x_value = self.x_value + self.x_change
        self.rect.center = (self.x_value, self.y_value)
        if self.x_value > 1000:
            self.kill()
        
def spriteLocation(sprite_image, x,y):
    screen.blit(sprite_image, (x,y))

def bulletReadyCheck():
    global bullet_start_time, damage
    current_time = pygame.time.get_ticks()
    delta_time = current_time - bullet_start_time
    if delta_time > 300:
        bullet_x_coordinate = character_x_coordinate + 120
        bullet_y_coordinate = character_y_coordinate + 50
        bullet_speed = 12
        spawned_bullet = Bullet("bullet 1.png", bullet_x_coordinate, bullet_y_coordinate, bullet_speed, damage)
        bullet_group.add(spawned_bullet)
        bullet_start_time = current_time
        
def zombieSpawnCheck():
    global zombie_start_time, number_of_zombies
    current_time = pygame.time.get_ticks()
    delta_time = current_time - zombie_start_time
    if delta_time > 800 and number_of_zombies < 10:
        number_of_zombies += 1
        zombie_x_coordinate = 1050
        zombie_y_coordinate = random.randrange(155,436,70)
        horizontal_change = -1
        #health_points = 40
        spawned_zombie = Zombie("basic zombie.png", zombie_x_coordinate, zombie_y_coordinate, horizontal_change, health_points)
        zombie_group.add(spawned_zombie)
        zombie_start_time = current_time

def healthBar(x_value, y_value, full_health, current_health):
    black = (0,0,0)
    red = (255,0,0)
    green = (0,255,0)
    pygame.draw.rect(screen,black,[x_value - 37, y_value - 52, 52, 7])
    pygame.draw.rect(screen,red,[x_value - 35, y_value - 50, 50,5])
    pygame.draw.rect(screen,green,[x_value - 35, y_value - 50, current_health * (50 / full_health),5])

pygame.init()

character_image = pygame.image.load("character.png")
character_x_coordinate = 50
character_y_coordinate = 240

bullet_image = pygame.image.load("bullet 1.png")
bullet_image = bullet_image.get_rect()

shield_image = pygame.image.load("shield.png")

number_of_zombies = 0

screen = pygame.display.set_mode((1000,600))

pygame.display.set_caption("Apocalypse Defense")

clock = pygame.time.Clock()
bullet_start_time = pygame.time.get_ticks()
zombie_start_time = pygame.time.get_ticks()

zombie_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()

damage = 10
health_points = 40
flag = True
while flag:
    
    clock.tick(60)
    screen.fill((135,206,235))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                character_y_coordinate -= 70
                if character_y_coordinate < 100:
                    character_y_coordinate = 100
            elif event.key == pygame.K_s:
                character_y_coordinate += 70
                if character_y_coordinate > 380:
                    character_y_coordinate = 380
            else:
                pass

    bulletReadyCheck()
    zombieSpawnCheck()
    
    for zombie in zombie_group:
        healthBar(zombie.x_value, zombie.y_value, health_points, zombie.health)
    
    if bullet_group and zombie_group:
        for bullet in bullet_group:
            for zombie in zombie_group:
                collision = pygame.sprite.collide_rect(bullet,zombie)
                if collision:
                    zombie.health -= damage
                    bullet.kill()
                
                
    spriteLocation(shield_image, 155, 100)
    spriteLocation(character_image,character_x_coordinate,character_y_coordinate)

    zombie_group.draw(screen)
    zombie_group.update()
    bullet_group.draw(screen)
    bullet_group.update()
    pygame.display.update()