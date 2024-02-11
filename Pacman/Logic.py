from Sprites import Sprite
from Trace import Node
import random


class Ghost(Sprite):

    def __init__(self, sf, x, y, v, grid):
        super().__init__(sf, x, y, v, grid)
        self.rect = self.image.get_rect()
        self.rect.center = (self.get_pos())
        self.current_direction = 'LEFT'
        self.previous_direction = 'NONE'
        self.scatter = True
        self.scatter_timings = [420, 1200, 420, 1200, 300, 1200, 300]
        self.scatter_frame = 0
        self.scatter_tick = 0
        self.scatter_step = 0
        self.frightened = False
        self.frightened_flash = 5
        self.frightened_ticks = 0
        self.frightened_velocity = 0.5
        self.reached_scatter = False
        self.previous_state = 'NORMAL'
        self.change_direction = False
        self.tunnel_velocity = 0.4
        self.velocity_modifier = 0.75
        self.dying_velocity = 1.5
        self.dead_velocity = 0.5
        self.alive = True
        self.dying = False
        self.respawning = False
        self.spawning = False
        self.counting_dots = False
        self.dot_counter = 0
        self.previous_dots = 0
        self.time_since_dot = 0
        self.global_dots = 0
        self.has_left = False


    def draw(self, win):
        if self.dying:
            image = self.sprites['DEAD'][self.current_direction]
        else:
            if self.frightened:
                images = self.sprites["FRIGHTENED"]
                if self.frightened_ticks >= self.frightened_flash * 30:
                    image = images[1] if self.tick >= 8 else images[0]
                else:
                    if self.frightened_ticks % 30 > 15:
                        image = images[1] if self.tick >= 8 else images[0]
                    else:
                        image = images[3] if self.tick >= 8 else images[2]
            else:
                images = self.sprites[self.current_direction]
                image = images[1] if self.tick >= 8 else images[0]

        win.blit(image, self.rect)

    def find_path(self, ex, ey, grid):
        open_set = []
        closed_set = []
        node_grid = [[None] * len(row) for row in grid]

        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] == 2:
                    node_grid[i][j] = Node(j, i)
                elif grid[i][j] == 1:
                    node_grid[i][j] = 1

        sx, sy, _ = self.get_grid_coord((self.x, self.y))
        start = Node(sx, sy)
        end = Node(ex, ey)
        node_grid[sy][sx] = start
        node_grid[ey][ex] = end
        path = []
        open_set.append(node_grid[sy][sx])

        start.t = 1

        for row in node_grid:
            for node in row:
                if node and node != 1:
                    node.find_neighbors(node_grid, self.previous_direction)

        while open_set:
            current = min(open_set, key=lambda node: node.f)

            if current == end:
                path = []
                temp = current
                while temp:
                    path.append(temp)
                    temp = temp.previous
                break

            open_set.remove(current)
            closed_set.append(current)

            for neighbor in current.neighbors:
                if neighbor in closed_set:
                    continue

                diff = abs(neighbor.x - current.x) + abs(neighbor.y - current.y)
                temp_g = current.g + diff

                if neighbor not in open_set:
                    open_set.append(neighbor)
                elif temp_g >= neighbor.g:
                    continue

                neighbor.previous = current
                neighbor.g = temp_g
                neighbor.h = abs(neighbor.x - end.x) + abs(neighbor.y - end.y)
                neighbor.f = neighbor.g + neighbor.h

        direction = 'NONE'
        if len(path) >= 2:
            next_node = path[-2]
            if next_node.x > start.x:
                direction = 'RIGHT'
            elif next_node.x < start.x:
                direction = 'LEFT'
            elif next_node.y > start.y:
                direction = 'DOWN'
            elif next_node.y < start.y:
                direction = 'UP'

        return direction


    def move(self, target, grid, target2=None):
        # Get current position and center coordinates
        x, y, centre = self.get_grid_coord(self.get_pos())
        
        # Check target states
        if target.activated_powered:
            self.frightened = True
        elif not target.powered:
            self.frightened = False
        
        # Update dot counters and time since last dot
        if target.dot_counter > self.previous_dots and self.counting_dots:
            self.previous_dots = target.dot_counter
            self.time_since_dot = 0
            if not self.counting_dots or self.global_dots <= 0:
                self.dot_counter += 1
            else:
                self.global_dots -= 1
        elif self.time_since_dot < 240 and self.counting_dots:
            self.time_since_dot += 1
        elif not self.counting_dots:
            self.time_since_dot = 0

        self.frightened_ticks = target.powered_ticks

        if self.alive:
            collision = self.collide(target)

            if self.previous_state == 'NORMAL':
                self.previous_state = 'SCATTER' if self.scatter else 'FRIGHTENED' if self.frightened else self.previous_state
            elif self.previous_state == 'SCATTER':
                self.previous_state = 'FRIGHTENED' if self.frightened else 'NORMAL' if not self.scatter else self.previous_state
            elif self.previous_state == 'FRIGHTENED':
                self.previous_state = 'NORMAL' if not (self.scatter or self.frightened) else 'SCATTER' if self.scatter and not self.frightened else self.previous_state

            if not self.frightened:
                # Handle non-frightened ghost movement
                if 'TURN' in collision:
                    if not self.scatter:
                        self.reached_scatter = False
                        self.scatter_frame = 0
                        tx, ty = self.get_target_pos(target, target2)
                    elif not self.reached_scatter:
                        tx, ty = self.scatter_coords[self.scatter_frame]
                        if x == tx and y == ty:
                            self.reached_scatter = True
                            self.scatter_frame += 1
                            tx, ty = self.scatter_coords[self.scatter_frame % len(self.scatter_coords)]
                    else:
                        self.scatter_frame += 1
                        tx, ty = self.scatter_coords[self.scatter_frame % len(self.scatter_coords)]
                    self.current_direction = self.find_path(tx, ty, grid)
                
                if self.change_direction and centre:
                    self.change_direction = False
                    available_directions = [direction for direction in self.directions if direction != self.current_direction]
                    for direction in available_directions:
                        dx, dy = x + self.directions[direction][0], y + self.directions[direction][1]
                        if grid[dy][dx] != 1:
                            self.current_direction = direction
                            break
                
                if 'COLLIDE' in collision:
                    target.kill()
                
                if self.current_direction != 'NONE':
                    self.previous_direction = self.current_direction
                
                d = self.directions[self.current_direction]
                
                if y == 14 and (x <= 5 or x >= 22):
                    v = self.v * self.tunnel_velocity
                else:
                    v = self.v * self.velocity_modifier
                
                self.x += d[0] * v
                self.y += d[1] * v
                self.rect.center = self.get_pos()
            else:
                # Handle frightened ghost movement
                if 'TURN' in collision:
                    directions = ['LEFT', 'RIGHT'] if self.current_direction in ['UP', 'DOWN'] else ['UP', 'DOWN']
                    random.shuffle(directions)
                    for direction in directions:
                        dx, dy = x + self.directions[direction][0], y + self.directions[direction][1]
                        if grid[dy][dx] != 1:
                            self.current_direction = direction
                            break

                if self.change_direction and centre:
                    self.change_direction = False
                    available_directions = [direction for direction in self.directions if direction != self.current_direction]
                    for direction in available_directions:
                        dx, dy = x + self.directions[direction][0], y + self.directions[direction][1]
                        if grid[dy][dx] != 1:
                            self.current_direction = direction
                            break

                else:
                    if 'COLLIDE' in collision:
                        self.dying = True
                        self.alive = False
                        self.frightened = False

                    if self.current_direction != 'NONE':
                        self.previous_direction = self.current_direction

                    dx, dy = self.directions[self.current_direction]
                    v = self.v * self.frightened_velocity
                    self.x += dx * v
                    self.y += dy * v
                    self.rect.center = self.get_pos()

                    # Wrap around the grid horizontally
                    if self.x <= 0 or self.x >= 28 * self.sf:
                        self.x = (self.x + 28 * self.sf) % (28 * self.sf)
                        self.rect.centerx = self.x

                    # Update ghost state if it has left the starting position
                    if not self.has_left:
                        diff = abs(y - 11) + abs(x - 13.5)
                        if diff > 2.5:
                            self.has_left = True
                    else:
                        self.counting_dots = False

            
        elif self.spawning:
            if self.dot_counter >= self.spawn_dots and self.counting_dots and self.global_dots <= 0:
                if self.x / self.sf < 14 and 14.6 > self.y / self.sf > 14.4:
                    self.current_direction = 'RIGHT'
                    v = self.v * self.dead_velocity
                    self.x += self.directions[self.current_direction][0] * v
                    self.y = 14.5 * self.sf
                    self.rect.center = self.get_pos()
                elif self.x / self.sf > 14 and 14.6 > self.y / self.sf > 14.4:
                    self.current_direction = 'LEFT'
                    v = self.v * self.dead_velocity
                    self.x += self.directions[self.current_direction][0] * v
                    self.y = 14.5 * self.sf
                    self.rect.center = self.get_pos()
                elif round(self.y / self.sf) > 11:
                    self.current_direction = 'UP'
                    v = self.v * self.dead_velocity
                    self.y += self.directions[self.current_direction][1] * v
                    self.rect.center = self.get_pos()
                else:
                    self.current_direction = 'LEFT'
                    self.counting_dots = False
                    self.spawning = False
                    self.alive = True
            else:
                if y >= 15:
                    self.current_direction = 'UP'
                elif y <= 13:
                    self.current_direction = 'DOWN'
                v = self.v * self.dead_velocity
                self.y += self.directions[self.current_direction][1] * v
                self.rect.center = self.get_pos()
            
            
        elif self.dying:
            # Handle dying ghost movement
            collision = self.collide(target)
            self.previous_state = 'NORMAL'

            # Check ghost position relative to the ghost house
            if self.is_above_ghost_house():
                self.handle_above_ghost_house()
            elif self.is_inside_ghost_house():
                self.handle_inside_ghost_house()

            # Not in ghost house or above it
            else:
                if 'TURN' in collision:
                    self.current_direction = self.find_path(14, 11, grid)

            if self.current_direction != 'NONE':
                self.previous_direction = self.current_direction
            d = self.directions[self.current_direction]
            v = self.v * self.dying_velocity
            self.x += d[0] * v
            self.y += d[1] * v
            self.rect.center = self.get_pos()

            if self.x <= 0:
                self.x = 28 * self.sf
                self.rect.centerx = self.x
            elif self.x >= 28 * self.sf:
                self.x = 0
                self.rect.centerx = self.x
            
        if self.respawning:
            pass

        # Update frightened state
        if not self.frightened:
            self.scatter_tick += 1
            if self.scatter_step < len(self.scatter_timings):
                if self.scatter_tick > self.scatter_timings[self.scatter_step]:
                    self.scatter_step += 1
                    self.scatter_tick = 0
                    self.scatter = not self.scatter
            else:
                self.scatter = False

        # Update ticks and frightened state
        self.tick = (self.tick + 1) % 17
        if self.frightened_ticks > 0:
            self.frightened_ticks -= 1
        else:
            self.frightened = False

    def collide(self, target):
        x, y, centre = self.get_grid_coord(self.get_pos())
        tx, ty, _, _ = target.get_grid_coord(target.get_pos())
        response = []

        if self.grid[y][x] == 2 and centre:
            response.append('TURN')

        if self.is_colliding(x, y, tx, ty, target.alive):
            response.append('COLLIDE')

        return response

    def is_colliding(self, x, y, tx, ty, is_target_alive):
        return x == tx and y == ty and is_target_alive

    # In ghost house
    def is_above_ghost_house(self):
        return 14.1 >= self.x / self.sf >= 13.9 and 14.5 > self.y / self.sf >= 10.5

    def is_inside_ghost_house(self):
        return 15 > self.x / self.sf > 12 and 15 > self.y / self.sf > 13

    def handle_above_ghost_house(self):
        self.x = 14 * self.sf
        self.current_direction = 'DOWN'

    def handle_inside_ghost_house(self):
        if self.spawn_coords == 0:
            self.current_direction = 'NONE'
            self.dying = False
            self.spawning = True
            self.counting_dots = True
        elif self.spawn_coords < 0:
            if self.x / self.sf > 12.5:
                self.current_direction = 'LEFT'
            else:
                self.x = 12.5 * self.sf
                self.dying = False
                self.spawning = True
                self.counting_dots = True
        else:
            if self.x / self.sf < 14.5:
                self.current_direction = 'RIGHT'
            else:
                self.x = 14.5 * self.sf
                self.dying = False
                self.spawning = True
                self.counting_dots = True

    def reset_level(self):
        self.x, self.y = self.start_pos
        self.rect.center = self.get_pos()
        self.current_direction = 'NONE'
        self.frightened = False
        self.frightened_ticks = 0
        self.previous_state = 'NORMAL'
        self.scatter = True
        self.scatter_frame = 0
        self.scatter_tick = 0
        self.scatter_step = 0
        self.has_left = False
        self.counting_dots = False
        self.dot_counter = 0
        self.previous_dots = 0
        self.time_since_dot = 0
        self.global_dots = 0
        self.dying = False

    def reset(self):
        self.reset_level()

