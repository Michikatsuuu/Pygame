import pygame
from Sprites import Sprite
from Map import dots
from pygame import mixer

pygame.mixer.init()
eat_sound=mixer.Sound('./sounds/credit-sound_2.mp3')
death=mixer.Sound('./sounds/Fail.mp3')
powerup=mixer.Sound('./sounds/Power_up2.mp3')

class Pacman(Sprite):
    def __init__(self, sf, x, y, v, grid):
        super().__init__(sf, x, y, v, grid)
        self.image = self.load_scaled_image('./grafiki/pacman/up_full.png', sf)
        self.rect = self.image.get_rect(center=self.get_pos())
        self.score = 0
        self.start_reset = False
        self.powered = False
        self.activated_powered = False
        self.powered_ticks = 0
        self.powered_flash = 5
        self.max_powered_ticks = 360 + self.powered_flash * 30
        self.velocity_modifier = 0.8
        self.temp_velocity_modifier = 0.8
        self.powered_velocity = 0.9
        self.temp_powered_velocity = 0.9
        self.level_end = False
        self.dot_counter = 0
        self.sprites = {
            'NONE': [
                self.load_scaled_image('./grafiki/pacman/up_full.png', sf),
                self.load_scaled_image('./grafiki/pacman/up_full.png', sf),
                self.load_scaled_image('./grafiki/pacman/up_full.png', sf),
                self.load_scaled_image('./grafiki/pacman/up_full.png', sf)
            ],
            'UP': [
                self.load_scaled_image('./grafiki/pacman/up_full.png', sf),
                self.load_scaled_image('./grafiki/pacman/up_half.png', sf),
                self.load_scaled_image('./grafiki/pacman/up_open.png', sf),
                self.load_scaled_image('./grafiki/pacman/up_half.png', sf)
            ],
            'DOWN': [
                self.load_scaled_image('./grafiki/pacman/down_full.png', sf),
                self.load_scaled_image('./grafiki/pacman/down_half.png', sf),
                self.load_scaled_image('./grafiki/pacman/down_open.png', sf),
                self.load_scaled_image('./grafiki/pacman/down_half.png', sf)
            ],
            'LEFT': [
                self.load_scaled_image('./grafiki/pacman/left_full.png', sf),
                self.load_scaled_image('./grafiki/pacman/left_half.png', sf),
                self.load_scaled_image('./grafiki/pacman/left_open.png', sf),
                self.load_scaled_image('./grafiki/pacman/left_half.png', sf)
            ],
            'RIGHT': [
                self.load_scaled_image('./grafiki/pacman/right_full.png', sf),
                self.load_scaled_image('./grafiki/pacman/right_half.png', sf),
                self.load_scaled_image('./grafiki/pacman/right_open.png', sf),
                self.load_scaled_image('./grafiki/pacman/right_half.png', sf)
            ],
            'DEATH': [
                self.load_scaled_image('./grafiki/pacman/death_0.png', sf),
                self.load_scaled_image('./grafiki/pacman/death_1.png', sf),
                self.load_scaled_image('./grafiki/pacman/death_2.png', sf),
                self.load_scaled_image('./grafiki/pacman/death_3.png', sf),
                self.load_scaled_image('./grafiki/pacman/death_4.png', sf),
                self.load_scaled_image('./grafiki/pacman/death_5.png', sf),
                self.load_scaled_image('./grafiki/pacman/death_6.png', sf),
                self.load_scaled_image('./grafiki/pacman/death_7.png', sf),
                self.load_scaled_image('./grafiki/pacman/death_8.png', sf),
                self.load_scaled_image('./grafiki/pacman/death_9.png', sf)
            ]
        }
        self.lives = 2

    def load_scaled_image(self, image_path, sf):
        image = pygame.image.load(image_path)
        return pygame.transform.scale(image, (36, 36))


    def draw(self, win):
        if self.alive and not self.level_end:
            images = self.sprites[self.current_direction]
            if self.tick >= 15:
                image = images[3]
            elif self.tick >= 10:
                image = images[2]
            elif self.tick >= 5:
                image = images[1]
            else:
                image = images[0]
        elif self.dying and not self.level_end:
            images = self.sprites['DEATH']
            if self.tick >= 70:
                self.dying = False
            elif self.tick >= 7:
                image = images[(self.tick - 7) // 7]
            else:
                image = images[0]
        else:
            images = self.sprites[self.current_direction]
            image = images[0]

        if self.dying or self.alive:
            win.blit(image, self.rect)
        else:
            self.start_reset = True


    def reset(self, r_lives):
        self.lives -= int(r_lives)
        self.x, self.y = self.start_pos
        self.rect.center = self.get_pos()
        self.alive = True
        self.current_direction = 'NONE'
        self.next_direction = 'NONE'
        self.powered = False
        self.powered_ticks = 0
        self.dot_counter = 0
        self.level_end = False
        self.dying = False
        self.tick = 0

    def get_score(self):
        return self.score

    def collide(self, grid_pos):
        dot_collision = dots.is_dot(grid_pos[0], grid_pos[1])
        super_collision = dots.is_super(grid_pos[0], grid_pos[1])



        if dot_collision or super_collision:
            dots.eat_dot(grid_pos[0], grid_pos[1])
            self.dot_counter += 1

            if dot_collision:
                eat_sound.play()
                self.score += 10
            else:
                powerup.play()
                self.score += 50
                self.powered = True
                self.powered_ticks = self.max_powered_ticks
                self.activated_powered = True



    def kill(self):

        self.alive = False
        self.dying = True
        self.tick = 0
        death.play()


    def get_lives(self):
        return self.lives

    def get_grid_coord(self, pos):
        x, y = pos
        turn_difference = 0.375 * self.sf
        direction = self.current_direction

        can_turn = (direction == 'UP' and (self.sf // 2) + turn_difference >= y % self.sf >= self.sf // 2) \
            or (direction == 'DOWN' and self.sf // 2 >= y % self.sf >= (self.sf // 2) - turn_difference) \
            or (direction == 'LEFT' and (self.sf // 2) + turn_difference >= x % self.sf >= self.sf // 2) \
            or (direction == 'RIGHT' and self.sf // 2 >= x % self.sf >= (self.sf // 2) - turn_difference) \
            or direction == 'NONE'

        distance = (int((x % self.sf) - self.sf // 2), int((y % self.sf) - self.sf // 2))
        x = int(x // self.sf)
        y = int(y // self.sf)

        return x, y, can_turn, distance


    def move(self):
        if self.alive:
            if self.can_turn() and self.next_direction != 'NONE':
                self.current_direction = self.next_direction

            if self.can_move(self.current_direction):
                x, y, can_turn, distance = self.get_grid_coord(self.get_pos())
                dx = -distance[0] if distance[0] != 0 and self.directions[self.current_direction][0] == 0 and not can_turn else 0
                dy = -distance[1] if distance[1] != 0 and self.directions[self.current_direction][1] == 0 and not can_turn else 0

                v = self.v * (self.temp_powered_velocity if self.powered else self.temp_velocity_modifier)

                self.x += (self.directions[self.current_direction][0] * v) + dx
                self.y += (self.directions[self.current_direction][1] * v) + dy
                self.rect.center = self.get_pos()

                self.activated_powered = False if self.activated_powered else self.activated_powered

                if self.x <= 0:
                    self.x = 28 * self.sf
                    self.rect.centerx = self.x
                elif self.x >= 28 * self.sf:
                    self.x = 0
                    self.rect.centerx = self.x

                self.tick = (self.tick + 1) if self.tick < 20 else 0
            else:
                self.tick = 5 if self.tick < 5 else self.tick

            self.collide(self.get_grid_coord(self.get_pos()))

            if self.powered_ticks > 0:
                self.powered_ticks -= 1
            else:
                self.powered = False
        elif self.dying:
            self.tick += 1
