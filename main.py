from sys import exit  # method

import colorgram
import pygame
import random

from sprites import Player, Obstacle


def display_score():
    """
    display the current score during the game and return the score
    :return: current score
    """
    current_time = int((pygame.time.get_ticks() - start_time) / 1000)
    score_surf = text_font.render(f"Score: {current_time}", False, (64, 64, 64))  # --> Surface object
    score_react = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_react)
    return current_time


def display_highest_score():
    with open(file="highest_score", mode="r+") as file_object:
        highest_score = int(file_object.read())
        if score > highest_score:
            highest_score = score
            file_object.seek(0)
            file_object.write(str(highest_score))

    highest_score_message = text_font.render(f"highest score: {highest_score}", False, (111, 196, 169))
    highest_score_message_rect = highest_score_message.get_rect(center=(400, 380))
    screen.blit(highest_score_message, highest_score_message_rect)


def collision_sprites():
    """
    checks if the runner (sprite object) that belong to the player group
    is colliding with any other sprites ('fly' or 'snail' in obstacle_group)

    :return: True or False
    """
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, dokill=False):
        obstacle_group.empty()
        return False
    else:
        return True


pygame.init()  # initializing Pygame
screen = pygame.display.set_mode((800, 400))  # create a display surface object and display it for one second
pygame.display.set_caption("Runner")  # give our game a title
clock = pygame.time.Clock()  # create a clock object to help track time and controlling the frame-rate
text_font = pygame.font.Font('font/Pixeltype.ttf', 50)  # create a Font object from a file
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound(file='audio/music.wav')
bg_music.set_volume(0.2)
bg_music.play(loops=-1)

runner = Player()
# Groups:
# container for a single Sprite object
player = pygame.sprite.GroupSingle()  # Create a GroupSingle object ( container for player object)
obstacle_group = pygame.sprite.Group()

# add the sprite to a group
player.add(runner)  # Player() is a Sprite object and add is a method belong to AbstractGroup class.

# Sky and ground:
sky_surface = pygame.image.load('graphics/Sky.png').convert()  # load new image from a file and create a surface object
sky_color = colorgram.extract('graphics/Sky.png', 3)
ground_surface = pygame.image.load('graphics/ground.png').convert()  # function

# Intro screen
player_stand = pygame.image.load("graphics/Player/player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)  # Surface object
player_stand_rect = player_stand.get_rect(center=(400, 200))

game_name = text_font.render("Pixel Runner", False, (111, 196, 169))  # Surface object
game_name_react = game_name.get_rect(center=(400, 80))

game_message = text_font.render("Press space to run", False, (111, 196, 169))
game_message_react = game_message.get_rect(center=(400, 340))

# Timers:
obstacle_timer = pygame.USEREVENT  # Create a custom user event ID (int) (24)
pygame.time.set_timer(obstacle_timer, 1500)

player_timer = pygame.USEREVENT + 1
pygame.time.set_timer(player_timer, 1000)

# while loop - draw all our elements and update everything
while True:
    for event in pygame.event.get():  # loop through all the events (check for all possible types of player input)
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()  # closes any kind of code once you call it --> our code going to end

        if game_active:

            if event.type == obstacle_timer:  # User event
                obstacle_group.add(Obstacle(random.choice(['fly', 'snail', 'snail', 'snail'])))

        else:  # when the game is not active

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()

    if game_active:

        screen.blit(sky_surface, (0, 0))  # attach the regular surface to our display surface
        screen.blit(ground_surface,
                    (0, 300))  # each surface is put in the same position on every frame - it's not static !

        score = display_score()

        player.draw(screen)  # draw the player (GroupSingle object) on display surface
        player.update()  # AbstractGroup method

        obstacle_group.draw(screen)  # blit the Sprite images
        obstacle_group.update()

        # collisions:
        game_active = collision_sprites()

    # when the game is not active:
    else:

        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)  # dest parameter can be Rect
        screen.blit(game_name, game_name_react)

        # create Surface object with a specified text rendered on it
        score_message = text_font.render(f"Your score: {score}", False, (111, 196, 169))

        # get the rectangular area of the Surface and returns a new rectangle covering the entire surface
        score_message_rect = score_message.get_rect(center=(400, 340))

        if score == 0:
            screen.blit(game_message, game_message_react)
        else:
            screen.blit(score_message, score_message_rect)

        display_highest_score()

    pygame.display.update()  # update the display surface/the frame

    # while loop should not run faster than 60 times per second (in one second we have 60 updates)
    # about one while loop for every 17 milliseconds
    clock.tick(60)  # 60 fps
