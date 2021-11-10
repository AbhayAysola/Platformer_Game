import pygame, random, sys, time
from pygame.locals import *

# Set up the variables.
WINDOWWIDTH = 400
WINDOWHEIGHT = 400

PLAYERMOVESPEED = 5

ENEMYMOVESPEED = 2
ENEMYSIZE = 30
ADDNEWENEMYRATE = 80

FPS = 60

ADDNEWBULLETRATE = 15
PLAYERBULLETHEIGHT = 10
PLAYERBULLETWIDTH = 3
PLAYERBULLETSPEED = 10

BACKGROUNDCOLOUR = (255, 255, 255)

enemyAddCounter = 0

LIFESIZE = 15

highScore = 0

EXPLOSIONSIZE = 70
REMOVEEXPLOSIONSRATE = 15

ADDNEWENEMYBULLETRATE = 60

# Enemy bullet variables.
ENEMYBULLETWIDTH = 4
ENEMYBULLETHEIGHT = 7
ENEMYBULLETSPEED = 3

# Define the colours.
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# Set up direction variables.
LEFT = 'left'
RIGHT = 'right'
DOWN = 'down'
DIRECTIONS = [LEFT, RIGHT, DOWN]

# Set up pygame and the window.
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
windowSurface.fill(BACKGROUNDCOLOUR)
pygame.display.set_caption('INVASION!')

# Set up the images.
backgroundImage = pygame.image.load('backgroundImage.jpg')
backgroundRect = backgroundImage.get_rect()
playerImage = pygame.image.load('ship.png')
enemyImage = pygame.image.load('enemy.png')
explosionImage = pygame.image.load('explosionImage.png')
explosionRect = explosionImage.get_rect()
playerRect = playerImage.get_rect()
lifeImage = pygame.image.load('life.jpg')

# Set up the sounds.
shootSound = pygame.mixer.Sound('shoot.wav')
explodeSound = pygame.mixer.Sound('explosion.wav')
gameOverSound = pygame.mixer.Sound('gameover.wav')

# Set up the font.
bigFont = pygame.font.SysFont(None, 40)
smallFont = pygame.font.SysFont(None, 30)

def terminate():
    pygame.quit()
    sys.exit()

def drawText(text, font, surface, colour, x, y):
    textobj = font.render(text, 1, colour)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def showInstructions():
    drawText('''Use the right and left arrows to move. You can only move
left and right, not up and down.
M is to turn sound on or off.
[SPACE] is to shoot.
P is to pause the game.

The object of the game is to destroy the enemy ships. They can shoot you.
If they hit or shoot you, your ship explodes and you restart.
Good luck!
Press enter to continue...''', smallFont, windowSurface, colour, 0, 0)
pygame.display.update()

def playerCollided(enemies, playerRect):
    for e in enemies:
        if playerRect.colliderect(e['rect']):
            enemies.remove(e)
            return True
        
        return False

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # Pressing ESC quits.
                    terminate()
                if event.key == K_RETURN:
                    return

