import pygame

from time import time
pygame.init()
window=pygame.display.set_mode((500,500))
background_image = pygame.image.load("images/background.png")

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

    def draw_text(self):
        self.draw_rect()
        window.blit(self.image, (self.rect.x, self.rect.y))

class Sprite(Area):

    def __init__(self, image, x, y, width, height):
        Area.__init__(self, x=x, y=y, width=width, height=height, color=None)
        self.image = pygame.image.load(image)

    def draw_sprite(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

ball = Sprite("images/ball.png", 250, 250 ,30 ,30)
ball.draw_sprite()

platform = Sprite("images/platform.png", 250, 300, 50, 50)
platform.draw_sprite()

monsters = []

y = 0
for j in range(3):
    x=5+ 28*j
    for i in range(9-j):
        monster=Sprite("images/monster.png", x, y, 50, 50)
        monsters.append(monster)
        x+=55
        y+=55

move_right = False
move_left = False


speed_x = 2
speed_y = 2

while True:
    window.blit(background_image, (0, 0))

    if ball.colliderect(platform.rect):
        speed_y = - speed_y

    if ball.rect.y <= 0 or ball.rect.y >= 500:
        speed_y = -speed_y
    if ball.rect.x <= 0 or ball.rect.x >= 500:
        speed_x = -speed_x

    ball.rect.x += speed_x
    ball.rect.y += speed_y

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

    if move_right:
        platform.rect.x += 5
    if move_left:
        platform.rect.x -= 5
    if len(monsters) == 0:
        win = Label(0, 0, 500, 500, (0, 255, 0))
        win.set_text("YOU WON!", 50, (0, 0, 0))
        win.draw_all(200, 200)
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
    for monster in monsters[:]:
        if ball.colliderect(monster.rect):
            speed_y = -speed_y
            monsters.remove(monster)

    for monster in monsters:
        monster.draw_sprite()

    for monster in monsters:
        monster.draw_sprite()

    window.blit(background_image, (0, 0))
    platform.draw_sprite()
    ball.draw_sprite()
    pygame.display.update()
    clock.tick(60)
pygame.display.update()
