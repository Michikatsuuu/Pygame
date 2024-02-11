from Logic import Ghost
import pygame


class Brown(Ghost):
        def __init__(self, sf, x, y, v, grid):
            self.scatter_coords = [(1, 29), (12, 29), (12, 26), (9, 26), (9, 23), (6, 23), (6, 26), (1, 26)]
            self.spawn_coords = 1
            self.spawn_dots = 60
            self.respawn_dots = 32
            self.current_direction = 'UP'
            self.image = self.load_image('./grafiki/orange_ghost/down_1.png', sf)
            self.sprites = {
                'NONE': [
                    self.load_image('./grafiki/orange_ghost/down_1.png', sf),
                    self.load_image('./grafiki/orange_ghost/down_2.png', sf),
                ],
                'UP': [
                    self.load_image('./grafiki/orange_ghost/up_1.png', sf),
                    self.load_image('./grafiki/orange_ghost/up_2.png', sf),
                ],
                'DOWN': [
                    self.load_image('./grafiki/orange_ghost/down_1.png', sf),
                    self.load_image('./grafiki/orange_ghost/down_2.png', sf),
                ],
                'LEFT': [
                    self.load_image('./grafiki/orange_ghost/left_1.png', sf),
                    self.load_image('./grafiki/orange_ghost/left_2.png', sf),
                ],
                'RIGHT': [
                    self.load_image('./grafiki/orange_ghost/right_1.png', sf),
                    self.load_image('./grafiki/orange_ghost/right_2.png', sf),
                ],
                'FRIGHTENED': [
                    self.load_image('./grafiki/other/vulnerable_1.png', sf),
                    self.load_image('./grafiki/other/vulnerable_2.png', sf),
                    self.load_image('./grafiki/other/vulnerable_3.png', sf),
                    self.load_image('./grafiki/other/vulnerable_4.png', sf),
                ],
                'DEAD': {
                    'UP': self.load_image('./grafiki/other/up_eyes.png', sf),
                    'DOWN': self.load_image('./grafiki/other/down_eyes.png', sf),
                    'LEFT': self.load_image('./grafiki/other/left_eyes.png', sf),
                    'RIGHT': self.load_image('./grafiki/other/right_eyes.png', sf),
                    'NONE': self.load_image('./grafiki/other/down_eyes.png', sf),
                }
            }
            super().__init__(sf, x, y, v, grid)

        def load_image(self, path, sf):
            return pygame.transform.scale(pygame.image.load(path), (30, 30))

        def get_target_pos(self, target, target2):
            x, y, _, _ = target.get_grid_coord((target.x, target.y))
            sx, sy, _ = self.get_grid_coord((self.x, self.y))
            diff = abs(sx - x) + abs(sy - y)
            if diff >= 8:
                tx, ty = x, y
            elif sx != 1 and sy != 29:
                tx, ty = 1, 29
            else:
                tx, ty = 9, 23
            return tx, ty

        def set_spawn_dots(id):
            spawn_dots = 60 if id == 1 else (50 if id == 2 else 0)

class Blue(Ghost):
    def __init__(self, sf, x, y, v, grid):
        self.scatter_coords = [(26, 29), (15, 29), (15, 26), (18, 26), (18, 23), (21, 23), (21, 26), (26, 26)]
        self.spawn_coords = -1
        self.spawn_dots = 30
        self.respawn_dots = 17
        self.current_direction = 'UP'
        self.image = self.load_image('./grafiki/blue_ghost/down_1.png', sf)
        self.sprites = {
            'NONE': [
                self.load_image('./grafiki/blue_ghost/down_1.png', sf),
                self.load_image('./grafiki/blue_ghost/down_2.png', sf),
            ],
            'UP': [
                self.load_image('./grafiki/blue_ghost/up_1.png', sf),
                self.load_image('./grafiki/blue_ghost/up_2.png', sf),
            ],
            'DOWN': [
                self.load_image('./grafiki/blue_ghost/down_1.png', sf),
                self.load_image('./grafiki/blue_ghost/down_2.png', sf),
            ],
            'LEFT': [
                self.load_image('./grafiki/blue_ghost/left_1.png', sf),
                self.load_image('./grafiki/blue_ghost/left_2.png', sf),
            ],
            'RIGHT': [
                self.load_image('./grafiki/blue_ghost/right_1.png', sf),
                self.load_image('./grafiki/blue_ghost/right_2.png', sf),
            ],
            'FRIGHTENED': [
                self.load_image('./grafiki/other/vulnerable_1.png', sf),
                self.load_image('./grafiki/other/vulnerable_2.png', sf),
                self.load_image('./grafiki/other/vulnerable_3.png', sf),
                self.load_image('./grafiki/other/vulnerable_4.png', sf),
            ],
            'DEAD': {
                'UP': self.load_image('./grafiki/other/up_eyes.png', sf),
                'DOWN': self.load_image('./grafiki/other/down_eyes.png', sf),
                'LEFT': self.load_image('./grafiki/other/left_eyes.png', sf),
                'RIGHT': self.load_image('./grafiki/other/right_eyes.png', sf),
                'NONE': self.load_image('./grafiki/other/down_eyes.png', sf),
            }
        }
        super().__init__(sf, x, y, v, grid)

    def load_image(self, path, sf):
        return pygame.transform.scale(pygame.image.load(path), (30, 30))

    def get_target_pos(self, target, target2):
        bx, by, _ = target2.get_grid_coord((target2.x, target2.y))
        px, py, _, _ = target.get_grid_coord((target.x, target.y))
        dx, dy = target.directions[target.current_direction]
        x, y = px + (dx * 2), py + (dy * 2)
        tx, ty = bx + ((x - bx) * 2), by + ((y - by) * 2)
        
        tx = max(0, min(tx, len(self.grid[0]) - 1))
        ty = max(0, min(ty, len(self.grid) - 1))
        
        while self.grid[ty][tx] == 1:
            if tx != px:
                tx += 1 if tx < px else -1
            elif ty != py:
                ty += 1 if ty < py else -1
        
        return tx, ty

    def set_spawn_dots(self, id):
        self.spawn_dots = 30 if id <= 1 else 0

