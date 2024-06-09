import pygame
import sys
import random

pygame.init()

# Screen settings
WIDTH = 1270
HEIGHT = 720
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()
FPS = 60

# Load images
BACKGROUND = pygame.image.load("background.png").convert_alpha()
BIRD = pygame.image.load("bird.png").convert_alpha()
PIPE = pygame.image.load("pipe.png").convert_alpha()
ROTATED_PIPE = pygame.image.load("rotated_pipe.png").convert_alpha()

# Load sounds
POINT_SOUND = pygame.mixer.Sound("sfx_point.wav")
HIT_SOUND = pygame.mixer.Sound("sfx_hit.wav")

# Game Caption
pygame.display.set_caption("Flappy Bird")


class Game:
    def __init__(self):
        self.reset_game()

    def reset_game(self):
        self.game_on = True
        self.bird_x = 100
        self.bird_y = 100
        self.pipes_x = [WIDTH + i * 200 for i in range(7)]
        self.lower_pipe_y = [self.random_pipe() for _ in range(7)]
        self.upper_pipe_y = [self.random_rotated_pipe() for _ in range(7)]
        self.gravity = 0
        self.pipe_velocity = 0
        self.flap = 0
        self.score = 0
        self.rotate_angle = 0
        self.is_game_over = False
        self.play_sound = True

    def moving_pipes(self):
        for i in range(7):
            self.pipes_x[i] -= self.pipe_velocity

        for i in range(7):
            if self.pipes_x[i] < -50:
                self.pipes_x[i] = WIDTH + 100
                self.lower_pipe_y[i] = self.random_pipe()
                self.upper_pipe_y[i] = self.random_rotated_pipe()

    @staticmethod
    def random_pipe():
        return random.randrange(HEIGHT // 2 + 50, HEIGHT - 200)

    @staticmethod
    def random_rotated_pipe():
        return random.randrange(-HEIGHT // 2 + 100, -100)

    def flapping(self):
        self.bird_y += self.gravity
        if not self.is_game_over:
            self.flap -= 1
            self.bird_y -= self.flap

    def is_collide(self):
        for i in range(7):
            if self.bird_x >= self.pipes_x[i] and self.bird_x <= self.pipes_x[i] + PIPE.get_width() and (
                self.bird_y + BIRD.get_height() - 15 >= self.lower_pipe_y[i] or
                self.bird_y <= self.upper_pipe_y[i] + ROTATED_PIPE.get_height() - 15
            ):
                return True

            if self.bird_x == self.pipes_x[i] and self.bird_y <= self.lower_pipe_y[i] and self.bird_y >= self.upper_pipe_y[i]:
                if not self.is_game_over:
                    self.score += 1
                    pygame.mixer.Sound.play(POINT_SOUND)

        if self.bird_y <= 0:
            return True

        if self.bird_y + BIRD.get_height() >= HEIGHT:
            self.gravity = 0
            return True

        return False

    def game_over(self):
        if self.is_collide():
            self.is_game_over = True
            self.display_text("Game Over!", (255, 255, 255), 450, 300, 84, "Fixedsys", bold=True)
            self.display_text("Press Enter To Play Again", (255, 255, 255), 400, 600, 48, "Fixedsys", bold=True)
            self.pipe_velocity = 0
            self.flap = 0
            self.rotate_angle = -90
            if self.play_sound:
                pygame.mixer.Sound.play(HIT_SOUND)
                self.play_sound = False

    @staticmethod
    def display_text(text, color, x, y, size, style, bold=False):
        font = pygame.font.SysFont(style, size, bold=bold)
        screen_text = font.render(text, True, color)
        SCREEN.blit(screen_text, (x, y))

    def main_game(self):
        while self.game_on:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if not self.is_game_over:
                            self.pipe_velocity = 5
                            self.gravity = 10
                            self.flap = 20
                            self.rotate_angle = 15

                    if event.key == pygame.K_RETURN:
                        self.reset_game()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.rotate_angle = 0

            SCREEN.blit(BACKGROUND, (0, 0))

            for i in range(7):
                SCREEN.blit(PIPE, (self.pipes_x[i], self.lower_pipe_y[i]))
                SCREEN.blit(ROTATED_PIPE, (self.pipes_x[i], self.upper_pipe_y[i]))

            SCREEN.blit(pygame.transform.rotozoom(BIRD, self.rotate_angle, 1), (self.bird_x, self.bird_y))

            self.moving_pipes()
            self.flapping()
            self.game_over()
            self.display_text(str(self.score), (255, 255, 255), 600, 50, 68, "Fixedsys", bold=True)

            pygame.display.update()
            CLOCK.tick(FPS)


if __name__ == "__main__":
    flappy_bird = Game()
    flappy_bird.main_game()
