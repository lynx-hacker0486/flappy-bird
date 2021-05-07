import random # For importing random numbers in the game
import sys # We will use sys.exit to exit the game 
import os
import pygame 
from pygame.locals import * # To import local files (pngs, sounds) in the game 

# Game specific variables
FPS = 32
SCREEN_WIDTH = 289
SCREEN_HEIGHT = 511
GROUND_Y = SCREEN_HEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'assets/sprites/bird.png'
BASE = 'assets/sprites/base.png'
BACKGROUND = 'assets/sprites/background.png'
PIPE = 'assets/sprites/pipe.png'
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Game Specific Functions
def text_screen(text, color, x, y):
    screen_text = pygame.font.SysFont(None, 20).render(text, True, color)
    SCREEN.blit(screen_text, (x, y))

# Welcome Screen function 
def welcomeScreen():
    # PLAYER_X = int(SCREEN_WIDTH - GAME_SPRITES['player'].get_width())/2
    PLAYER_X = int(SCREEN_WIDTH)/5
    PLAYER_Y = int(SCREEN_HEIGHT - GAME_SPRITES['player'].get_height())/2
    MESSAGE_X = int(SCREEN_WIDTH - GAME_SPRITES['message'].get_width())/2
    MESSAGE_Y = int(SCREEN_HEIGHT * 0.13)
    BASE_X = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == K_ESCAPE):
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == K_SPACE or (event.key == K_UP or event.key == K_RETURN):
                    return

            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))
                SCREEN.blit(GAME_SPRITES['player'], (PLAYER_X, PLAYER_Y))
                SCREEN.blit(GAME_SPRITES['message'], (MESSAGE_X, MESSAGE_Y))
                SCREEN.blit(GAME_SPRITES['base'], (BASE_X, GROUND_Y))
                pygame.display.update()
                FPS_CLOCK.tick(FPS)

