import pygame
from sys import exit
from random import randint, choice
from PIL import Image

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        scale_factor = 4
        player_idle_1 = pygame.image.load('stickman/graphics/player/stickman_stand1.png').convert_alpha()
        player_idle_2 = pygame.image.load('stickman/graphics/player/stickman_stand2.png').convert_alpha()
        
        player_idle_1 = pygame.transform.scale_by(player_idle_1, scale_factor)
        player_idle_2 = pygame.transform.scale_by(player_idle_2, scale_factor)
        
        self.player_idle = [player_idle_1, player_idle_2]
        
        self.player_run = [
            pygame.transform.scale_by(pygame.image.load(f'stickman/graphics/player/stickman_run{i}.png').convert_alpha(), scale_factor)
            for i in range(1, 8)
        ]
        
        self.player_hadouken = [
            pygame.transform.scale_by(pygame.image.load(f'stickman/graphics/player/stickman_hadouken{i}.png').convert_alpha(), scale_factor)
            for i in range(1,11)
        ]
        
        self.player_jump = [
            pygame.transform.scale_by(pygame.image.load(f'stickman/graphics/player/stickman_jump{i}.png').convert_alpha(), scale_factor)
            for i in range(1,9)
        ]
        
        self.player_kick = [
            pygame.transform.scale_by(pygame.image.load(f'stickman/graphics/player/stickman_kick{i}.png').convert_alpha(), scale_factor)
            for i in range(1,11)
        ]
        self.player_punch = [
            pygame.transform.scale_by(pygame.image.load(f'stickman/graphics/player/stickman_punch{i}.png').convert_alpha(), scale_factor)
            for i in range(1,8)
        ]
        self.player_index_idle = 0
        self.player_index_run = 0
        self.player_index_hadouken = 0
        self.player_index_jump = 0
        self.player_index_kick = 0
        self.player_index_punch = 0
        
        self.image = self.player_idle[self.player_index_idle]
        self.rect = self.image.get_rect(center=(120,500))
        
        self.speed = 5
        self.running = False
        self.hadouken = False
        self.kick = False
        self.punch = False
        self.facing_right = True
        self.jump = False
        self.gravity = 0
        
        self.walk_sound = pygame.mixer.Sound('stickman/audio/minecraft-footsteps-sound-effect-made-with-Voicemod.wav')
        self.walk_sound.set_volume(1)
        self.hadouken_sound = pygame.mixer.Sound('stickman/audio/hadouken.wav')
        self.hadouken_sound.set_volume(1)
        self.jump_sound = pygame.mixer.Sound('stickman/audio/jump.wav')
        self.jump_sound.set_volume(0.3)
        self.punch_sound = pygame.mixer.Sound('stickman/audio/punch.wav')
        self.punch_sound.set_volume(0.3)
        
    def player_input(self):
        keys = pygame.key.get_pressed()
        self.running = False
        if keys[pygame.K_d]: 
            self.rect.x += self.speed
            self.running = True
            self.facing_right = True
            
        if keys[pygame.K_a]: 
            self.rect.x -= self.speed
            self.running = True
            self.facing_right = False
            
        if keys[pygame.K_KP7] and not self.hadouken:
            self.hadouken = True
            self.player_index_hadouken = 0
        
        if keys[pygame.K_SPACE] and self.rect.bottom >= 500:
            self.jump = True
            self.gravity = -20
        
        if keys[pygame.K_KP5] and not self.kick:
            self.kick = True
            self.player_index_kick = 0
        
        if keys[pygame.K_KP4] and not self.punch:
            self.punch = True
            self.player_index_punch = 0

        channel = pygame.mixer.Channel(0)
        
        if self.hadouken:
            if not channel.get_busy():
                channel.play(self.hadouken_sound)
        elif self.jump:
            if not channel.get_busy():
                channel.play(self.jump_sound)
        elif self.kick:
            if not channel.get_busy():
                channel.play(self.punch_sound)
        elif self.punch:
            if not channel.get_busy():
                channel.play(self.punch_sound)
        elif self.running:
            if not channel.get_busy():
                channel.play(self.walk_sound, loops=-1)
        else:
            channel.stop()
        

    def animation_state(self):
        if self.running:
            self.player_index_run += 0.35
            if self.player_index_run >= len(self.player_run): 
                self.player_index_run = 0
                self.running = False
            self.image = self.player_run[int(self.player_index_run)]
            
        elif self.hadouken:
            self.player_index_hadouken += 0.15
            if self.player_index_hadouken >= len(self.player_hadouken):
                self.player_index_hadouken = 0
                self.hadouken = False
            self.image = self.player_hadouken[int(self.player_index_hadouken)]
        
        elif self.jump:
            self.player_index_jump += 0.15
            if self.player_index_jump >= len(self.player_jump):
                self.player_index_jump = 0
                self.jump = False
            self.image = self.player_jump[int(self.player_index_jump)]
            
        elif self.kick:
            self.player_index_kick += 0.3
            if self.player_index_kick >= len(self.player_kick):
                self.player_index_kick = 0
                self.kick = False
            self.image = self.player_kick[int(self.player_index_kick)]
        
        elif self.punch:
            self.player_index_punch += 0.3
            if self.player_index_punch >= len(self.player_punch):
                self.player_index_punch = 0
                self.punch = False
            self.image = self.player_punch[int(self.player_index_punch)]
        
        else:
            self.player_index_idle += 0.1
            if self.player_index_idle >= len(self.player_idle): 
                self.player_index_idle = 0
            self.image = self.player_idle[int(self.player_index_idle)]
        
        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)
    
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 500:
            self.rect.bottom = 500
            
    def update(self):
        self.animation_state()
        self.player_input()
        self.apply_gravity()

class Hadouken(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        scale_factor = 4
        self.speed = 10
        self.image = [
            pygame.transform.scale_by(pygame.image.load(f'stickman/graphics/effects/hadouken_effect{i}.png').convert_alpha(), scale_factor)
            for i in range(1,7)
        ]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.direction = direction
    def update(self):
        self.rect.x += (self.direction*self.speed)
        if self.rect.right < 0 or self.rect.left > 1264:
            self.kill()
            
#the game itself
pygame.mixer.init()
pygame.init()
screen = pygame.display.set_mode((1264,720))
clock = pygame.time.Clock()
game_active = True

player = pygame.sprite.GroupSingle()
player.add(Player())

hadouken = pygame.sprite.Group()
sky_surface = pygame.image.load('stickman/graphics/background.png').convert()
ground_surface = pygame.image.load('stickman/graphics/ground.png').convert()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    if game_active:
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,470))
        player.update()
        player.draw(screen)
        hadouken.update()
        hadouken.draw(screen)
    else:
        pass
    
    pygame.display.update()
    clock.tick(60)