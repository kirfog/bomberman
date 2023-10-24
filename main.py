import pygame
import numpy
import os
import sys
import random

FPS = 60
WIDTH, HEIGHT = 15, 8
WALL_WIDTH, WALL_HEIGHT = 100, 100

pygame.init()
pygame.font.init()
window = pygame.display.set_mode((WIDTH * WALL_WIDTH, HEIGHT * WALL_HEIGHT))
pygame.display.set_caption("BOMBERMAN")
font = pygame.font.Font(None, 48)
space = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'back.png')), (WIDTH * WALL_WIDTH, HEIGHT * WALL_HEIGHT))
cells = numpy.random.randint(2, size = (WIDTH, HEIGHT))

walls = pygame.sprite.Group()
goods = pygame.sprite.Group()
bombermans = pygame.sprite.Group()
scores = pygame.sprite.Group()
bombs = pygame.sprite.Group()

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x * WALL_WIDTH, y * WALL_HEIGHT, WALL_WIDTH, WALL_HEIGHT)
        self.image =  pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'wall.png')), (WALL_WIDTH, WALL_HEIGHT))
        walls.add(self)
        
    def explose(self):
        ver = random.random()
        if  ver < 0.33:
            self.goods = Goods(self.x, self.y)
        walls.remove(self)
        del self

class Goods(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.rect = pygame.Rect((x + 0.25) * WALL_WIDTH, (y + 0.25) * WALL_HEIGHT, WALL_WIDTH / 2, WALL_HEIGHT / 2)
        ver = random.random()
        if  ver < 0.20:
            self.image = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'hart.png')), (WALL_WIDTH / 2, WALL_HEIGHT / 2))
            self.kind = 'life'
        elif ver > 0.60:
            self.image = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'goods.png')), (WALL_WIDTH / 2, WALL_HEIGHT / 2))
            self.kind = 'force'
        elif 0.20 <= ver <= 0.60:
            self.image = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'bombplus.png')), (WALL_WIDTH / 2, WALL_HEIGHT / 2))
            self.kind = 'bomb'
        goods.add(self)
    def explose(self):
        goods.remove(self)
        del self

class Score(pygame.sprite.Sprite):
    lives = 3
    bomb_force = 1
    mbombs = 1
    mscores = 0
    def __init__(self, id):
        super().__init__()
        self.rect = pygame.Rect(((id - 1) * WALL_WIDTH) * 2, WALL_HEIGHT / 4, WALL_WIDTH * 2, WALL_HEIGHT)
        self.image = (pygame.Surface([WALL_WIDTH * 2, WALL_HEIGHT], pygame.SRCALPHA, 32)).convert_alpha()
        self.text = font.render(str(self.mscores) + " | " + str(self.lives) + " | " + str(self.bomb_force) + " | " + str(self.mbombs), True, (255, 255, 255))
        self.image.blit(self.text, [0, 0])
        self.id = id
        scores.add(self)
    def updatescores(self):
        self.image = (pygame.Surface([WALL_WIDTH * 2, WALL_HEIGHT], pygame.SRCALPHA, 32)).convert_alpha()
        self.text = font.render(str(self.mscores) + " | " + str(self.lives) + " | " + str(self.bomb_force) + " | " + str(self.mbombs), True, (255, 255, 255))
        self.image.blit(self.text, [0, 0])

