class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.t = 0
        self.forbidden_directions = [(12, 11), (12, 23), (15, 11), (15, 23)]
        self.neighbors = []
        self.previous = None

    def find_neighbors(self, node_grid, direction):
        x, y = self.x, self.y

        def add_neighbor(node):
            if node and node != 1:
                self.neighbors.append(node)

        if self.t != 1 or direction != 'LEFT':
            i = x + 1
            while i < len(node_grid[y]):
                neighbor = node_grid[y][i]
                add_neighbor(neighbor)
                if neighbor:
                    break
                i += 1

        # UP direction
        if self.t != 1 or direction != 'UP':
            i = y + 1
            while i < len(node_grid):
                neighbor = node_grid[i][x]
                add_neighbor(neighbor)
                if neighbor:
                    break
                i += 1

        # RIGHT direction
        if self.t != 1 or direction != 'RIGHT':
            i = x - 1
            while i >= 0:
                neighbor = node_grid[y][i]
                add_neighbor(neighbor)
                if neighbor:
                    break
                i -= 1

        # DOWN direction
        if not (self.t == 1 and direction == 'DOWN') or (x, y) in self.forbidden_directions:
            i = y - 1
            while i >= 0:
                neighbor = node_grid[i][x]
                add_neighbor(neighbor)
                if neighbor:
                    break
                i -= 1
