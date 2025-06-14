import pygame
from pygame.locals import *
import random
import time

#change background
def changeBackground(img):
    # Change the background 
    background = pygame.image.load(img)
    #set its size
    bg = pygame.transform.scale(background, (screen_width,screen_height))
    screen.blit(bg,(0,0))

# Initialize Pygame
pygame.init()
# Set up the screen dimensions
screen_width = 900
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Recycle Game')

class Bin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/poubelle.png')
        self.image = pygame.transform.scale(self.image, (50,50))
        self.rect = self.image.get_rect()

class Recyclable(pygame.sprite.Sprite):
    def __init__(self, img):
        super().__init__()
        self.image = pygame.image.load(img)
        self.image = pygame.transform.scale(self.image, (30,30))
        self.rect = self.image.get_rect()

class NonRecyclable(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/bag.png")
        self.image = pygame.transform.scale(self.image, (30,30))
        self.rect = self.image.get_rect()

images = ["images/item1.png","images/box.png","images/pen.png"]

recyclable_list = pygame.sprite.Group()
non_recyclable_list = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

for i in range(30):
    item = Recyclable(random.choice(images))
    item.rect.x = random.randrange(0,screen_width - item.rect.width)
    item.rect.y = random.randrange(0,screen_height - item.rect.height)
    recyclable_list.add(item)
    all_sprites.add(item)

for i in range(15):
    item = NonRecyclable()
    item.rect.x = random.randrange(0,screen_width - item.rect.width)
    item.rect.y = random.randrange(0,screen_height - item.rect.height)
    non_recyclable_list.add(item)
    all_sprites.add(item)

bin = Bin()
all_sprites.add(bin)
#initialize essential variables
# Define colour
WHITE = (255, 255, 255)
RED=(255,0,0)
playing=True
score = 0
#clock 
clock = pygame.time.Clock()
#start time
start_time = time.time()
#font to print score on screen 
myFont=pygame.font.SysFont("Times New Roman",22)
timingFont=pygame.font.SysFont("Times New Roman",22)
text=myFont.render("Score ="+str(0),True,WHITE)

# Main game loop    
while playing:
    clock.tick(60)
    screen.fill(WHITE)
    changeBackground('images/greenbackground.png')
    
    # Draw all sprites
    all_sprites.draw(screen)
    
    # Draw the score
    text = myFont.render("Score = " + str(score), True, WHITE)
    screen.blit(text, (10, 10))
    
    # Draw the timer
    elapsed_time = time.time() - start_time
    timer_text = timingFont.render(f"Time: {int(elapsed_time)}s", True, WHITE)
    screen.blit(timer_text, (screen_width - 150, 10))

    if elapsed_time > 60:
        if score >= 30:
            win_text = myFont.render("You Win!", True, RED)
        else:
            win_text = myFont.render("You Lose!", True, RED)
        screen.blit(win_text, (screen_width // 2 - win_text.get_width() // 2, screen_height // 2 - win_text.get_height() // 2))

    
    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        
        if event.type == MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            bin.rect.center = pos
            
            # Check for collisions with recyclable items
            for item in recyclable_list:
                if bin.rect.colliderect(item.rect):
                    score += 1
                    item.kill()
            
            # Check for collisions with non-recyclable items
            for item in non_recyclable_list:
                if bin.rect.colliderect(item.rect):
                    score -= 1
                    item.kill()

    pygame.display.flip()

pygame.quit()
