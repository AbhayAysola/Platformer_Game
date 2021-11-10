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

ACC = 15
FRIC = 1
GRAV = 2.5 
JUMP = 45

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
   
        self.pos = [0, WINDOW_HEIGHT - 3*BLOCK_SIZE]
        self.vel = vec(0,0)
        self.acc = vec(0,0)

    def move(self):
        self.acc = vec(0, GRAV)
    
        pressed_keys = pygame.key.get_pressed()
                
        if pressed_keys[pygame.K_LEFT] and 0 < self.pos[0]:
            self.acc.x = -ACC
        if pressed_keys[pygame.K_RIGHT] and self.pos[0] < 1920 - BLOCK_SIZE:
            self.acc.x = ACC

        self.acc.x += self.vel.x * -FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

    def render(self) -> None:
        self.rect.topleft = self.pos
        windowSurface.blit(self.surf, self.rect)

    def update(self):
        player.move()
        player.render()
        hits = pygame.sprite.spritecollide(self, blocks, False)
        if self.vel.y > 0:
            print('vel ', self.vel.y)
            if hits:
                self.vel.y = 0
                self.pos.y = hits[0].rect.top - BLOCK_SIZE + 1
                self.acc.y = 0

    def jump(self):
        hits = pygame.sprite.spritecollide(self, blocks, False)
        if hits:
            self.vel.y = -JUMP

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
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_SPACE, pygame.K_w, pygame.K_UP]:
                player.jump()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                terminate()

    for block in blocks:
        block.render()
    player.update()

    pygame.display.update() # Important