class Bomberman(pygame.sprite.Sprite):
    width, height = WALL_WIDTH * 0.8, WALL_HEIGHT * 0.8
    vel = 5
    bomb_time = 3000
    lives = 3
    bomb_force = 1
    mbombs = 1
    mscores = 0
    def __init__(self, id, x, y, left, right, up, down, drop):
        super().__init__()
        self.x = x
        self.y = y
        self.id = id
        self.rect = pygame.Rect(self.x * WALL_WIDTH, self.y * WALL_HEIGHT, self.width * 0.8, self.height * 0.8)
        self.image = pygame.transform.scale(pygame.image.load(os.path.join('Assets', "bomberman" + str(id) + "right.png")), (self.width, self.height))
        self.left = left
        self.right = right
        self.up = up
        self.down = down
        self.drop = drop
        self.freespace()
        self.score = Score(self.id)
        self.updatescores()
        bombermans.add(self)
    def updatescores(self):
            self.score.mscores = self.mscores
            self.score.lives = self.lives
            self.score.mbombs = self.mbombs
            self.score.bomb_force = self.bomb_force
            self.score.updatescores()
    def move(self, dx, dy):
        self.x =  self.rect.center[0] // WALL_WIDTH
        self.y =  self.rect.center[1] // WALL_HEIGHT
        if dx > 0:
            self.rect.x += dx
            self.image = pygame.transform.scale(pygame.image.load(os.path.join('Assets', "bomberman" + str(self.id) + "right.png")), (self.width, self.height))
        if dx < 0:
            self.rect.x += dx
            self.image = pygame.transform.scale(pygame.image.load(os.path.join('Assets', "bomberman" + str(self.id) + "left.png")), (self.width, self.height))
        if dy > 0:
            self.rect.y += dy
            self.image = pygame.transform.scale(pygame.image.load(os.path.join('Assets', "bomberman" + str(self.id) + "down.png")), (self.width, self.height))
        if dy < 0:
            self.rect.y += dy
            self.image = pygame.transform.scale(pygame.image.load(os.path.join('Assets', "bomberman" + str(self.id) + "up.png")), (self.width, self.height))
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0:
                    self.rect.right = wall.rect.left
                if dx < 0:
                    self.rect.left = wall.rect.right
                if dy > 0:
                    self.rect.bottom = wall.rect.top
                if dy < 0:
                    self.rect.top = wall.rect.bottom
        for bomb in bombs:
            if self.x != bomb.x or self.y != bomb.y:
                if self.rect.colliderect(bomb.rect):
                    if dx > 0:
                        self.rect.right = bomb.rect.left
                    if dx < 0:
                        self.rect.left = bomb.rect.right
                    if dy > 0:
                        self.rect.bottom = bomb.rect.top
                    if dy < 0:
                        self.rect.top = bomb.rect.bottom
        for good in goods:
            if self.rect.colliderect(good.rect):
                if good.kind == 'life':
                    self.lives += 1
                if good.kind == 'force':
                    self.bomb_force += 1
                if good.kind == 'bomb':
                    self.mbombs += 1
                self.updatescores()
                good.explose()
    def keys(self, keys_pressed):
        if keys_pressed[self.left] and self.rect.x - self.vel > 0:  # LEFT
            self.move(-self.vel, 0)
        if keys_pressed[self.right] and self.rect.x + self.vel + self.width < WIDTH * WALL_WIDTH:  # RIGHT
            self.move(self.vel, 0)
        if keys_pressed[self.up] and self.rect.y - self.vel > 0:  # UP
            self.move(0, -self.vel)
        if keys_pressed[self.down] and self.rect.y + self.vel + self.height < HEIGHT * WALL_HEIGHT:  # DOWN
            self.move(0, self.vel)
        if keys_pressed[self.drop] and self.rect.x - self.vel > 0:  # LEFT
            self.dropbomb()
    def freespace(self):
        cells[self.x, self.y] = 0
        cells[self.x + 1, self.y] = 0
        cells[self.x + 1, self.y + 1] = 0
    def dropbomb(self):
        exist = False
        for bomb in bombs:
            if bomb.x == self.x and bomb.y == self.y:
                exist = True
        if not exist:
            if self.mbombs > 0:
                bomb = Bomb(self.x, self.y, self.bomb_time, self.bomb_force, self.id)
    def kill(self):
        self.lives -= 1
        self.updatescores()
        if self.lives < 1:
            bombermans.remove(self)
            del self

