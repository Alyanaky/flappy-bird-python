import pygame
import random

pygame.init()

WIDTH, HEIGHT = 400, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

FPS = 30
GRAVITY = 1
JUMP = -15
PIPE_WIDTH = 70
PIPE_GAP = 150

bird_img = pygame.Surface((30, 30))
bird_img.fill((255, 255, 0))

class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 0
        self.img = bird_img

    def jump(self):
        self.vel = JUMP

    def update(self):
        self.vel += GRAVITY
        self.y += self.vel

        # Top boundary:
        if self.y < 0:
            self.y = 0

        if self.y + self.img.get_height() > HEIGHT:
            self.y = HEIGHT - self.img.get_height()

    def draw(self):
        win.blit(self.img, (self.x, self.y))

class Pipe:
    def __init__(self, x, height):
        self.x = x
        self.height = height
        self.width = PIPE_WIDTH
        self.top = random.randrange(50, HEIGHT - PIPE_GAP - 50)
        self.bottom = self.top + PIPE_GAP

        self.passed = False

    def draw(self):
        pygame.draw.rect(win, GREEN, (self.x, 0, self.width, self.top))
        pygame.draw.rect(win, GREEN, (self.x, self.bottom, self.width, HEIGHT - self.bottom))

    def update(self):
        self.x -= 5

        if self.x + self.width < 0:
            return False
        else:
            return True

def draw_window(bird, pipes, score):
    win.fill(WHITE)

    for pipe in pipes:
        pipe.draw()

    bird.draw()

    # Display the score:
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, BLACK)
    win.blit(text, (10, 10))

    pygame.display.update()

def check_collision(bird, pipes):
    # Check if the bird's rectangle collides with any pipe's rectangle
    bird_rect = pygame.Rect(bird.x, bird.y, bird.img.get_width(), bird.img.get_height())

    for pipe in pipes:
        top_pipe_rect = pygame.Rect(pipe.x, 0, pipe.width, pipe.top)
        bottom_pipe_rect = pygame.Rect(pipe.x, pipe.bottom, pipe.width, HEIGHT - pipe.bottom)

        if bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect):
            return True

    return False

def main():
    run = True
    clock = pygame.time.Clock()

    bird = Bird(50, HEIGHT // 2)
    pipes = [Pipe(WIDTH, 0)]

    score = 0
    game_over = False

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    bird.jump()

        if not game_over:
            bird.update()

            if len(pipes) > 0 and pipes[0].x + pipes[0].width < bird.x:
                if not pipes[0].passed:
                    score += 1
                    pipes[0].passed = True

            for pipe in pipes:
                if not pipe.update():
                    pipes.remove(pipe)

            if len(pipes) == 0 or pipes[-1].x < WIDTH - 300:
                pipes.append(Pipe(WIDTH, 0))

            # Check for collision:
            game_over = check_collision(bird, pipes)

        draw_window(bird, pipes, score)

        # Game Over screen:
        if game_over:
            font = pygame.font.Font(None, 72)
            text = font.render("Game Over", True, BLACK)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            win.blit(text, text_rect)
            pygame.display.update()

            # Wait for a key press to exit
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        run = False
                        break

    pygame.quit()

if __name__ == "__main__":
    main()
