import pygame
import colorsys
import time
import asset
import numpy as np

"""
I'm sorry for this bad code, this is my first time working with pygame. 
"""

assets = {}
size = (6,6)
px_size = (20,20)
keeps_alive_range = range(2,4)
birth_range = range(3,4)
game_board = np.zeros(size, dtype=bool)
game_board[2:5,5:6] = True
nb_grid = np.zeros(size)
run = True
tps = 2
mspt = 1/tps

def init():
    pygame.init()
    load_assets()
    screen = pygame.display.set_mode((size[0]*px_size[0],size[1]*px_size[1]))
    pygame.display.set_caption("Game of Life")
    pygame.display.set_icon(pygame.image.load("Icon.png"))
    game_loop(screen, pygame.time.Clock())

def load_assets() -> None:
    pass

def game_loop(screen:pygame.display, clock:pygame.time.Clock) -> None:
    global mspt,tps
    cnt = 0
    t0 = time.time()
    while (True):
        while (time.time()-t0 < mspt):
            do_redraw = handle_events()
            if (do_redraw):
                redraw(screen)
        t0 = time.time()
        mspt = 1/tps
        if (run):
            cnt += 1
            tick(screen, cnt)
        redraw(screen)
        #clock.tick(4)

def tick(screen:pygame.display, cnt:int) -> None:
    global game_board
    new_board = game_board.copy()
    grid = game_board
    loop = True
    if (loop):
        grid = extend_grid(grid)
    for y in range(size[0]):
        for x in range(size[1]):
            new_board[x,y] = update(x+loop,y+loop, grid)
            nb_grid[x,y] = count_adjacent(x+loop, y+loop, grid)
    #print(nb_grid)
    game_board = new_board

def redraw(screen:pygame.display) -> None:
    screen.fill(((not run)*255,0,0))
    [[draw(x,y, screen) for x in range(size[1])]for y in range(size[0])]
    pygame.display.update()


def update(x:int, y:int, grid:np.array, loop:bool=False) -> None:
    adj = count_adjacent(x, y, grid, loop)
    if (grid[x,y]):
        if (adj not in keeps_alive_range):
            return False
        return True
    else:
        if (adj in birth_range):
            return True
        return False

def draw(x:int, y:int, screen:pygame.display) -> None:
    if (game_board[x][y]):
        pygame.draw.rect(screen, (255,255,255,255), pygame.Rect(x*px_size[0], y*px_size[1], px_size[0], px_size[1]))


def count_adjacent(x:int, y:int, grid:np.array, loop:bool=False) -> int:
    size = grid.shape
    adj = np.sum(
        grid[
            max(x-1, 0) : min(x+2,size[0]),
            max(y-1, 0) : min(y+2,size[1])
        ]
    )
    return adj-grid[x,y]

def extend_grid(grid:np.array):
    shape = [i+2 for i in np.shape(grid)]
    tmp = np.zeros(shape, dtype=bool)
    #copy main
    tmp[1:-1,1:-1] = grid

    #copy horizontal
    tmp[1:-1, 0] = grid[:, -1]
    tmp[1:-1, -1] = grid[:, 0]

    #copy vertical
    tmp[0, 1:-1] = grid[-1, :]
    tmp[-1, 1:-1] = grid[0, :]

    #copy corners
    tmp[0,0] = grid[-1,-1]
    tmp[-1,-1] = grid[0,0]
    tmp[-1,0] = grid[0,-1]
    tmp[0,-1] = grid[-1,0]
    return tmp


def handle_events() -> bool:
    global run, tps, game_board
    ret = False
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            exit(0)
        elif (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_SPACE):
                run = not run
            elif (event.key == pygame.K_BACKSPACE):
                print("resetting")
                game_board = np.zeros(game_board.shape, dtype=bool)
                ret = True
            elif (event.key == pygame.K_r):
                print("randomizing")
                game_board = np.random.choice((True,False), size=game_board.shape)
                ret = True
        elif (event.type == pygame.MOUSEBUTTONDOWN):
            abs_pos = pygame.mouse.get_pos()
            pos = abs_pos[0]//px_size[0],abs_pos[1]//px_size[1]
            if (event.button == 1):
                print("spawning")
                game_board[pos[0],pos[1]] = True
            elif (event.button == 3):
                print("deleting")
                game_board[pos[0],pos[1]] = False
            elif (event.button == 4):
                tps += 1
            elif (event.button == 5):
                if (tps <= 1):
                    tps /= 2
                else:
                    tps -= 1
    return ret

def draw_assets(screen:pygame.display):
    for (name, asset) in assets.items():
        screen.blit(asset.get_image(), asset.get_pos)
        pygame.display.update()

def hsv2rgb(h:int, s:float, v:float) -> tuple:
    return tuple(i*255 for i in colorsys.hsv_to_rgb(h/360, s, v))

if __name__ == "__main__":
    init()