while True:
    # Set up the start of the game.
    enemyAddCounter = 0
    enemies = []
    playerBullets = []
    playerBulletCounter = 0
    moveUp = moveDown = moveLeft = moveRight = False
    playerRect.topleft = (round(WINDOWWIDTH / 2) - playerRect.width, round(WINDOWHEIGHT - 50))
    playerShoot = False
    windowSurface.fill(BACKGROUNDCOLOUR)
    shootSound.stop()
    explodeSound.stop()
    windowSurface.blit(backgroundImage, backgroundRect)
    explosions = []
    enemyBullets = []
    score = 0
    lives = 5
    lifex = WINDOWWIDTH - LIFESIZE
    lifey = 0
    
    while True:
        windowSurface.blit(backgroundImage, backgroundRect)
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT:
                    moveLeft = False
                    moveRight = True
                if event.key == K_SPACE:
                    playerShoot = True
            if event.type == KEYUP:
                if event.key == K_LEFT:
                    moveLeft = False
                if event.key == K_RIGHT:
                    moveRight = False
                if event.key == K_SPACE:
                    playerShoot = False
                if event.key == K_ESCAPE:
                    terminate()

        # Add new enemies to the top of the screen if needed.
        enemyAddCounter += 1
        if enemyAddCounter == ADDNEWENEMYRATE:
            enemyAddCounter = 0
            newEnemy = {'rect':pygame.Rect(random.randint(0, WINDOWWIDTH - ENEMYSIZE), 0 - ENEMYSIZE, ENEMYSIZE, ENEMYSIZE),
                        'surface':pygame.transform.scale(enemyImage, (ENEMYSIZE,  ENEMYSIZE)),
                        'dir':DOWN,
                        'sidecounter':0,
                        'downcounter':0,
                        'movecounter':0,
                        'bulletAddCounter':0
                        }
            enemies.append(newEnemy)

        # Move the player.
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * PLAYERMOVESPEED, 0)
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVESPEED, 0)

        # Let the player shoot.
        if playerShoot:
            playerBulletCounter += 1
            if playerBulletCounter == ADDNEWBULLETRATE:
                newPlayerBullet = {'rect':pygame.Rect(playerRect.centerx, playerRect.top, PLAYERBULLETWIDTH, PLAYERBULLETHEIGHT),
                                   'speed':PLAYERBULLETSPEED,
                                   'colour':GREEN
                                   }
                playerBulletCounter = 0
                playerBullets.append(newPlayerBullet)
                shootSound.stop()
                shootSound.play()

        # Let the enemies shoot.
        for e in enemies:
            e['bulletAddCounter'] += 1
            if e['bulletAddCounter'] > ADDNEWENEMYBULLETRATE:
                newEnemyBullet = {'rect':pygame.Rect(e['rect'].centerx, e['rect'].bottom, ENEMYBULLETWIDTH, ENEMYBULLETHEIGHT),
                                  'speed':ENEMYBULLETSPEED,
                                  'colour':RED
                                  }
                e['bulletAddCounter'] = 0
                enemyBullets.append(newEnemyBullet)
                shootSound.stop()
                shootSound.play()

        # Move the enemies.
        for e in enemies:
            if e['dir'] == LEFT and e['rect'].left > 0:
                e['rect'].move_ip(-1 * ENEMYMOVESPEED, 0)
                e['sidecounter'] += 1
                e['movecounter'] += 1
            if e['rect'].left <= 0:
                e['dir'] = RIGHT
            if e['dir'] == RIGHT and e['rect'].right < WINDOWWIDTH:
                e['rect'].move_ip(ENEMYMOVESPEED, 0)
                e['sidecounter'] += 1
                e['movecounter'] += 1
            if e['rect'].right >= WINDOWWIDTH:
                e['dir'] = LEFT
            if e['dir'] == DOWN:
                e['rect'].move_ip(0, ENEMYMOVESPEED)
                e['downcounter'] += 1
                
            if e['downcounter'] > random.randint(30, 60):
                e['downcounter'] = 0
                e['dir'] = random.choice([LEFT, RIGHT])
            if e['sidecounter'] > random.randint(30, 60):
                e['sidecounter'] = 0
                if e['dir'] == LEFT:
                    e['dir'] = RIGHT
                if e['dir'] == RIGHT:
                    e['dir'] = LEFT
            if e['movecounter'] > random.randint(30, 60):
                e['dir'] = DOWN
                e['movecounter'] = 0

        # Delete enemies that have fallen past the bottom of the screen.
        for e in enemies:
            if e['rect'].top > WINDOWHEIGHT:
                enemies.remove(e)
                lives -= 1
    
        # Move the player's bullets.
        for b in playerBullets:
            b['rect'].move_ip(0, -1 * PLAYERBULLETSPEED)

        # Move the enemies' bullets.
        for e in enemyBullets:
            e['rect'].move_ip(0, ENEMYBULLETSPEED)

        # Check if player's bullets have moved out of the screen.
        for b in playerBullets:
            if b['rect'].bottom < 0:
                playerBullets.remove(b)

        # Check if enemies' bullets have moved out of the screen.
        for b in enemyBullets:
            if b['rect'].top > WINDOWHEIGHT:
                enemyBullets.remove(b)

        # Set up the lives.
        livesImages = []
        lifex = WINDOWWIDTH - LIFESIZE
        for i in range(lives):
            newLife = {'rect':pygame.Rect(lifex, lifey, LIFESIZE, LIFESIZE),
                       'surface':pygame.transform.scale(lifeImage, (LIFESIZE, LIFESIZE))
                       }
            livesImages.append(newLife)
            lifex -= LIFESIZE

        # Draw the score.
        drawText('%s' % (score), bigFont, windowSurface, WHITE, 0, 0)

        # Draw the player.
        windowSurface.blit(playerImage, playerRect)

        # Draw the enemies.
        for e in enemies:
            windowSurface.blit(e['surface'], e['rect'])

        # Draw the player's bullets.
        for b in playerBullets:
            pygame.draw.rect(windowSurface, b['colour'], b['rect'])

        # Draw the enemies' bullets.
        for b in enemyBullets:
            pygame.draw.rect(windowSurface, b['colour'], b['rect'])

        # Draw the lives.
        for life in livesImages:
            windowSurface.blit(life['surface'], life['rect'])

        # Draw the explosions.
        for e in explosions:
            e['counter'] += 1
            if e['counter'] < REMOVEEXPLOSIONSRATE:
                windowSurface.blit(e['surface'], e['rect'])
            else:
                explosions.remove(e)

        pygame.display.update()

        # Check if the player has collided with any enemies.
        if playerCollided(enemies, playerRect):
            explodeSound.play()
            break

        # Check if the player collided with any enemy bullets.
        for b in enemyBullets:
            if b['rect'].colliderect(playerRect):
                enemyBullets.remove(b)
                lives -= 1

        if lives <= 0:
            if score > highScore:
                highScore = score
            break

        # Check if any enemies have collided.
        for b in playerBullets:
            for e in enemies:
                if b['rect'].colliderect(e['rect']):
                    enemies.remove(e)
                    playerBullets.remove(b)
                    score += 100
                    explodeSound.play()
                    newExplosion = {'surface':pygame.transform.scale(explosionImage, (EXPLOSIONSIZE, EXPLOSIONSIZE)),
                                    'rect':pygame.Rect(e['rect'].left, e['rect'].top, EXPLOSIONSIZE, EXPLOSIONSIZE),
                                    'counter':0
                                    }
                    explosions.append(newExplosion)

        mainClock.tick(FPS)

    # Stop the game and show the explosion effect with sound.
    gameOverSound.play()
    windowSurface.blit(pygame.transform.scale(explosionImage, (400, 400)), (0, 0, 400, 400))
    pygame.display.update()
    time.sleep(1.5)

    # Show the game over screen.
    drawText('GAME OVER!', bigFont, windowSurface, BLACK, (111), (186 - 50))
    drawText('Press ENTER to play again.', smallFont, windowSurface, BLACK, 72, 180)
    drawText('Score: %s' % (score), smallFont, windowSurface, BLACK, 150, 210)
    drawText('High score: %s' % (highScore), smallFont, windowSurface, BLACK, 130, 240)
    pygame.display.update()
    time.sleep(0.5)
    waitForPlayerToPressKey()

    gameOverSound.stop()
