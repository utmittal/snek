import pygame
import random

print("Hello World")

SC_X = 400
SC_Y = 400
SN_W = 20
TICK = pygame.USEREVENT+1
TICK_time = 500

snake = []
food = None
direction = (0, -SN_W)

def init_snake():
    # start snake roughly in middle of screen and two more boxes below
    snake.append(pygame.Rect(SC_X/2, SC_Y/2, SN_W, SN_W))
    snake.append(pygame.Rect(SC_X/2, SC_Y/2 + SN_W, SN_W, SN_W))
    snake.append(pygame.Rect(SC_X/2 , SC_Y/2 + SN_W + SN_W, SN_W, SN_W))

def new_food():
    global food

    food_x = random.randint(0, (SC_X-SN_W)/SN_W) * SN_W
    food_y = random.randint(0, (SC_Y-SN_W)/SN_W) * SN_W

    food = pygame.Rect(food_x, food_y, SN_W, SN_W)

def draw_snake_and_food(screen):
    for rectangle in snake:
        pygame.draw.rect(screen, pygame.Color("white"), rectangle)
    pygame.draw.rect(screen, pygame.Color("red"), food)

def set_direction(key):
    global direction

    if key == pygame.K_LEFT:
        direction = (-SN_W, 0)
    if key == pygame.K_RIGHT:
        direction = (SN_W, 0)
    if key == pygame.K_UP:
        direction = (0, -SN_W)
    if key == pygame.K_DOWN:
        direction = (0, SN_W)

def move_snake():
    snake.insert(0, snake[0].move(direction[0], direction[1]))
    snake.pop(-1)

def check_collision_self():
    if snake[0].collidelistall(snake[1:]):
        return True

def check_collision_walls():
    if snake[0].top < 0 or snake[0].bottom > SC_Y or snake[0].left < 0 or snake[0].right > SC_X:
        return True

def check_collision_food():
    if snake[0].colliderect(food):
        return True

def eat_food():
    snake.append(food)
    new_food()

def start():
    # initialize the pygame module
    pygame.init()
    screen = pygame.display.set_mode((SC_X, SC_Y))
    pygame.time.set_timer(TICK, TICK_time)

    #initialize snake and food
    init_snake()
    new_food()

    while True:
        # clear screen
        screen.fill((0,0,0))

        for event in pygame.event.get():
            # quit handler
            if event.type == pygame.QUIT:
                return
            # arrow key handler
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    set_direction(event.key)
            # tick handler
            if event.type == TICK:
                # everything inside tick so that conditions get evaluated only at tick time
                move_snake()

                collision = False
                # check snake collision with itself or walls
                collision = (check_collision_self() or check_collision_walls())
                if collision:
                    # game over
                    return

                # logic for eating food
                if check_collision_food():
                    eat_food()

                # draw snake and food
                draw_snake_and_food(screen)

                # update screen
                pygame.display.update()

start()