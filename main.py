import pygame
from pygame.locals import *
import time
import random

SIZE = 40

class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("apple.jpg").convert()
        self.parent_screen = parent_screen
        self.x = 120
        self.y = 120

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()  # updating the window

    def move(self):
        self.x = random.randint(0, 24) * SIZE
        self.y = random.randint(0, 16) * SIZE

class Snake:
    def __init__(self, surface, length):
        self.length = length
        self.parent_screen = surface
        self.block = pygame.image.load("block.jpg").convert()
        self.block_x = [SIZE]*length
        self.block_y = [SIZE]*length
        self.direction = 'down'

    def increase_length(self):
        self.length+=1
        self.block_x.append(-1)
        self.block_y.append(-1);

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.block_x[i], self.block_y[i]))
        pygame.display.flip()  # updating the window

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_down(self):
        self.direction = 'down'

    def move_up(self):
        self.direction = 'up'

    def walk(self):
        for i in range(self.length-1,0,-1):
            self.block_x[i] = self.block_x[i-1]
            self.block_y[i] = self.block_y[i - 1]

        if self.direction == 'left':
            self.block_x[0] -= SIZE
        elif self.direction == 'right':
            self.block_x[0] += SIZE
        elif self.direction == 'down':
            self.block_y[0] += SIZE
        elif self.direction == 'up':
            self.block_y[0] -= SIZE

        self.draw()

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Snake Game ')  # title
        pygame.mixer.init()
        self.play_bg_music()
        self.surface = pygame.display.set_mode((1200, 650))  # initialize the game window
        self.surface.fill((110, 110, 5))   # set the color
        self.snake = Snake(self.surface, 3)   # snake starts with 3 blocks
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def collision(self, x1, x2, y1, y2):
        if x1 >= x2 and x1 <= x2 + SIZE:
            if y1 >= y2 and y1 <= y2 + SIZE:
                return True
        return False

    def play_music(self, music):
        music = pygame.mixer.Sound(f"{music}.mp3")
        pygame.mixer.Sound.play(music)

    def play_bg_music(self):
        pygame.mixer.music.load('bg_music_1.mp3')
        pygame.mixer.music.play()

    def background(self):
        bg = pygame.image.load('background.jpg')
        self.surface.blit(bg, (0, 0))

    def play(self):
        self.background()
        self.snake.walk()
        self.apple.draw()
        self.show_score()
        pygame.display.flip()

        if self.collision(self.snake.block_x[0],self.apple.x, self.snake.block_y[0], self.apple.y):   # snake colliding with apple
            self.play_music('ding')
            self.snake.increase_length()
            self.apple.move()

        for i in range(3, self.snake.length):  # snake colliding with itself
            if self.collision(self.snake.block_x[0], self.snake.block_y[0], self.snake.block_x[i], self.snake.block_y[i]):
                self.play_music('crash')
                raise "Game Over!"
                #exit()

        if not (0 <=self.snake.block_x[0] <= 1200 and 0 <= self.snake.block_y[0] <= 650):  # snake colliding with wall
            self.play_music('crash')
            raise "Game Over!"

    def show_score(self):
        font = pygame.font.SysFont('Arial', 25)
        score = font.render(f"your score(s) : {self.snake.length}", True, (200, 200, 200))
        self.surface.blit(score, (1000, 10))

    def game_over(self):
        self.background()
        font = pygame.font.SysFont('Arial', 25)
        line = font.render(f"your score(s) : {self.snake.length}", True, (200, 200, 200))
        self.surface.blit(line, (200, 300))
        line2 = font.render("if you wanna continue the game press Enter. for exiting press Esc", True, (200, 200, 200))
        self.surface.blit(line2, (300, 400))
        pygame.display.flip()

    def reset_game(self):
        self.snake = Snake(self.surface, 3)
        self.apple = Apple(self.surface)

    def run(self):
        runnig = True
        pause = False

        while runnig:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:  # exit by click Esc on keybord
                        runnig = False
                    elif event.key == K_RETURN:   # RETURN and Enter are same
                        pause = False
                    elif event.key == K_UP:
                        self.snake.move_up()
                    elif event.key == K_DOWN:
                        self.snake.move_down()
                    elif event.key == K_LEFT:
                        self.snake.move_left()
                    elif event.key == K_RIGHT:
                        self.snake.move_right()
                elif event.type == QUIT:
                    runnig = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.game_over()
                pause = True
                self.reset_game()

            time.sleep(0.3)  # snake's speed

if __name__ == '__main__':
    game = Game()
    game.run()