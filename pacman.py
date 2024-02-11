import pygame
from pygame.locals import *
from Enemy import *
from pygame import mixer
from Player import Pacman
from Map import grid, dots
#window
SCREEN = pygame.display.set_mode((700, 864))
WINDOW = pygame.Surface((672, 744))
pygame.display.set_caption('Pac-Man')

#font
font = './grafiki/Apple_II_ALT_Pro.otf'
#sound
pygame.mixer.init()
intro=mixer.Sound('./sounds/Start_Music.mp3')

#game_img
BACKGROUND_IMAGE_PATH = './grafiki/other/background.png'
DOT_IMAGE_PATH = './grafiki/other/pellet.png'
POWERUP_IMAGE_PATH = './grafiki/other/powerup.png'
LIFE_IMAGE_PATH = './grafiki/other/pacman_life.png'
#direction#
keys = {
    K_UP: "UP",
    K_DOWN: "DOWN",
    K_LEFT: "LEFT",
    K_RIGHT: "RIGHT"
}

#map
tlo = pygame.transform.scale(pygame.image.load(BACKGROUND_IMAGE_PATH), (672, 744)) 
dot = pygame.transform.scale(pygame.image.load(DOT_IMAGE_PATH), (4, 4)) 
powerup = pygame.transform.scale(pygame.image.load(POWERUP_IMAGE_PATH), (19, 19))  
life = pygame.transform.scale(pygame.image.load(LIFE_IMAGE_PATH), (24, 24))  


# speed
SPEED = 24 // 7


####gh and pac object####
red = Red(24, 13.5, 11, SPEED, grid)
blue = Blue(24, 11.5, 14, SPEED, grid)
pink = Pink(24, 13.5, 14, SPEED, grid)
brown = Brown(24, 15.5, 14, SPEED, grid)
pacman = Pacman(24, 13.5, 23, SPEED, grid)

clock = pygame.time.Clock()


####main-function(draw)####

def draw(surface, screen, background, sprites, dots):
    updated_surface = pygame.Surface(surface.get_size())
    background_rect = background.get_rect()
    updated_surface.blit(background, background_rect)
    
    draw_dots(updated_surface, dots.positions)
    draw_lives(screen)

    if sprites[0].dying:
        sprites[0].draw(updated_surface)
    else:
        for sprite in sprites:
            sprite.draw(updated_surface)

    updated_screen = pygame.Surface(screen.get_size())
    updated_screen.blit(updated_surface, (0, 72))  

    score_text = f'SCORE: {sprites[0].get_score()}'
    score_font_size = 16  
    score_position = (8, 32) 
    draw_text(updated_screen, score_text, font, score_font_size, (255, 255, 255), score_position)

    pygame.display.update()
    screen.fill((0, 0, 0))
    screen.blit(updated_screen, (0, 0))

def draw_dots(WINDOW, dots):
    dot_positions = []
    powerup_positions = []

    num_rows = len(dots)
    num_cols = len(dots[0]) if num_rows > 0 else 0

    for i in range(num_rows):
        for j in range(num_cols):
            value = dots[i][j]
            if value == 1:
                dot_positions.append((j, i))
            elif value == 2:
                powerup_positions.append((j, i))

    for dot_pos in dot_positions:
        dot_x = dot_pos[0] * 24 + 10
        dot_y = dot_pos[1] * 24 + 10
        WINDOW.blit(dot, (dot_x, dot_y))

    for powerup_pos in powerup_positions:
        powerup_x = powerup_pos[0] * 24 + 3
        powerup_y = powerup_pos[1] * 24 + 3
        WINDOW.blit(powerup, (powerup_x, powerup_y))    

def draw_text(surface, text, font, size, color, position):
    text_font = pygame.font.Font(font, int(size))
    text_render = text_font.render(text, True, color)
    text_rect = text_render.get_rect()
    text_rect.topleft = position
    surface.blit(text_render, text_rect)

def draw_lives(WINDOW):
    lives = pacman.get_lives()
    for i in range(lives):
        WINDOW.blit(life, ((i * 28.8) + 12, 825)) 

def draw_start(WINDOW, screen, tlo, sprites, dots):
    screen_position = (0, 72)
    screen.blit(WINDOW, screen_position)
    
    score = sprites[0].get_score()
    
    score_font_size = 16
    score_font_color = (255, 255, 255)
    score_position = (8, 16)
    draw_text(screen, f'SCORE: {score}', font, score_font_size, score_font_color, score_position)
    
    ready_font_size = 18.4
    ready_font_color = (255, 241, 24)
    ready_position = (288, 480)
    draw_text(screen, "READY!", font, ready_font_size, ready_font_color, ready_position)
    
    
    pygame.display.update()
    
    screen.fill((0, 0, 0))
    WINDOW.blit(tlo, (0, 0))
    
    draw_dots(WINDOW, dots.positions)
    draw_lives(screen)
    
    for sprite in sprites:
        sprite.draw(WINDOW)


