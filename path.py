import pygame
import math
from queue import PriorityQueue


WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))

pygame.display.set_caption("A* Search Algorithm")


RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
CYAN = (0, 255, 255)


class Cube:
    """
    draws cubes, creates begining, ends, and barricades
    and changes the color of cubes while path finding
    """
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def closed(self):
        return self.color == RED

    def opened(self):
        return self.color == GREEN

    def barricade(self):
        return self.color == BLACK

    def starting(self):
        return self.color == ORANGE

    def ending(self):
        return self.color == CYAN

    def reset(self):
        self.color == WHITE

    def create_start(self):
        self.color = ORANGE

    def close_path(self):
        self.color = RED

    def open_path(self):
        self.color = GREEN

    def barricade_path(self):
        self.color = BLACK
    
    def end_path(self):
        self.color = CYAN

    def create_path(self):
        self.color = PURPLE



    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        """
        UP, DOWN, LEFT, AND RIGHT
        """
        self.neighbors = []
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
			self.neighbors.append(grid[self.row - 1][self.col])

        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
			self.neighbors.append(grid[self.row + 1][self.col])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
			self.neighbors.append(grid[self.row][self.col - 1])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
			self.neighbors.append(grid[self.row][self.col + 1])

    def less_than(self, other):
        """
        compares two cubes to each other
        """
        return False


def h(c1, c2):
    """
    heurisitc function for the algorithm
    """
    x1, y1 = c1
    x2, y2 = c2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.create_path()
		draw()

def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {cube: float('inf') for row in grid for cube in row}
    g_score[start] = 0
    f_score = {cube: float('inf') for row in grid for cube in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.end_path()
            return True

        for neighbor in current.neighbors:
            tmp_g_score = g_score[current] + 1

            if tmp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tmp_g_score
                f_score[neighbor] = tmp_g_score + h(neighbor.get_pos(), end.get_pos())

                if neighbor not in set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set.hash.add(neighbor)
                    neighbor.open_path()

        draw()

        if current != start:
            current.close_path()

    return False

def create_grid(rows, width):
    grid = []
    gap = width // rows

    for i in range(rows):
        grid.append([])
        for j in range(rows):
            cube = Cube(i, j, gap, rows)
            grid[i].append(cube)
    
    return grid

def draw_grid(win, rows, width):
    gap = width // rows

    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for cube in row:
            cube.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col

def main(win, width):
    ROWS = 50
    grid = create_grid(ROWS, width)

    start = None
    end = None

    run = True
    while run:
        draw(win, grid, ROWS, width)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                cube = grid[row][col]

                if not start and cube != end:
                    start = cube
                    cube.create_start()

                elif not end and cube != start:
                    end = cube
                    end.end_path()
                
                elif cube != end and cube != start:
                    cube.barricade_path()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                cube = grid[row][col]
                cube.reset()

                if cube == start:
                    start = None
                
                elif cube == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for cube in row:
                            cube.update_neighbors(grid)
                    
                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
                
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = create_grid(ROWS, width)

    pygame.quit()

main(WIN, WIDTH)
