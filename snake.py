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

# setting size of map.
size = [400, 400]
screen = pygame.display.set_mode(size)

# score of games.
score = 0

# done for ending of game.
done = False

# time setting.
#
# for game speed setting line 105.
clock = pygame.time.Clock()
last_moved_time = datetime.now()

# keyboard constant setting.
KEY_DIRECTION = {
    pygame.K_UP: 'N',
    pygame.K_DOWN: 'S',
    pygame.K_LEFT: 'W',
    pygame.K_RIGHT: 'E',
}


# Snake represents snake object that playable character.
class Snake:
    # __init__ sets first position of snake.
    def __init__(self):
        self.positions = [(2, size[1] // 40), (1, size[1] // 40), (0, size[1] // 40)]
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


# Apple represents Apple objects that game's goal.
class Apple:
    # __init__() sets first position of apple.
    def __init__(self, position=(size[0] // 40, size[1] // 40)):
        self.position = position

    # draw() draws and sets next position of apple.
    def draw(self):
        draw_block(screen, RED, self.position)


# draw_block sets the frontier of blocks.
def draw_block(screen, color, position):
    block = pygame.Rect((position[0] * 20, position[1] * 20), (20, 20))
    pygame.draw.rect(screen, color, block)


# runGame is main function of game.
def run_game():
    global done, last_moved_time, score

    # visualize snake and apple.
    snake = Snake()
    apple = Apple()

    # for playing game.
    while not done:
        clock.tick(10)
        screen.fill(WHITE)
        font = pygame.font.Font(None, 30)
        text = font.render("Score : " + '{}'.format(score), True, (28, 0, 0))
        screen.blit(text, (10, 10))

        # game process.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key in KEY_DIRECTION:
                    snake.direction = KEY_DIRECTION[event.key]

        # for setting game speed change seconds=0.5.
        if timedelta(seconds=0.5) <= datetime.now() - last_moved_time:
            snake.move()

        # getting score.
        if snake.positions[0] == apple.position:
            snake.grow()
            while apple.position in snake.positions:
                apple.position = (random.randint(0, size[0] // 20 - 1), random.randint(0, size[1 ] // 20 - 1))

        # crash snake head with body
        if snake.positions[0] in snake.positions[1:]:
            return
        # snake head out of map.
        if snake.positions[0][0] > size[0] // 20-1 or snake.positions[0][0] < 0:
            return
        if snake.positions[0][1] > size[1] // 20-1 or snake.positions[0][1] < 0:
            return

        # display update.
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    pygame.init()
    # First Game Start
    run_game()
    while True:
        font = pygame.font.Font(None, 30)
        end_text = font.render("Press ESC to exit or R to restart", True, (28, 0, 0))
        screen.blit(end_text, (size[0] // 2 - 150, size[1] // 2))
        pygame.display.update()
        time.sleep(0.2)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
    
            # Press R: Restart
            # Press ESC: End game
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    score = 0
                    run_game()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
