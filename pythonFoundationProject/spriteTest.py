import pygame
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

pygame.init()
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
sprite_sheet_image = pygame.image.load("cardSprites.png").convert_alpha()

def get_image(sheet, width, height):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), (0, 0, width, height))

    return image

frame_0 = get_image(sprite_sheet_image, 80, 115)

run = True
while run:

    screen.blit(frame_0, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()




pygame.quit()