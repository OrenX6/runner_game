import random
import pygame


class Player(pygame.sprite.Sprite):  # player is kind of sprite class
    def __init__(self):  # overrides
        super().__init__()  # initializing the Sprite class constructor, so we can access it.
        # Player surfaces:
        player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()  # Surface object
        player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()  # Surface object
        self.player_walk = [player_walk_1, player_walk_2]  # frames
        self.player_index = 0  # immutable
        self.player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()
        self.image = self.player_walk[self.player_index]  # Surface object (mutable)

        # Create new Rect object with the size of the image,set origin point and  built position.
        self.rect = self.image.get_rect(midbottom=(80, 300))  # Rect Object (mutable)
        self.gravity = 0
        self.jump_sound = pygame.mixer.Sound(file='audio/jump.mp3')
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        """
        Give us all possible key inputs. The player jump if we press the right key.
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20  # the player jump !
            self.jump_sound.play()

    def apply_gravity(self):
        """
        apply the gravity on the player after the jump.
        """
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300  # set the player on top of the ground

    def animation_state(self):
        """
        update the player surface (3 options):
        play walking animation if the player on the floor.
        display the jump surface when the player is not on the floor.
        """
        if self.rect.bottom < 300:  # jump
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):  # Overriding the instance method of Sprite class
        """
        method to control sprite behavior:
        player behavior means if he is jumping or not,
        if he is, then we apply the gravity on the player and change the player's frame
        to be jumping.
        if he is not jumping then we apply the walking animation.
        """
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    """
    Create an obstacle object 'fly' or 'snail':
    attributes:
    frames = list of obstacle surfaces objects
    image = the first surface
    rect = Rect object of the image.

    """

    def __init__(self, obstacle_type):  # override
        super().__init__()

        if obstacle_type == 'fly':
            fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()  # fly surfaces:
            fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()  # snail surfaces
            snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(random.randint(900, 1100), y_pos))  # random x

    def animation_state(self):
        """
        update the obstacle surface (2 options for each obstacle):

        """
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        """
         method to control sprites behavior:
         The fly and the snail have the same behavior in different positions.
         both of them fly or walking

        """
        self.animation_state()
        self.rect.left -= 6
        self.destroy()

    def destroy(self):
        """
        Whenever the sprite goes out of the screen it's going to destroy itself.
        """
        if self.rect.right < 0:
            self.kill()
