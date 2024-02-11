class Sprite:
    #унаслідування для всіх спрайтів

    def __init__(self, sf, x, y, v, grid):
        self.sf = sf  # Scale factor
        self.grid = grid
        self.v = v  # Velocity
        self.tick = 0
        self.start_pos = self.calculate_position(x, y)
        self.alive = True
        self.dying = False
        self.directions = {'LEFT': (-1, 0), 'RIGHT': (1, 0), 'UP': (0, -1), 'DOWN': (0, 1), 'NONE': (0, 0)}
        self.current_direction = 'NONE'
        self.next_direction = 'NONE'
        self.x, self.y = self.start_pos

    def calculate_position(self, x, y):
        return (int((x * self.sf) + (self.sf // 2)), (y * self.sf) + (self.sf // 2))

    def update_next_direction(self, direction):
        if direction == self.current_direction:
            return

        self.next_direction = direction

        nx, ny = self.directions[self.next_direction]
        cx, cy = self.directions[self.current_direction]

        if (nx + cx, ny + cy) == (0, 0):
            self.current_direction = self.next_direction
            self.next_direction = 'NONE'
       

    def is_alive(self):
        return self.alive == True

    def get_pos(self):
        return self.x, self.y

    def get_grid_coord(self, pos):
        x, y = pos
        centre = False
        extra = 2.5
        sf_div_2 = self.sf // 2
        x_mod_sf = x % self.sf
        y_mod_sf = y % self.sf
        current_direction_1 = self.directions[self.current_direction][1]
        current_direction_0 = self.directions[self.current_direction][0]
        
        if (sf_div_2 + extra >= x_mod_sf >= sf_div_2 - extra and current_direction_1 == 0) or (sf_div_2 + extra >= y_mod_sf >= sf_div_2 - extra and current_direction_0 == 0):
            self.rect.center = self.get_pos()
            centre = True
        
        x = int(x // self.sf)
        y = int(y // self.sf)
        
        return x, y, centre


    def can_move(self, direction):
        x, y, centre, _ = self.get_grid_coord((self.x, self.y))
        cx, cy = self.directions[direction]
        newx = cx + x
        newy = cy + y
        
        return not (self.grid[newy][newx] == 1 and centre)


    def can_turn(self):
        x, y, centre, _ = self.get_grid_coord((self.x, self.y))
        
        return self.grid[y][x] == 2 and centre and self.can_move(self.next_direction)


    def kill(self):
        pass
