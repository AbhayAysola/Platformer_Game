import pygame
import sys

# Colours
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Constants
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
BACKGROUND_COLOUR = WHITE
BLOCK_SIZE = 60
BLOCK_COLOUR = CYAN

PLAYER_SPEED = 10
GRAV = 30
JUMP = 200

# Initialising
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('platformer gaem dum')

vec = pygame.math.Vector2

background_image = pygame.image.load('background_image.png')
background_rect = background_image.get_rect()

blocks = pygame.sprite.Group()

# Block
class Block(pygame.sprite.Sprite):

    
    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, texture, posx, posy) -> None:
        # Call the parent class (Sprite) constructor
        super().__init__()
        self.texture = texture
        self.image = pygame.image.load(self.texture)
        self.rect = self.image.get_rect(topleft=(posx, posy))
    
    def render(self) -> None:
        windowSurface.blit(self.image, self.rect)

coordsx = 0
for i in range(int(WINDOW_WIDTH/BLOCK_SIZE)):
    blocks.add(Block("dirt_block.png", coordsx, WINDOW_HEIGHT - BLOCK_SIZE))
    blocks.add(Block("grass_block.png", coordsx, WINDOW_HEIGHT - 2*BLOCK_SIZE))
    coordsx += BLOCK_SIZE

# Player stuff
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.surf = pygame.Surface((60, 60))
        self.surf.fill(CYAN)
        self.rect = self.surf.get_rect()

        self.col = False
        self.pos = [5*BLOCK_SIZE, WINDOW_HEIGHT - 5*BLOCK_SIZE]

    def render(self) -> None:
        self.rect.topleft = self.pos
        windowSurface.blit(self.surf, self.rect)

    def check_col(self):
        self.rect.topleft = [self.pos[0] + 1, self.pos[1] + 1]
        col = pygame.sprite.spritecollide(self, blocks, False)
        if not col:
            self.rect.topleft = [self.pos[0] - 1, self.pos[1] - 1]
        return True if col else False

    def move(self, x, y):
        for i in range(x):
            if self.check_col():
                break
            else:
                self.pos[0] += 1 if x>0 else -1
        for i in range(y):
            if self.check_col():
                break
            else:
                self.pos[1] += 1 if y>0 else -1

    def update(self):
        # Left-Right Movement
        pressed_keys = pygame.key.get_pressed() 
        if pressed_keys[pygame.K_LEFT] and 0 < self.pos[0]:
            self.pos[0] -= PLAYER_SPEED
        if pressed_keys[pygame.K_RIGHT] and self.pos[0] < WINDOW_WIDTH - BLOCK_SIZE:
            self.pos[0] += PLAYER_SPEED
        if pressed_keys[pygame.K_SPACE]:
            self.jump()

        # Gravity
        if not self.check_col():
            self.move(0, GRAV)
        # for b in blocks:
        #     if b.rect.top == self.rect.bottom + 1:
        #         hits = True
        # hits = pygame.sprite.spritecollide(self, blocks, False)
        # if hits and not self.col:
        #     self.col = True
        #     self.pos[1] = hits[0].rect.top - BLOCK_SIZE
        # elif not self.col:
        #     self.pos[1] += 10

        self.render()


    def jump(self):
        if self.check_col():
            self.pos[1] -= JUMP

player = Player()

def terminate():
    pygame.quit()
    sys.exit()

def drawText(text, font, surface, colour, x, y):
    textobj = font.render(text, 1, colour)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Game loop
while True:
    windowSurface.blit(background_image, background_rect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                terminate()

    for block in blocks:
        block.render()

    player.update()

    pygame.display.update() # Important