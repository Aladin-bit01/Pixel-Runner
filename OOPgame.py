import pygame
import sys
from random import randint, choice
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()
        self.player_index = 0
        self.image= self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom= (200,300))
        self.gravity = 0

        self.sound= pygame.mixer.Sound('audio/jump.mp3')
        self.sound.set_volume(0.5) #between 0 and 1
    def player_input(self):
        keys= pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300: self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == 'fly':
            fly_frame_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
            fly_frame_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_frame_1, fly_frame_2]
            y_pos= 210
        else:
            snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_frame_1, snail_frame_2]
            y_pos = 300
        self.animation_index = 0
        self.image= self.frames[self.animation_index]
        self.rect= self.image.get_rect(midbottom= (randint(900,1100),y_pos))
    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image= self.frames[int(self.animation_index)]
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()



def display_score():
    current_time= round((pygame.time.get_ticks()- start)/1000)
    score_surf= text_font.render(f'Score: {current_time}', False, (64,64,64))
    score_rect= score_surf.get_rect(center= (400,50))
    screen.blit(score_surf,score_rect)
    return current_time
def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        return False
    else: return True


pygame.init()
screen= pygame.display.set_mode((800,400))
pygame.display.set_caption('Pixel Runner')
game_active= False
clock= pygame.time.Clock()
start= 0
current = 0
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.play(loops= -1) #plays forever
#Groups
player= pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()



#SKY and Ground Surfaces:
sky_surf= pygame.image.load('graphics/Sky.png').convert_alpha()
ground_surf= pygame.image.load('graphics/ground.png').convert_alpha()


#text font
text_font= pygame.font.Font('font/Pixeltype.ttf', 50)



#Timer
obstacle= pygame.USEREVENT + 1
pygame.time.set_timer(obstacle,1500)


#GameOver Screeen
player_stand_surf= pygame.image.load('graphics/Player/player_stand.png')
player_stand_surf= pygame.transform.rotozoom(player_stand_surf,0,2)
player_stand_rect= player_stand_surf.get_rect(center= (400,200))

#Game title
title_surf= text_font.render('Pixel Runner', False, (111, 196, 169))
title_rect= title_surf.get_rect(center= (400,80))

#Message
message_surf= text_font.render('PRESS SPACE TO START', False, (111, 196, 169))
message_rect = message_surf.get_rect(center=(400, 340))



while True:

    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game_active:
            if event.type == obstacle:
                obstacle_group.add(Obstacle(choice(['fly','snail', 'snail', 'snail'])))
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True

    if game_active:

        #Always Show the background (Sky+Ground)
        screen.blit(sky_surf, (0,0))
        screen.blit(ground_surf, (0,300))



        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active= collision_sprite()
        #Score
        current= display_score()
    else:
        start= pygame.time.get_ticks()
        player.sprite.rect.bottom = 300
        player.sprite.gravity = 0

        screen.fill((94,129,162))

        screen.blit(player_stand_surf,player_stand_rect)
        screen.blit(title_surf, title_rect)

        if current == 0:
            screen.blit(message_surf,message_rect)
        else:
            score_surf= text_font.render(f'Your score: {current}', False,(111, 196, 169) )
            score_rect = score_surf.get_rect(center=(400, 340))
            screen.blit(score_surf,score_rect)

    pygame.display.update()
    clock.tick(60)
