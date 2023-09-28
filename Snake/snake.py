from random import randint
import pygame

pygame.init()
SCREEN = pygame.display.set_mode((1000, 1000))
WIDTH, HEIGHT = SCREEN.get_size()
CLOCK = pygame.time.Clock()

pygame.display.set_caption('Snake By Armando Chaparro')

GRID_WIDTH = GRID_HEIGHT = 15
SQUARE_WIDTH = WIDTH // GRID_WIDTH
SQUARE_HEIGHT = HEIGHT // GRID_HEIGHT
FONT = pygame.font.SysFont('Comic Sans', SQUARE_HEIGHT)
FPS = 5

GREEN = pygame.Vector3(145, 190, 72)        #91be48
LIGHT_GREEN = pygame.Vector3(171, 214, 81)  #abd651
DARK_GREEN = pygame.Vector3(76, 125, 44)    #4c7d2c
DARK_BLUE = pygame.Vector3(0, 0, 255)       #0000ff
LIGHT_BLUE = pygame.Vector3(74, 125, 250)   #4a7dfa
RED = pygame.Vector3(255, 0, 0)             #ff0000
YELLOW = pygame.Vector3(255, 255, 0)        #ffff00


def color_lerp(a: pygame.Vector3, b: pygame.Vector3, t: float) -> pygame.Vector3:

    return a + (b - a) * t


class Food:

    def __init__(self):

        self.time = 0
        self.delta_time = 1
        self.anim_time = 4
        self.color = RED

        self.respawn()

    def respawn(self) -> None:

        x, y = randint(0, GRID_WIDTH - 1), randint(1, GRID_WIDTH - 1)
        self.pos = pygame.Vector2(x, y)
        if self.pos not in SNAKE.pieces:
            self.rect = pygame.Rect(
                x * SQUARE_WIDTH, y * SQUARE_HEIGHT,
                SQUARE_WIDTH, SQUARE_HEIGHT
            )
        else: self.respawn()

    def update(self) -> None:

        if SNAKE.pause:
            return
        if self.time < 0 or self.time > self.anim_time:
            self.delta_time *= -1
        self.time += self.delta_time
        self.color = color_lerp(RED, YELLOW, max(0, self.time) / 10)

    def show(self) -> None:

        pygame.draw.rect(SCREEN, self.color, self.rect)

    def collide(self, pos: pygame.Vector2) -> bool:

        return self.pos == pos


class Snake:

    def __init__(self):

        self.left = pygame.Vector2(-1, 0)
        self.right = pygame.Vector2(1, 0)
        self.up = pygame.Vector2(0, -1)
        self.down = pygame.Vector2(0, 1)
        self.dir = self.left

        self.score = 0
        self.time = 0
        self.pause = False

        self.respawn()

    def respawn(self) -> None:

        self.pieces = [pygame.Vector2(10, 10)]
        self.dir = self.left
        self.time = self.score = 0

    def show(self) -> None:

        for i, (x, y) in enumerate(reversed(self.pieces)):
            porcent = i / len(self.pieces)
            color = color_lerp(DARK_BLUE, LIGHT_BLUE, porcent)
            rect = (
                x * SQUARE_WIDTH, y * SQUARE_HEIGHT, SQUARE_WIDTH, SQUARE_HEIGHT
            )
            pygame.draw.rect(SCREEN, color, rect)

    def update(self) -> None:

        if self.pause:
            return
        self.pieces.insert(0, self.pieces[0] + self.dir)
        self.pieces.pop(-1)
        self.check_food()
        self.check_collision()

    def check_collision(self) -> None:

        if any([
            self.pieces[0].x < 0, self.pieces[0].x == GRID_WIDTH,
            self.pieces[0].y < 1, self.pieces[0].y == GRID_HEIGHT,
            self.pieces.count(self.pieces[0]) != 1
        ]):
            self.respawn()

    def check_food(self) -> None:

        if FOOD.collide(self.pieces[0]):
            FOOD.respawn()
            self.score += 1
            self.pieces.insert(0, self.pieces[0] + self.dir)

    def keydown(self, key: int) -> None:

        if key == pygame.K_LEFT and self.dir != self.right:
            self.dir = self.left
        elif key == pygame.K_RIGHT and self.dir != self.left:
            self.dir = self.right
        elif key == pygame.K_DOWN and self.dir != self.up:
            self.dir = self.down
        elif key == pygame.K_UP and self.dir != self.down:
            self.dir = self.up
        elif key == pygame.K_SPACE:
            self.pause = not self.pause
    
    def update_time(self, time: float) -> None:

        if not self.pause:
            self.time += time


def main() -> None:
    """Main loop"""

    while True:


        SCREEN.fill(DARK_GREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                SNAKE.keydown(event.key)


        for y in range(1, GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                index = x + y * GRID_WIDTH
                color = LIGHT_GREEN if index%2 else GREEN
                rect = (x * SQUARE_WIDTH, y * SQUARE_HEIGHT, SQUARE_WIDTH, SQUARE_HEIGHT)
                pygame.draw.rect(SCREEN, color, rect)


        time = FONT.render(f'{SNAKE.time:.02f}', True, 'green')
        time_rect = time.get_rect(centerx=0.75*WIDTH, centery=SQUARE_HEIGHT/2)
        SCREEN.blit(time, time_rect)

        score = FONT.render(str(SNAKE.score), True, 'white')
        score_rect = score.get_rect(centerx=0.25*WIDTH, centery=SQUARE_HEIGHT/2)
        SCREEN.blit(score, score_rect)


        SNAKE.update()
        FOOD.update()
        SNAKE.show()
        FOOD.show()


        pygame.display.update()
        SNAKE.update_time(CLOCK.tick(FPS) / 1000)


if __name__ == '__main__':
    SNAKE = Snake()
    FOOD = Food()
    main()