def draw_gameover(WINDOW, screen, tlo, sprites, dots):
    screen_position = (0, 72)
    screen.blit(WINDOW, screen_position)
    screen.fill((0, 0, 0))
    WINDOW.blit(tlo, (0, 0))
    score = sprites[0].get_score()
    score_font_size = 16
    score_font_color = (255, 255, 255)
    score_position = (8, 32)
    draw_text(screen, f'SCORE: {score}', font, score_font_size, score_font_color, score_position)

    gameover_font_size = 18
    gameover_font_color = (255, 0, 0)
    gameover_position = (72, 420)
    draw_text(screen, 'YOU LOSE PRESS "SPACE" TO RESTART', font, gameover_font_size, gameover_font_color, gameover_position)
    pygame.display.update()

def reset_game():
    global game_over, pacman, red, blue, pink, brown, start_animation, death_timer, end_timer
    start_animation = True
    death_timer = False
    end_timer = False
    game_over = False
    pacman = Pacman(24, 13.5, 23, SPEED, grid)
    red = Red(24, 13.5, 11, SPEED, grid)
    blue = Blue(24, 11.5, 14, SPEED, grid)
    pink = Pink(24, 13.5, 14, SPEED, grid)
    brown = Brown(24, 15.5, 14, SPEED, grid)
    dots.reset_dots()
    intro.play()
    
def handle_keydown_event(event):
    global game_over, start_animation, end_timer
    if event.key in keys and not game_over:
        pacman.update_next_direction(keys[event.key])
    elif event.key == K_SPACE and game_over:
        reset_game()
        start_animation = True


def update_dot_counter(counter):
        blue.time_since_dot = 0
        brown.time_since_dot = 0

def update_counting_dots(Red, Pink, Blue, Brown):
    if Red.has_left and not Pink.has_left:
        Pink.counting_dots = True
    elif Pink.has_left and not Blue.has_left:
        Blue.counting_dots = True
    elif Blue.has_left and not Brown.has_left:
        Brown.counting_dots = True

if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    clock = pygame.time.Clock()

    import Menu
    Menu.main_menu()

    start_animation = True
    start_frames = 0
    start_delay = 120
    death_timer = False
    death_frames = 0
    death_delay = 60
    end_timer = False
    end_frames = 0
    end_delay = 120
    game_over = False

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                handle_keydown_event(event)
          
        if not start_animation and not game_over and not death_timer and not end_timer:
            draw(WINDOW, SCREEN, tlo, [pacman, red, blue, pink, brown], dots)
            pacman.move()
            red.move(pacman, grid)
            blue.move(pacman, grid, red)
            pink.move(pacman, grid)
            brown.move(pacman, grid)

        elif end_timer and end_frames >= end_delay:
            end_timer = False
            end_frames = 0
            dots.reset_dots()
            red.reset_level()
            blue.reset_level()
            pink.reset_level()
            brown.reset_level()
            red.current_direction = 'LEFT'
            blue.current_direction = 'UP'
            pink.current_direction = 'DOWN'
            brown.current_direction = 'UP'
            pacman.reset(False)
            start_animation = True

        elif end_timer:
            draw(WINDOW, SCREEN, tlo, [pacman], dots)
            end_frames += 1

        elif death_timer and death_frames >= death_delay:
            death_timer = False
            death_frames = 0
            red.reset()
            blue.reset()
            pink.reset()
            brown.reset()
            pacman.reset(True)
            intro.play()
            
        elif death_timer:
            draw(WINDOW, SCREEN, tlo, [pacman], dots)
            pacman.move()
            death_frames += 1

        elif game_over:
            draw_gameover(WINDOW, SCREEN, tlo, [pacman], dots)

        elif start_frames <= start_delay // 2 and start_animation:
            draw_start(WINDOW, SCREEN, tlo, [pacman], dots)
            start_frames += 1

        elif start_frames <= start_delay and start_animation:
            draw_start(WINDOW, SCREEN, tlo, [pacman, red, blue, pink, brown], dots)
            start_frames += 1

        elif start_animation:
            start_animation = False
            start_frames = 0
            blue.alive = False
            pink.alive = False
            brown.alive = False
            blue.spawning = True
            pink.spawning = True
            brown.spawning = True
            red.current_direction = 'LEFT'
            blue.current_direction = 'UP'
            pink.current_direction = 'DOWN'
            brown.current_direction = 'UP'

        if pacman.start_reset:
            death_timer = True
            start_animation = pacman.lives > 0
            game_over = not start_animation
            pacman.start_reset = False

        if dots.is_empty():
            pacman.level_end = True
            end_timer = True

        update_dot_counter(pink)
        update_dot_counter(blue)
        update_dot_counter(brown)

        update_counting_dots(red, pink, blue, brown)