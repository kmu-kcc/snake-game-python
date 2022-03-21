from typing import List, Tuple
import time
import pygame
import random
from datetime import datetime
from datetime import timedelta

# color constants setting.
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
SnakeBody = (80, 80, 255)
FONT_COLOR = (28, 0, 0)

# setting size of map.
SCREEN_SIZE = [400, 400]

# score of games.
score = 0

# done for ending of game.
playing = True
exit_request = False

# time setting.
#
# for game speed setting line 105.
clock = pygame.time.Clock()
last_moved_time = datetime.now()
font: pygame.font.Font

# keyboard constant setting.
KEY_DIRECTION = {
    pygame.K_UP: 'N',
    pygame.K_DOWN: 'S',
    pygame.K_LEFT: 'W',
    pygame.K_RIGHT: 'E',
}


# Snake represents snake object that playable character.
class Snake:

    positions: List[Tuple]
    direction: str

    # __init__ sets first position of snake.
    def __init__(self):
        self.init_position()
        
    def init_position(self):
        self.positions = [(2, SCREEN_SIZE[1] // 40), (1, SCREEN_SIZE[1] // 40), (0, SCREEN_SIZE[1] // 40)]
        self.direction = ''

    # draw() draws snake with right positions.
    def draw(self):
        for position in self.positions:
            draw_block(screen, SnakeBody, position)
            if position == self.positions[0]:
                draw_block(screen, BLUE, position)

    # move() moves snake to input keyboard direction.
    def move(self):
        head_position = self.positions[0]
        y, x = head_position
        if self.direction == 'W':
            self.positions = [(y - 1, x)] + self.positions[:-1]
        elif self.direction == 'E':
            self.positions = [(y + 1, x)] + self.positions[:-1]
        elif self.direction == 'N':
            self.positions = [(y, x - 1)] + self.positions[:-1]
        elif self.direction == 'S':
            self.positions = [(y, x + 1)] + self.positions[:-1]

    # grow() append array element to @snake.positions for representing growing of snake.
    def grow(self):
        global score
        score += 1
        tail_position = self.positions[-1]
        x, y = tail_position
        if self.direction == 'N':
            self.positions.append((x, y - 1))
        elif self.direction == 'S':
            self.positions.append((x, y + 1))
        elif self.direction == 'W':
            self.positions.append((x - 1, y))
        elif self.direction == 'C':
            self.positions.append((x + 1, y))
    
    def change_direction(self, key_code):
        direction = KEY_DIRECTION[key_code]
        if self.direction == 'E' and direction == 'W':
            return
        if self.direction == 'W' and direction == 'E':
            return
        if self.direction == 'N' and direction == 'S':
            return
        if self.direction == 'S' and direction == 'N':
            return
        if self.direction == '' and direction == 'W':
            return
        self.direction = direction


# Apple represents Apple objects that game's goal.
class Apple:

    position: Tuple
    
    # __init__() sets first position of apple.
    def __init__(self):
        self.init_position()

    def init_position(self):
        self.position = (SCREEN_SIZE[0] // 40, SCREEN_SIZE[1] // 40)
        
    # draw() draws and sets next position of apple.
    def draw(self):
        draw_block(screen, RED, self.position)


# define snake and apple. initialize later.
apple: Apple
snake: Snake


# draw_block sets the frontier of blocks.
def draw_block(screen, color, position):
    block = pygame.Rect((position[0] * 20, position[1] * 20), (20, 20))
    pygame.draw.rect(screen, color, block)


def handle_event():
    global playing, exit_request
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_request = True
            return
        if event.type == pygame.KEYDOWN:
            if playing and event.key in KEY_DIRECTION:
                snake.change_direction(event.key)
            elif not playing:
                if event.key == pygame.K_r:
                    reset_game()
                elif event.key == pygame.K_ESCAPE:
                    exit_request = True
                    return


def draw_common():
    screen.fill(WHITE)
    score_text = font.render(f'Score : {score}', True, FONT_COLOR)
    screen.blit(score_text, (10, 10))


def game_scene():
    global playing

    clock.tick(10)

    # for setting game speed change seconds=0.5.
    if timedelta(seconds=0.5) <= datetime.now() - last_moved_time:
        snake.move()

    # getting score.
    if snake.positions[0] == apple.position:
        snake.grow()
        while apple.position in snake.positions:
            apple.position = (random.randint(0, SCREEN_SIZE[0] // 20 - 1), random.randint(0, SCREEN_SIZE[1] // 20 - 1))

    # crash snake head with body
    if snake.positions[0] in snake.positions[1:]:
        playing = False
    # snake head out of map.
    if snake.positions[0][0] > SCREEN_SIZE[0] // 20 - 1 or snake.positions[0][0] < 0:
        playing = False
    if snake.positions[0][1] > SCREEN_SIZE[1] // 20 - 1 or snake.positions[0][1] < 0:
        playing = False

    # display update.
    snake.draw()
    apple.draw()
    pygame.display.update()


def end_scene():
    global exit_request

    game_end_text = font.render('Press ESC to exit or R to restart', True, FONT_COLOR)
    screen.blit(game_end_text, (SCREEN_SIZE[0] // 2 - 150, SCREEN_SIZE[1] // 2))
    pygame.display.update()
    time.sleep(0.2)


def reset_game():
    global score, playing

    playing = True    
    score = 0
    apple.init_position()
    snake.init_position()


# run_game is main function of game.
def run_game():
    global playing, last_moved_time, score, font, apple, snake

    # infinite loop to prevent game finishing
    while not exit_request:
        handle_event()
        if exit_request:
            pygame.quit()
            break

        draw_common()
        if playing:
            # show while playing game
            game_scene()
        else:
            # show when game end
            end_scene()


if __name__ == '__main__':
    # initialize pygame
    pygame.init()
    # load font to draw text
    font = pygame.font.Font(None, 30)
    # adjust screen size
    screen = pygame.display.set_mode(SCREEN_SIZE)
    # initialize game object
    apple = Apple()
    snake = Snake()

    # start game
    run_game()
