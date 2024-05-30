import datetime
import os
import random
import threading

import pygame

pygame.init()


def scale_image(path, scale=15):
    image = pygame.image.load(path)
    image = pygame.transform.scale(
        image, (image.get_size()[0] // scale, image.get_size()[1] // scale)
    )
    return image


# Global Constants
SCREEN_HEIGHT = 1080
SCREEN_WIDTH = 1920
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Chrome Dino Runner")

Ico = scale_image("assets/DinoWallpaper.png")
pygame.display.set_icon(Ico)

RUNNING = [
    scale_image(os.path.join("assets/Dino", "DinoRun1.png")),
    scale_image(os.path.join("assets/Dino", "DinoRun2.png")),
]
JUMPING = scale_image(os.path.join("assets/Dino", "DinoJump.png"))
DUCKING = [
    scale_image(os.path.join("assets/Dino", "DinoDuck1.png")),
    scale_image(os.path.join("assets/Dino", "DinoDuck2.png")),
]

SMALL_CACTUS = [
    scale_image(os.path.join("assets/Cactus", "SmallCactus1.png"), 5),
    scale_image(os.path.join("assets/Cactus", "SmallCactus2.png"), 5),
    scale_image(os.path.join("assets/Cactus", "SmallCactus3.png"), 5),
]
LARGE_CACTUS = [
    scale_image(os.path.join("assets/Cactus", "LargeCactus1.png"), 4),
    scale_image(os.path.join("assets/Cactus", "LargeCactus2.png"), 4),
    scale_image(os.path.join("assets/Cactus", "LargeCactus3.png"), 4),
]

BIRD = [
    scale_image(os.path.join("assets/Bird", "Bird1.png")),
    scale_image(os.path.join("assets/Bird", "Bird2.png")),
]

CLOUD = pygame.image.load(os.path.join("assets/Other", "Cloud.png"))

BG = pygame.transform.scale(
    pygame.image.load(os.path.join("assets/Other", "Track.jpg")),
    (SCREEN_WIDTH, SCREEN_HEIGHT),
)

FONT_COLOR = (0, 0, 0)


class Dinosaur:

    X_POS = 150
    Y_POS = 310
    Y_POS_DUCK = 350
    JUMP_VEL = 8

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.image = self.run_img[0]

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.dino_rect = self.image.get_rect(topleft=(self.X_POS, self.Y_POS))

    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if (userInput[pygame.K_UP] or userInput[pygame.K_SPACE]) and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True

        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False

        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]

        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK

        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]

        self.dino_rect = self.image.get_rect(topleft=(self.X_POS, self.Y_POS))

        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8

        if self.jump_vel < -self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN) -> None:
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))
        pygame.draw.rect(SCREEN, "#000000", self.dino_rect, 2)


class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)
        pygame.draw.rect(SCREEN, "#000000", self.rect, 2)


class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 400


class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 355


class Bird(Obstacle):
    BIRD_HEIGHTS = [230, 250, 330]

    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = random.choice(self.BIRD_HEIGHTS)
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        pygame.draw.rect(SCREEN, "#000000", self.rect, 2)
        self.index += 1


def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles

    run = True

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1
        current_time = datetime.datetime.now().hour

        if not os.path.exists("score.txt"):
            with open("score.txt", "w+", encoding="utf-8") as f:
                f.write("")

        with open("score.txt", "r") as f:
            score_ints = [int(x) for x in f.read().split()]

            if score_ints:
                highscore = max(score_ints)
            else:
                highscore = 0

            if points > highscore:
                highscore = points
            text = font.render(
                "High Score: " + str(highscore) + "  Points: " + str(points),
                True,
                FONT_COLOR,
            )

        textRect = text.get_rect()
        textRect.center = (900, 40)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg

        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    def unpause():
        nonlocal pause, run
        pause = False
        run = True

    def paused():
        nonlocal pause
        pause = True
        font = pygame.font.Font("freesansbold.ttf", 30)
        text = font.render("Game Paused, Press 'u' to Unpause", True, FONT_COLOR)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
        SCREEN.blit(text, textRect)
        pygame.display.update()

        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_u:
                    unpause()

    clock = pygame.time.Clock()
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 0
    points = 0

    death_count = 0
    pause = False

    background()
    player = Dinosaur()
    cloud = Cloud()
    obstacles = []
    font = pygame.font.Font("freesansbold.ttf", 20)

    game_over = False
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                run = False
                paused()

        if game_over:
            pygame.time.delay(1000)
            death_count += 1
            menu(death_count)

        current_time = datetime.datetime.now().hour
        if 7 < current_time < 19:
            SCREEN.fill((255, 255, 255))
        else:
            SCREEN.fill((0, 0, 0))
        userInput = pygame.key.get_pressed()

        player.update(userInput)
        player.draw(SCREEN)

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(BIRD))

        for obstacle in obstacles:
            obstacle.update()
            obstacle.draw(SCREEN)
            if player.dino_rect.colliderect(obstacle.rect):
                game_over = True

        background()
        cloud.draw(SCREEN)
        cloud.update()

        score()

        clock.tick(30)
        pygame.display.update()


def menu(death_count):
    global points
    global FONT_COLOR

    run = True
    while run:
        current_time = datetime.datetime.now().hour
        if 7 < current_time < 19:
            FONT_COLOR = (0, 0, 0)
            SCREEN.fill((255, 255, 255))
        else:
            FONT_COLOR = (255, 255, 255)
            SCREEN.fill((128, 128, 128))
        font = pygame.font.Font("freesansbold.ttf", 30)

        if death_count == 0:
            text = font.render("Press any Key to Start", True, FONT_COLOR)
        elif death_count > 0:
            text = font.render("Press any Key to Restart", True, FONT_COLOR)
            score = font.render("Your Score: " + str(points), True, FONT_COLOR)
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)
            f = open("score.txt", "a")
            f.write(str(points) + "\n")
            f.close()
            with open("score.txt", "r") as f:
                score = (
                    f.read()
                )  # Read all file in case values are not on a single line
                score_ints = [int(x) for x in score.split()]  # Convert strings to ints
            highscore = max(score_ints)  # sum all elements of the list
            hs_score_text = font.render(
                "High Score : " + str(highscore), True, FONT_COLOR
            )
            hs_score_rect = hs_score_text.get_rect()
            hs_score_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
            SCREEN.blit(hs_score_text, hs_score_rect)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                main()


t1 = threading.Thread(target=menu(death_count=0), daemon=True)
t1.start()