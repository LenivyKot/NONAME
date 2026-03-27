import pygame
import random

pygame.init()

SIZE = 5
SUB = 3
CELL = 80
WIDTH = SIZE * CELL
HEIGHT = SIZE * CELL + 80

WHITE = (240,240,240)
BLACK = (30,30,30)
RED = (200,60,60)
BLUE = (60,120,200)
GRAY = (200,200,200)
GREEN = (0,255,0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kvadroteka")

font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 60)

sx = 1
sy = 1
win = False


def check_win(board):

    for x in range(SIZE):

        first = board[0][x]

        for y in range(SIZE):
            if board[y][x] != first:
                return False

    return True


def create_board():

    while True:

        cells = [0]*15 + [1]*10
        random.shuffle(cells)

        board = []
        index = 0

        for y in range(SIZE):
            row = []
            for x in range(SIZE):
                row.append(cells[index])
                index += 1
            board.append(row)

        if not check_win(board):
            return board


board = create_board()


def shuffle_board():
    global board, win
    board = create_board()
    win = False


def rotate_clockwise():
    global board

    sub = [row[sx:sx+SUB] for row in board[sy:sy+SUB]]
    rotated = [list(row) for row in zip(*sub[::-1])]

    for y in range(SUB):
        for x in range(SUB):
            board[sy+y][sx+x] = rotated[y][x]


def rotate_counter():
    global board

    sub = [row[sx:sx+SUB] for row in board[sy:sy+SUB]]
    rotated = [list(row) for row in zip(*sub)]
    rotated.reverse()

    for y in range(SUB):
        for x in range(SUB):
            board[sy+y][sx+x] = rotated[y][x]


def draw():

    screen.fill(WHITE)

    for y in range(SIZE):
        for x in range(SIZE):

            color = RED if board[y][x] == 0 else BLUE

            rect = pygame.Rect(x*CELL, y*CELL, CELL, CELL)

            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)

    highlight = pygame.Rect(sx*CELL, sy*CELL, CELL*SUB, CELL*SUB)
    pygame.draw.rect(screen, GREEN, highlight, 4)

    button = pygame.Rect(WIDTH//2-100, HEIGHT-60, 200, 40)
    pygame.draw.rect(screen, GRAY, button)

    text = font.render("Перемешать", True, BLACK)
    screen.blit(text, (button.x+25, button.y+5))

    if win:

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0,0,0))
        screen.blit(overlay,(0,0))

        msg = big_font.render("ПОБЕДА!", True, WHITE)
        screen.blit(msg,(WIDTH//2-120, HEIGHT//2-40))

    pygame.display.flip()

    return button


running = True

while running:

    button_rect = draw()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and not win:

            if event.key == pygame.K_LEFT:
                sx = max(0, sx-1)

            if event.key == pygame.K_RIGHT:
                sx = min(SIZE-SUB, sx+1)

            if event.key == pygame.K_UP:
                sy = max(0, sy-1)

            if event.key == pygame.K_DOWN:
                sy = min(SIZE-SUB, sy+1)

            if event.key == pygame.K_z:
                rotate_counter()

            if event.key == pygame.K_x:
                rotate_clockwise()

        if event.type == pygame.MOUSEBUTTONDOWN:

            if button_rect.collidepoint(event.pos):
                shuffle_board()

    if not win and check_win(board):
        win = True

pygame.quit()