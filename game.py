import pygame
import sys
from random import randint


def display_score():
    current_time= round((pygame.time.get_ticks()- start)/1000)
    score_surf= text_font.render(f'Score: {current_time}', False, (64,64,64))
    score_rect= score_surf.get_rect(center= (400,50))
    screen.blit(score_surf,score_rect)
    return current_time
def obstacle_movement(obstacle_rect_list):
    if obstacle_rect_list:
        for obstacle_rect in obstacle_rect_list:
            obstacle_rect.x -= 5
            if obstacle_rect.bottom == 300:screen.blit(snail_surf, obstacle_rect)
            else:screen.blit(fly_surf, obstacle_rect)
        obstacle_rect_list = [obstacle for obstacle in obstacle_rect_list if obstacle.x > -100]
        return obstacle_rect_list
    else:
        return []
def collisions(player, obstacle_list):
    if obstacle_list:
        for obs in obstacle_list:
            if player.colliderect(obs): return False
    return True

def player_animation():
    global player_surf, player_index
    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index > len(player_walk): player_index = 0
        player_surf = player_walk[int(player_index)]

pygame.init()
screen= pygame.display.set_mode((800,400))
pygame.display.set_caption('Pixel Runner')
game_active= False
clock= pygame.time.Clock()
gravity= 0
start= 0
current = 0

#SKY and Ground Surfaces:
sky_surf= pygame.image.load('graphics/Sky.png').convert_alpha()
ground_surf= pygame.image.load('graphics/ground.png').convert_alpha()


#Player
player_walk1= pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_walk2= pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
player_walk =[player_walk1,player_walk2]
player_jump= pygame.image.load('graphics/Player/jump.png').convert_alpha()
player_index= 0
player_surf= player_walk[player_index]
player_rect= player_surf.get_rect(midbottom= (100,300))

#text font
text_font= pygame.font.Font('font/Pixeltype.ttf', 50)



#Snails
snail_frame_1= pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame_2= pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames= [snail_frame_1,snail_frame_2]
snail_index= 0
snail_surf= snail_frames[snail_index]
#Flies
fly_frame_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
fly_frames= [fly_frame_1,fly_frame_2]
fly_index= 0
fly_surf= fly_frames[fly_index]



obstacles_rect_list= []


#Timer
obstacle= pygame.USEREVENT + 1
pygame.time.set_timer(obstacle,1500)

#snail animation timer
snail_animation_timer= pygame.USEREVENT +2
pygame.time.set_timer(snail_animation_timer, 500)

#fly animation timer
fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)


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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == 300:
                    gravity = -20
            if event.type== pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint((event.pos)) and player_rect.bottom == 300:
                    gravity = -20

            if event.type == obstacle:
                if randint(0,2):
                    obstacles_rect_list.append(snail_surf.get_rect(bottomright= (randint(900,1100),300)))
                else:
                    obstacles_rect_list.append(fly_surf.get_rect(bottomright=(randint(900, 1100), 215)))

            if event.type == snail_animation_timer:
                if snail_index == 0 : snail_index =1
                else: snail_index = 0
                snail_surf= snail_frames[snail_index]

            if event.type == fly_animation_timer:
                if fly_index == 0:fly_index = 1
                else:fly_index = 0
                fly_surf = fly_frames[fly_index]

        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True

    if game_active:
        #Always Show the background (Sky+Ground)
        screen.blit(sky_surf, (0,0))
        screen.blit(ground_surf, (0,300))

        #Modify Comtinously the position of the obstacles
        obstacles_rect_list= obstacle_movement(obstacles_rect_list)

        #Player display on display screen
        gravity += 1
        player_rect.y += gravity
        if player_rect.bottom >= 300 : player_rect.bottom = 300
        player_animation()
        screen.blit(player_surf, player_rect)

        #collisions
        game_active = collisions(player_rect,obstacles_rect_list)

        #Score
        current= display_score()
    else:
        start= pygame.time.get_ticks()
        obstacles_rect_list.clear()
        player_rect.bottom = 300
        gravity = 0
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
