import pygame
import random
import sys


CELL_SIZE   = 8          # rozmiar jednej komórki w pikselach
COLS        = 120        # liczba kolumn
ROWS        = 90         # liczba wierszy
WIDTH       = COLS * CELL_SIZE
HEIGHT      = ROWS * CELL_SIZE
FPS         = 15

# % 
P_TREE      = 0.05     # szansa wyrostu nowego drzewa na pustym polu
P_IGNITE    = 0.0001     # szansa spontanicznego zapłonu drzewa
P_THREE_SPAWN = 0 # procent drzew na nowo wygenerowanej planszy


EMPTY       = 0
TREE        = 1
BURNING     = 2

# Kolory
COLOR_BG      = (20,  20,  20)
COLOR_EMPTY   = (40,  30,  20)    # ziemia
COLOR_TREE    = (34, 139,  34)    # zielony
COLOR_BURNING = (255,  80,   0)   # ogień
COLOR_BURNING2  = (200,  50,   0)   # drugi kolor ognia


# tworzenie siatki 
def make_grid():

    grid = []
    for a in range(ROWS):        # dla każdego wiersza
        row = []
        for a in range(COLS):    # dla każdej kolumny
            if random.random() < P_THREE_SPAWN:
                row.append(TREE)
            else:
                row.append(EMPTY)
        grid.append(row)
    return grid




def step(grid):

    new_grid = []
    for a in range(ROWS):
        row = [EMPTY] * COLS        # następny stan planszy 
        new_grid.append(row)

    for r in range(ROWS):
        for c in range(COLS):
            state = grid[r][c]

            if state == BURNING:
                # spalone pole 
                new_grid[r][c] = EMPTY

            elif state == TREE:
                # sprawdzanie czy któryś sąsiad płonie
                if has_burning_neighbor(grid, r, c):
                    new_grid[r][c] = BURNING
                # spontaniczny zapłon
                elif random.random() < P_IGNITE:
                    new_grid[r][c] = BURNING
                else:
                    new_grid[r][c] = TREE

            else:  # magia natury
                
                if random.random() < P_TREE:
                    new_grid[r][c] = TREE
                else:
                    new_grid[r][c] = EMPTY

    return new_grid


def has_burning_neighbor(grid, r, c):
    
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            nr = r + dr
            nc =  c + dc
            if 0 <= nr < ROWS and 0 <= nc < COLS:
                if grid[nr][nc] == BURNING:
                    return True
    return False

#RYsowanie
def draw(surface, grid):
    surface.fill(COLOR_BG)

    for r in range(ROWS):
        for c in range(COLS):
            state = grid[r][c]

            if state == EMPTY:
                color = COLOR_EMPTY
            elif state == TREE:
                color = COLOR_TREE
            else:
                # dodać migotanie ognia
                color = COLOR_BURNING 

            rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1)
            pygame.draw.rect(surface, color, rect)


# Wyświetlanie statystyk
def draw_hud(surface, font, grid, paused, generation):
    trees   = sum(row.count(TREE)    for row in grid)
    burning = sum(row.count(BURNING) for row in grid)
    total   = ROWS * COLS

    info = (
        f"Gen: {generation}   "
        f"Drzewa: {trees} ({100*trees//total}%)   "
        f"Pożary: {burning} ({100*burning//total}%)  "
        f"{'[ PAUZA ]' if paused else ''}"   #
    )
    text = font.render(info, True, (220, 220, 220))
    # tło pod tekstem
    bg = pygame.Surface((text.get_width() + 10, text.get_height() + 6), pygame.SRCALPHA)
    bg.fill((0, 0, 0, 160))
    surface.blit(bg,   (5, 5))
    surface.blit(text, (10, 8))

   


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Syzyf")
    clock  = pygame.time.Clock()
    font   = pygame.font.SysFont("consolas", 14)
    pause_status = True
    grid       = make_grid()
    paused     = False
    generation = 0
    speed      = FPS         # ilość zdarzeń na sekunde

    while True:
        # obsługa zdarzeń
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    paused = not paused
                if event.key == pygame.K_r:
                    grid = make_grid()
                    generation = 0
                if event.key in (pygame.K_PLUS , pygame.K_EQUALS):
                    speed = min(speed + 5, 120)
                if event.key == pygame.K_MINUS:
                    speed = max(speed - 5, 1)
 
            # Thor
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                mouse_x = pos[0]
                mouse_y = pos[1]

                col = mouse_x // CELL_SIZE
                row = mouse_y // CELL_SIZE

                if row >= 0 and row < ROWS:
                    if col >= 0 and col < COLS:
                        grid[row][col] = BURNING

        
        

        
        if not paused:
            grid = step(grid)
            generation += 1

        # wyświetlanie 
        draw(screen, grid)
        draw_hud(screen, font, grid, paused, generation)
        pygame.display.flip()
        clock.tick(speed)


if __name__ == "__main__":
    main()