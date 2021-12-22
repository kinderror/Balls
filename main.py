import pygame
import math
import pygame.draw as draw
from random import randint

pygame.init()
screen = pygame.display.set_mode((1200, 700))
points_font = pygame.font.Font(None, 100)
time_font = pygame.font.Font(None, 70)
end_font = pygame.font.Font(None, 150)
FPS = 60
# initial parameters
points = 0
time = 59
amount = 7
# colors
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]
main_color = BLACK
# create list of balls
balls = {i + 1: {'x': 0, 'y': 0, 'r': 0, 'v_x': 0, 'v_y': 0, 'color': 0} for i in range(amount)}


def get_point(x_0, y_0):
    """this function calculates whether you got a point or not"""
    N = 0
    for i in range(amount):
        R = math.hypot(balls[i + 1]['x'] - x_0, balls[i + 1]['y'] - y_0)
        if int(R) < balls[i + 1]['r'] and N == 0:
            N = i + 1
    return N


def parameters(N):
    """this function changes all parameters of N-th ball"""
    global balls
    balls[N]['x'] = randint(200, 1000)
    balls[N]['y'] = randint(200, 500)
    balls[N]['r'] = randint(10, 100)
    balls[N]['v_x'] = randint(-7, 7)
    balls[N]['v_y'] = randint(-7, 7)
    balls[N]['color'] = COLORS[randint(0, 5)]


def wall(x, y, r, v_x, v_y):
    """this function calculates how the ball reflects of the wall"""
    if x < r or x > 1200 - r:
        v_x = -v_x
    if y < r or y > 700 - r:
        v_y = -v_y
    return v_x, v_y


def what_color():
    """this functions shows whether you have collected the same colors or not """
    global balls
    same_color = True
    color_1 = balls[1]['color']
    for i in range(amount):
        if balls[i+1]['color'] != color_1:
            same_color = False
    return same_color


# set the balls' parameters
for i in range(amount):
    parameters(i + 1)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            N = get_point(event.pos[0], event.pos[1])
            if N != 0:
                points += 1
                parameters(N)
    screen.fill(WHITE)
    # calculate all balls' motion
    for i in range(amount):
        i = amount - i
        circ = balls[i]
        draw.circle(screen, circ['color'], (circ['x'], circ['y']), circ['r'])
        balls[i]['v_x'], balls[i]['v_y'] = wall(circ['x'], circ['y'], circ['r'], circ['v_x'], circ['v_y'])
        balls[i]['x'] += balls[i]['v_x']
        balls[i]['y'] += balls[i]['v_y']
    # give points for same color of balls
    if what_color() and balls[1]['color'] != main_color:
        points += 50
        main_color = balls[1]['color']
    # see whether game is over or not
    if time <= 0:
        finished = True
    points_text = points_font.render(str(points), 1, BLACK)
    screen.blit(points_text, (50, 50))
    time_text = time_font.render('00:' + str(int(time)//10) + str(int(time) % 10), 1, BLACK)
    screen.blit(time_text, (535, 50))
    time -= 1 / FPS
    pygame.display.update()

# final screen
screen.fill(WHITE)
end_text = end_font.render('Well played!', 1, BLACK)
screen.blit(end_text, (290, 200))
points_text = points_font.render('Your score: ' + str(points), 1, BLACK)
screen.blit(points_text, (370, 320))
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
    pygame.display.update()
pygame.quit()
