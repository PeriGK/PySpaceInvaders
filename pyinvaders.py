from pygame import *
import random


###TODO###
# Add a score counter => Done
# Check for missile-to-missile collisions.
# Add a second row of aliens
# Remove magic numbers
# Publish to github mentioning the changes

class Sprite:
    SIZE = 32

    def __init__(self, xpos, ypos, filename):
        self.x = xpos
        self.y = ypos
        self.bitmap = image.load(filename)
        self.bitmap.set_colorkey((0,0,0))

    def set_position(self, xpos, ypos):
        self.x = xpos
        self.y = ypos

    def render(self):
        screen.blit(self.bitmap, (self.x, self.y))


def intersect(s1_x, s1_y, s2_x, s2_y):
    if (s1_x > s2_x - Sprite.SIZE) and (s1_x < s2_x + Sprite.SIZE) and (s1_y > s2_y - Sprite.SIZE) and (s1_y < s2_y + Sprite.SIZE):
        return 1
    else:
        return 0


init()
window_width = 640
window_height = 480
screen = display.set_mode((window_width,window_height))
key.set_repeat(1, 1)
display.set_caption('PyInvaders')
backdrop = image.load('data/backdrop.bmp')

score = 0
myfont = font.SysFont("monospace", 16)

enemies = []

x = 0

for count in range(10):
    enemies.append(Sprite(50 * x + 50, 50, 'data/baddie.bmp'))
    x += 1

hero = Sprite(20, 400, 'data/hero.bmp')
ourmissile = Sprite(0, 480, 'data/heromissile.bmp')
enemymissile = Sprite(0, 480, 'data/baddiemissile.bmp')
enemy_rightmost_bound = 590
enemy_leftmost_bound = 10


quit = 0
enemyspeed = 3
killed_enemy_points = 1
enemy_vertical_speed = 5
ourmissile_speed = 5
time_delay = 5
hero_horizontal_speed = 5

while quit == 0:
    screen.blit(backdrop, (0, 0))
    scoretext = myfont.render("Score = " + str(score), 1, (0, 0, 0))
    screen.blit(scoretext, (5, 10))

    for count in range(len(enemies)):
        enemies[count].x += + enemyspeed
        enemies[count].render()

    if enemies[len(enemies)-1].x > enemy_rightmost_bound:
        enemyspeed = -3
        for count in range(len(enemies)):
            enemies[count].y += enemy_vertical_speed

    if enemies[0].x < enemy_leftmost_bound:
        enemyspeed = 3
        for count in range(len(enemies)):
            enemies[count].y += enemy_vertical_speed

    if 0 < ourmissile.y < (window_height - 1):
        ourmissile.render()
        ourmissile.y -= ourmissile_speed

    if enemymissile.y >= window_height and len(enemies) > 0:
        enemymissile.x = enemies[random.randint(0, len(enemies) - 1)].x
        enemymissile.y = enemies[0].y

    if intersect(hero.x, hero.y, enemymissile.x, enemymissile.y):
        quit = 1

    for count in range(0, len(enemies)):
        if intersect(ourmissile.x, ourmissile.y, enemies[count].x, enemies[count].y):
            del enemies[count]
            score += killed_enemy_points
            break

    if len(enemies) == 0:
        quit = 1

    for ourevent in event.get():
        if ourevent.type == QUIT:
            quit = 1
        if ourevent.type == KEYDOWN:
            if ourevent.key == K_RIGHT and hero.x < 590:
                hero.x += hero_horizontal_speed
            if ourevent.key == K_LEFT and hero.x > 10:
                hero.x -= hero_horizontal_speed
            if ourevent.key == K_SPACE:
                ourmissile.x = hero.x
                ourmissile.y = hero.y

    enemymissile.render()
    enemymissile.y += 5

    hero.render()

    display.update()
    time.delay(time_delay)