class Pink(Ghost):
    def __init__(self, sf, x, y, v, grid):
        self.scatter_coords = [(1, 1), (1, 5), (6, 5), (6, 1)]
        self.spawn_coords = 0
        self.spawn_dots = 0
        self.respawn_dots = 7
        self.current_direction = 'DOWN'
        self.image = self.load_image('./grafiki/pink_ghost/down_1.png', sf)
        self.sprites = {
            'NONE': [
                self.load_image('./grafiki/pink_ghost/down_1.png', sf),
                self.load_image('./grafiki/pink_ghost/down_2.png', sf),
            ],
            'UP': [
                self.load_image('./grafiki/pink_ghost/up_1.png', sf),
                self.load_image('./grafiki/pink_ghost/up_2.png', sf),
            ],
            'DOWN': [
                self.load_image('./grafiki/pink_ghost/down_1.png', sf),
                self.load_image('./grafiki/pink_ghost/down_2.png', sf),
            ],
            'LEFT': [
                self.load_image('./grafiki/pink_ghost/left_1.png', sf),
                self.load_image('./grafiki/pink_ghost/left_2.png', sf),
            ],
            'RIGHT': [
                self.load_image('./grafiki/pink_ghost/right_1.png', sf),
                self.load_image('./grafiki/pink_ghost/right_2.png', sf),
            ],
            'FRIGHTENED': [
                self.load_image('./grafiki/other/vulnerable_1.png', sf),
                self.load_image('./grafiki/other/vulnerable_2.png', sf),
                self.load_image('./grafiki/other/vulnerable_3.png', sf),
                self.load_image('./grafiki/other/vulnerable_4.png', sf),
            ],
            'DEAD': {
                'UP': self.load_image('./grafiki/other/up_eyes.png', sf),
                'DOWN': self.load_image('./grafiki/other/down_eyes.png', sf),
                'LEFT': self.load_image('./grafiki/other/left_eyes.png', sf),
                'RIGHT': self.load_image('./grafiki/other/right_eyes.png', sf),
                'NONE': self.load_image('./grafiki/other/down_eyes.png', sf),
            }
        }
        super().__init__(sf, x, y, v, grid)

    def load_image(self, path, sf):
        return pygame.transform.scale(pygame.image.load(path), (30, 30))

    def get_target_pos(self, target):
        tx, ty, _, _ = target.get_grid_coord((target.x, target.y))
        direction = target.directions[target.current_direction]
        
        for i in range(4, -1, -1):
            x = tx + (direction[0] * i)
            y = ty + (direction[1] * i)
            
            if 0 <= y < len(self.grid) and 0 <= x < len(self.grid[y]):
                if self.grid[y][x] != 1:
                    tx, ty = x, y
                    break
        
        return tx, ty

    def set_spawn_dots(self, id):
        self.spawn_dots = 0


class Red(Ghost):
    def __init__(self, sf, x, y, v, grid):
        self.scatter_coords = [(26, 1), (26, 5), (21, 5), (21, 1)]
        self.spawn_coords = 0
        self.spawn_dots = 0
        self.respawn_dots = 0
        self.image = self.load_image('./grafiki/red_ghost/down_1.png', sf)
        self.sprites = {
            'NONE': [
                self.load_image('./grafiki/red_ghost/down_1.png', sf),
                self.load_image('./grafiki/red_ghost/down_2.png', sf),
            ],
            'UP': [
                self.load_image('./grafiki/red_ghost/up_1.png', sf),
                self.load_image('./grafiki/red_ghost/up_2.png', sf),
            ],
            'DOWN': [
                self.load_image('./grafiki/red_ghost/down_1.png', sf),
                self.load_image('./grafiki/red_ghost/down_2.png', sf),
            ],
            'LEFT': [
                self.load_image('./grafiki/red_ghost/left_1.png', sf),
                self.load_image('./grafiki/red_ghost/left_2.png', sf),
            ],
            'RIGHT': [
                self.load_image('./grafiki/red_ghost/right_1.png', sf),
                self.load_image('./grafiki/red_ghost/right_2.png', sf),
            ],
            'FRIGHTENED': [
                self.load_image('./grafiki/other/vulnerable_1.png', sf),
                self.load_image('./grafiki/other/vulnerable_2.png', sf),
                self.load_image('./grafiki/other/vulnerable_3.png', sf),
                self.load_image('./grafiki/other/vulnerable_4.png', sf),
            ],
            'DEAD': {
                'UP': self.load_image('./grafiki/other/up_eyes.png', sf),
                'DOWN': self.load_image('./grafiki/other/down_eyes.png', sf),
                'LEFT': self.load_image('./grafiki/other/left_eyes.png', sf),
                'RIGHT': self.load_image('./grafiki/other/right_eyes.png', sf),
                'NONE': self.load_image('./grafiki/other/down_eyes.png', sf),
            }
        }
        super().__init__(sf, x, y, v, grid)

    def load_image(self, path, sf):
        return pygame.transform.scale(pygame.image.load(path), (30, 30))

    def get_target_pos(self, target, target2):
        tx, ty, _, _ = target.get_grid_coord((target.x, target.y))
        return tx, ty

    def set_spawn_dots(self, id):
        self.spawn_dots = 0