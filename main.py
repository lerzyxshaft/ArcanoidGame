import pygame
import sys

pygame.init()
window = pygame.display.set_mode((500,500))
background_image = pygame.image.load("images/background.png")
window.blit(background_image, (0, 0))
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)

clock=pygame.time.Clock()

class Area():

    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.fill_color = color

    def draw_rect(self):
        pygame.draw.rect(window, self.fill_color, self.rect)

    def colliderect(self, rect):
        return self.rect.colliderect(rect)


class Label(Area):

    def set_text(self, text, font_size=50, color=(0, 0, 0)):
        self.image = pygame.font.SysFont("Verdana", font_size).render(text, True, color)

    def draw_all(self, shift_x = 13, shift_y = 50):
        self.draw_rect()
        window.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))


class Sprite(Area):

    def __init__(self, image, x, y, width, height):
        Area.__init__(self, x=x, y=y, width=width, height=height, color=None)
        self.image = pygame.image.load(image)

    def draw_sprite(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


def draw_button(window, color, rect, text, text_color):
    font = pygame.font.Font(None, 36)
    pygame.draw.rect(window, color, rect)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    window.blit(text_surface, text_rect)


easy_button = pygame.Rect(100, 150, 300, 50)
medium_button = pygame.Rect(100, 250, 300, 50)
hard_button = pygame.Rect(100, 350, 300, 50)
difficulty = None


ball = Sprite("images/ball.png", 250, 250, 30, 30)
platform = Sprite("images/platform.png", 250, 450, 100, 20)

monsters = []


y = 50
for j in range(3):
    x = 5 + 28 * j
    for i in range(9 - j):
        monster = Sprite("images/monster.png", x, y, 50, 50)
        monsters.append(monster)
        x += 55
    y += 55

move_right = False
move_left = False


def difficulty_screen():
    global difficulty

    while True:
        window.fill(GRAY)

        draw_button(window, WHITE, easy_button, "Easy", BLACK)
        draw_button(window, WHITE, medium_button, "Medium", BLACK)
        draw_button(window, WHITE, hard_button, "Hard", BLACK)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if easy_button.collidepoint(mouse_pos):
                    difficulty = "easy"
                    return
                elif medium_button.collidepoint(mouse_pos):
                    difficulty = "medium"
                    return
                elif hard_button.collidepoint(mouse_pos):
                    difficulty = "hard"
                    return

difficulty_screen()

if difficulty == "easy":
    speed_x, speed_y = 2, 2
elif difficulty == "medium":
    speed_x, speed_y = 4, 4
elif difficulty == "hard":
    speed_x, speed_y = 6, 6

while True:
    window.blit(background_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_left = True
            if event.key == pygame.K_RIGHT:
                move_right = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                move_left = False
            if event.key == pygame.K_RIGHT:
                move_right = False

    if move_right and platform.rect.x + platform.rect.width < 500:
        platform.rect.x += 5
    if move_left and platform.rect.x > 0:
        platform.rect.x -= 5

    if len(monsters) == 0:
        win = Label(0, 0, 500, 500, (0, 255, 0))
        win.set_text("YOU WON!", 50, (0, 0, 0))
        win.draw_all(100, 200)
        pygame.display.update()
        pygame.time.delay(2000)
        break
    if ball.rect.y > platform.rect.y:
        win = Label(0, 0, 500, 500, (255, 0, 0))
        win.set_text("YOU LOSE;(", 50, (255, 255, 255))
        win.draw_all(100, 200)
        pygame.display.update()
        pygame.time.delay(2000)
        break

    ball.rect.x += speed_x
    ball.rect.y += speed_y

    if ball.rect.colliderect(platform.rect):
        speed_y = -speed_y
    if ball.rect.y <= 0 or ball.rect.y >= 500:
        speed_y = -speed_y
    if ball.rect.x <= 0 or ball.rect.x >= 500:
        speed_x = -speed_x

    for monster in monsters[:]:
        if ball.colliderect(monster.rect):
            speed_y = -speed_y
            monsters.remove(monster)

    for monster in monsters:
        monster.draw_sprite()

    platform.draw_sprite()
    ball.draw_sprite()

    pygame.display.update()
    clock.tick(60)