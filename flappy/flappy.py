import random # to generate the random numnber
import sys # sys.exit take exit from the game 
import pygame 
from pygame.locals import *  # Basic pygame imports


# Global variables for the game-------------------------------------------------------------------

FPS = 32 # Frames Per Second
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT)) #actual game screen
GROUNDY = SCREENHEIGHT * 0.8 # SCREEN base side
GAME_SPRITES = {} # GAME IMAGE
GAME_SOUNDS = {} # GAME SOUNDS
PLAYER = 'C:/Users/sagar/OneDrive/Desktop/venky/python/flappy/sprites/bird.png'
BACKGROUND = 'C:/Users/sagar/OneDrive/Desktop/venky/python/flappy/sprites/background.png'
PIPE = 'C:/Users/sagar/OneDrive/Desktop/venky/python/flappy/sprites/pipe.png'


# this will be the main point from where our game will start---------------------------------------

def welcomeScreen():
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    messagey = int(SCREENHEIGHT*0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            # if user clicks on cross button close the game
            if event.type  == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # if the user presses space or up key start the game for them
            elif event.type==KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'],(0, 0))
                SCREEN.blit(GAME_SPRITES['player'],(playerx, playery))
                SCREEN.blit(GAME_SPRITES['message'],(messagex, messagey))
                SCREEN.blit(GAME_SPRITES['base'],(basex, GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)



def mainGame(): # mail game will be start after clicking on welcome scree
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    basex = 0

    # creating two pipe for blitting on the screen

    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    # upper pipe list
    upperPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[0]['y']},
    ]
    # lower pipe list
    lowerPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[1]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[1]['y']},
    ]

    pipeVelX = -4 
    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8 # velocity while flapping
    playerFlapped = False # it is true when bird is flapping
    
    # run the game main loop 
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()

        # this function will return true if playr is crashed
        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)
        if crashTest:
            return

        # check the score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos<= playerMidPos < pipeMidPos +4:
                score +=1
                print(f"Your score is {score}") 
                GAME_SOUNDS['point'].play()
        

        if playerVelY <playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False            
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        # move pipe to the left
        for upperPipe , lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # add a new pipe when the first is about to cross the leftmost part of the screen

        if 0<upperPipes[0]['x']<5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        
        # if pipe was out of the screen , remove it 
        
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # let blit our sprites now

        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe , lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))

        # to show the score
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)


# hit and out

def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery> GROUNDY - 25  or playery<0:
        GAME_SOUNDS['hit'].play()
        return True
    
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    return False

# generate position of two pipes for blitting

def getRandomPipe():
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset =  SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2 *offset))
    pipeX = SCREENWIDTH - 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1}, #upper pipe 
        {'x': pipeX, 'y': y2} #lower pipe
    ]
    return pipe


if __name__ == "__main__":
    pygame.init() # first we want to initialize the pygame
    FPSCLOCK = pygame.time.Clock() # this will controls the FSP 
    pygame.display.set_caption('Flappy game by venky')
    GAME_SPRITES['numbers'] = (
        pygame.image.load('C:/Users/sagar/OneDrive/Desktop/venky/python/flappy/sprites/0.png').convert_alpha(), # convert_alpha will changes the pixel #convert will optimizes the image
        pygame.image.load('C:/Users/sagar/OneDrive/Desktop/venky/python/flappy/sprites/1.png').convert_alpha(),
        pygame.image.load('C:/Users/sagar/OneDrive/Desktop/venky/python/flappy/sprites/2.png').convert_alpha(),
        pygame.image.load('C:/Users/sagar/OneDrive/Desktop/venky/python/flappy/sprites/3.png').convert_alpha(),
        pygame.image.load('C:/Users/sagar/OneDrive/Desktop/venky/python/flappy/sprites/4.png').convert_alpha(),
        pygame.image.load('C:/Users/sagar/OneDrive/Desktop/venky/python/flappy/sprites/5.png').convert_alpha(),
        pygame.image.load('C:/Users/sagar/OneDrive/Desktop/venky/python/flappy/sprites/6.png').convert_alpha(),
        pygame.image.load('C:/Users/sagar/OneDrive/Desktop/venky/python/flappy/sprites/7.png').convert_alpha(),
        pygame.image.load('C:/Users/sagar/OneDrive/Desktop/venky/python/flappy/sprites/8.png').convert_alpha(),
        pygame.image.load('C:/Users/sagar/OneDrive/Desktop/venky/python/flappy/sprites/9.png').convert_alpha(),
    )

    GAME_SPRITES['message'] =pygame.image.load('C:/Users/sagar/OneDrive/Desktop/venky/python/flappy/sprites/messege.png').convert_alpha()
    GAME_SPRITES['base'] =pygame.image.load('C:/Users/sagar/OneDrive/Desktop/venky/python/flappy/sprites/base.png').convert_alpha()
    GAME_SPRITES['pipe'] =(pygame.transform.rotate(pygame.image.load( PIPE).convert_alpha(), 180), 
    pygame.image.load(PIPE).convert_alpha()
    )

    # sounds--------------------------------------------------------------------------------------
    
    GAME_SOUNDS['die'] = pygame.mixer.Sound('C:/Users/sagar/OneDrive/Desktop/venky/python/flappy/music/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('C:/Users/sagar/OneDrive/Desktop/venky/python/flappy/music/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('C:/Users/sagar/OneDrive/Desktop/venky/python/flappy/music/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('C:/Users/sagar/OneDrive/Desktop/venky/python/flappy/music/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('C:/Users/sagar/OneDrive/Desktop/venky/python/flappy/music/wing.wav')

    GAME_SPRITES['background'] =pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] =pygame.image.load('C:/Users/sagar/OneDrive/Desktop/venky/python/flappy/sprites/bird.png').convert_alpha()

    while True:
        welcomeScreen() # displys the welcome screen
        mainGame() # mail game will be start after clicking on welcome scree