class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y, bomb_time, bomb_force, bomberman_id):
        super().__init__()
        self.x = x
        self.y = y
        self.bomberman_id = bomberman_id
        self.rect = pygame.Rect((x + 0.25) * WALL_WIDTH, (y + 0.25) * WALL_HEIGHT, WALL_WIDTH / 2, WALL_HEIGHT / 2)
        self.image = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'bomb.png')), (WALL_WIDTH / 2, WALL_HEIGHT / 2))
        self.bomb_time = bomb_time
        self.bomb_force = bomb_force
        self.new = 1
        for bomberman in bombermans:
            if bomberman.id == self.bomberman_id:
                bomberman.mbombs -= 1
                bomberman.updatescores()
        self.sound = pygame.mixer.Sound(os.path.join('Assets', 'bomb.wav'))
        exist = False
        for bomb in bombs:
            if bomb.rect.x == self.rect.x and bomb.rect.y == self.rect.y:
                exist = True
        if not exist: 
            self.start_time = pygame.time.get_ticks()
            bombs.add(self)
    def explose(self):
        todetonate = []
        todestroy = []
        toexplose = []
        tokill = []
        self.sound.play()
        for good in goods:
            if (abs(good.x - self.x) <= self.bomb_force and good.y == self.y) or \
               (abs(good.y - self.y) <= self.bomb_force and good.x == self.x):
                todestroy.append(good)
        for good in todestroy:
            good.explose()
        
        #for i in range(self.bomb_force+1):
        #    left = 0
        #    right = 0
        #    up = 0
        #    down = 0
        #    for wall in walls:
        #        if wall.y == self.y:
        #            if 0 < wall.x - self.x <= i and not right:
        #                toexplose.append(wall)
        #                right = 1
        #                print('right')
        #            elif 0 < self.x - wall.x <= i and not left: 
        #                toexplose.append(wall)
        #                left = 1
        #                print('left')
        #        elif wall.x == self.x:
        #            if 0 < wall.y - self.y <= i and not down:
        #                toexplose.append(wall)
        #                down = 1
        #                print('down')
        #            elif 0 < self.y - wall.y <= i and not up:
        #                toexplose.append(wall)
        #                up = 1
        #                print('up')

        for wall in walls:
            if (abs(wall.x - self.x) <= self.bomb_force and wall.y == self.y) or \
               (abs(wall.y - self.y) <= self.bomb_force and wall.x == self.x):
                toexplose.append(wall)
        for wall in toexplose:
            wall.explose()
        for bomberman in bombermans:
            if (abs(bomberman.x - self.x) <= self.bomb_force and bomberman.y == self.y) or \
               (abs(bomberman.y - self.y) <= self.bomb_force and bomberman.x == self.x):
                tokill.append(bomberman)
            if bomberman.id == self.bomberman_id:
                bomberman.mbombs += 1
                bomberman.mscores += len(tokill)
                bomberman.updatescores()
        for bomberman in tokill:
                if bomberman.id == self.bomberman_id:
                    bomberman.mscores -= 1
                bomberman.kill()
        if self in bombs:
            bombs.remove(self)
        for bomb in bombs:
            if (abs(bomb.x - self.x) <= self.bomb_force and bomb.y == self.y) or \
               (abs(bomb.y - self.y) <= self.bomb_force and bomb.x == self.x):
                todetonate.append(bomb)
        for bomb in todetonate:
            bomb.explose()
        del self

bomberman1 = Bomberman(1, 1, 3, pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_LCTRL)
bomberman2 = Bomberman(2, 7, 3, pygame.K_LEFT, pygame.K_RIGHT,pygame.K_UP, pygame.K_DOWN, pygame.K_RCTRL)

for x in range(WIDTH):
    for y in range(HEIGHT):
        if cells[x,y] == 1:
            wall = Wall(x, y)

def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

        pygame.display.flip()

        window.blit(space, (0, 0))

        curent_time = pygame.time.get_ticks()
        for bomb in bombs:
            if curent_time - bomb.start_time > bomb.bomb_time - 200:
                bomb.rect = pygame.Rect(bomb.x * WALL_WIDTH, bomb.y * WALL_HEIGHT, WALL_WIDTH, WALL_HEIGHT)
                bomb.image = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'bomb.png')), (WALL_WIDTH, WALL_HEIGHT))
                if curent_time - bomb.start_time > bomb.bomb_time:
                    bomb.explose()

        keys_pressed = pygame.key.get_pressed()
        for bomberman in bombermans:
            bomberman.keys(keys_pressed)

        bombs.draw(window)
        walls.draw(window)
        goods.draw(window)
        bombermans.draw(window)
        scores.draw(window)
        
        clock.tick(FPS)

if __name__ == "__main__":
    main()