# Main game function
def gameScreen():
    # PLAYER_X = int(SCREEN_WIDTH - GAME_SPRITES['player'].get_width())/2
    SCORE = 0
    PLAYER_X = int(SCREEN_WIDTH)/5
    PLAYER_Y = int(SCREEN_HEIGHT - GAME_SPRITES['player'].get_height())/2
    BASE_X = 0
    
    # Generate 2 new pipe for bliting on the screen
    PIPE_1 = getRandomPipe()
    PIPE_2 = getRandomPipe()

    # My list of upper pipes
    UPPER_PIPES  = [
        {'x': SCREEN_WIDTH + 200, 'y': PIPE_1[0]['y']},
        {'x': SCREEN_WIDTH + 200 + (SCREEN_WIDTH/2), 'y': PIPE_2[0]['y']},
    ]

    # My list of lower pipes
    LOWER_PIPES  = [
        {'x': SCREEN_WIDTH + 200, 'y': PIPE_1[1]['y']},
        {'x': SCREEN_WIDTH + 200 + (SCREEN_WIDTH/2), 'y': PIPE_2[1]['y']},
    ]

    PIPES_VELOVITY_X = -4

    PLAYER_VELOVITY_Y = -9
    PLAYER_MAX_VELOVITY_Y = 10
    PLAYER_MIN_VELOVITY_Y = -8
    PLAYER_ACCELERATION_Y = 1

    PLAYER_FLAP_VELOCITY = -8
    PLAYER_FLAPPED = False

    # if highscore.txt file is not present it will create
    if (not os.path.exists("gamesave\\highscore.txt")):
        with open("gamesave\\highscore.txt", "w") as h:
            h.write("0") 
    # Highscore
    with open("gamesave\\highscore.txt", "r") as h:
        HIGHSCORE = h.read()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_UP or (event.key == K_SPACE):
                    if PLAYER_Y > 0:
                        PLAYER_VELOVITY_Y = PLAYER_FLAP_VELOCITY
                        PLAYER_FLAPPED = True
                        GAME_SOUNDS['wing'].play()

        # check if player is crashed
        crashTest = isColide(PLAYER_X, PLAYER_Y, UPPER_PIPES, LOWER_PIPES)
        if crashTest:
            GAME_SOUNDS['hit'].play()
            return

        # score updation
        PLAYER_MID_POSITION = PLAYER_X + GAME_SPRITES['player'].get_width()/2
        
        for pipe in UPPER_PIPES:
            PIPE_MID_POSITION = int(pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2)
            if PIPE_MID_POSITION <= PLAYER_MID_POSITION < PIPE_MID_POSITION + 4:
                SCORE += 1
                if SCORE > int(HIGHSCORE):
                    HIGHSCORE = SCORE
                    with open("gamesave\\highscore.txt", "w") as h:
                        h.write(str(HIGHSCORE))
                GAME_SOUNDS['point'].play()
        
        if PLAYER_VELOVITY_Y < PLAYER_MAX_VELOVITY_Y and not PLAYER_FLAPPED:
            PLAYER_VELOVITY_Y += PLAYER_ACCELERATION_Y
        
        if PLAYER_FLAPPED:
            PLAYER_FLAPPED = False

        PLAEYR_HEIGHT = GAME_SPRITES['player'].get_height()
        PLAYER_Y = PLAYER_Y + min(PLAYER_VELOVITY_Y, GROUND_Y - PLAYER_Y - PLAEYR_HEIGHT)

        # Move pipe to the left
        for UPPER_PIPE , LOWER_PIPE in zip(UPPER_PIPES , LOWER_PIPES):
            UPPER_PIPE['x'] += PIPES_VELOVITY_X
            LOWER_PIPE['x'] += PIPES_VELOVITY_X 

        # Add a new pipe when the first pipe is about to cross the leftmost part of the screen
        if 0 < UPPER_PIPES[0]['x'] < 5:
            NEW_PIPE = getRandomPipe()
            UPPER_PIPES.append(NEW_PIPE[0])
            LOWER_PIPES.append(NEW_PIPE[1])

        # if pipes go out of the screen, remove it
        if UPPER_PIPES[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            UPPER_PIPES.pop(0)
            LOWER_PIPES.pop(0)

        # let's blit our screen now
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for UPPER_PIPE, LOWER_PIPE in zip(UPPER_PIPES, LOWER_PIPES):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (UPPER_PIPE['x'], UPPER_PIPE['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (LOWER_PIPE['x'], LOWER_PIPE['y']))
        SCREEN.blit(GAME_SPRITES['base'], (BASE_X, GROUND_Y))
        SCREEN.blit(GAME_SPRITES['player'], (PLAYER_X, PLAYER_Y))

        MY_DIGITS = [int(x) for x in list(str(SCORE))]
        WIDTH = 0
        for digits in MY_DIGITS:
            WIDTH += GAME_SPRITES['numbers'][digits].get_width()
        X_OFFSET  = (SCREEN_WIDTH - WIDTH)/2
        
        for digits in MY_DIGITS:
            SCREEN.blit(GAME_SPRITES['numbers'][digits], (X_OFFSET, SCREEN_WIDTH * 0.12))
            X_OFFSET += GAME_SPRITES['numbers'][digits].get_width()

        text_screen("Highscore: " + str(HIGHSCORE), BLACK, 5, 3)
        pygame.display.update()
        FPS_CLOCK.tick(FPS)
        
def isColide(PLAYER_X, PLAYER_Y, UPPER_PIPES, LOWER_PIPES):
    if PLAYER_Y > GROUND_Y - 25 or PLAYER_Y < 0:
        return True

    for pipe in UPPER_PIPES:
        PIPE_HEIGHT = GAME_SPRITES['pipe'][0].get_height()
        if (PLAYER_Y < PIPE_HEIGHT + pipe['y'] and abs(PLAYER_X - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            return True

    for pipe in LOWER_PIPES:
        if (PLAYER_Y + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(PLAYER_X - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            return True
            
    return False

def getRandomPipe():
    PIPE_HEIGHT = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREEN_HEIGHT/3
    y2 = offset + random.randrange(0, int(SCREEN_HEIGHT - GAME_SPRITES['base'].get_height() - (1.2 * offset)))
    PIPE_X = SCREEN_HEIGHT + 10
    y1 = PIPE_HEIGHT - y2 + offset
    pipe = [
        {'x': PIPE_X, 'y': -y1}, # Upper pipe
        {'x': PIPE_X, 'y': y2} # Lower pipe
    ]
    return pipe

# This is the main point from which the game starts 
if __name__ == "__main__":
    
    pygame.init() # initialize all the pygame modules 
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    FPS_CLOCK = pygame.time.Clock()
    pygame.display.set_caption("FLappy Bird By Anshuman Thakur")

    # Loading all the images in the game
    GAME_SPRITES['numbers'] = ( 
        pygame.image.load('assets/sprites/0.png').convert_alpha(),
        pygame.image.load('assets/sprites/1.png').convert_alpha(),
        pygame.image.load('assets/sprites/2.png').convert_alpha(),
        pygame.image.load('assets/sprites/3.png').convert_alpha(),
        pygame.image.load('assets/sprites/4.png').convert_alpha(),
        pygame.image.load('assets/sprites/5.png').convert_alpha(),
        pygame.image.load('assets/sprites/6.png').convert_alpha(),
        pygame.image.load('assets/sprites/7.png').convert_alpha(),
        pygame.image.load('assets/sprites/8.png').convert_alpha(),
        pygame.image.load('assets/sprites/9.png').convert_alpha()
    )
    GAME_SPRITES['message'] = pygame.image.load('assets/sprites/message.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load(BASE).convert_alpha()
    GAME_SPRITES['pipe'] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
        pygame.image.load(PIPE).convert_alpha()
    )
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()
    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    
    # Game sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound('assets/audio/die.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('assets/audio/wing.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('assets/audio/swoosh.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('assets/audio/point.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('assets/audio/hit.wav')

    # Game loop
    while True:
        welcomeScreen()
        gameScreen()





