import pygame
import button

pygame.init()

# game window
screenwidth = 672
screenheight = 864

screen = pygame.display.set_mode((screenwidth, screenheight))
pygame.display.set_caption("Pac-man")

icon_img = pygame.image.load("./grafiki/menu/icon.png").convert_alpha()
pygame.display.set_icon(icon_img)

bg_img = pygame.image.load("./grafiki/menu/Pac-Man-Menu.png").convert_alpha()

# game variables
menu_state = "start"

# define fonts / colours
font = pygame.font.Font("./grafiki/menu/Minecraft.ttf", 45)
text_col = (255, 255, 255)


def drawtext(text, font, textcol, x, y):
    img = font.render(text, True, textcol)
    screen.blit(img, (x, y))


# load images
start_img = pygame.image.load("./grafiki/menu/start.png").convert_alpha()
quit_img = pygame.image.load("./grafiki/menu/quit.png").convert_alpha()

# create button instances
screen.blit(bg_img, (0, 0))
quit_button = button.Button(250, 500, quit_img, 1.85)
start_button = button.Button(225, 400, start_img, 1.85)

def main_menu():
    global menu_state
    while True:
        # check menu state
        if menu_state == "start":
            if quit_button.draw(screen):
                pygame.quit()
                exit()
            if start_button.draw(screen):
                menu_state = "game"
                break

        # event handler
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu_state = "main"
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        pygame.display.update()
