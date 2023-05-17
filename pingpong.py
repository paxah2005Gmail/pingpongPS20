#создай игру "Лабиринт"!
from pygame import *
from random import randint
from time   import time as tm

class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, sizeX, sizeY, speed=0):
        super().__init__()
        self.img = transform.scale(image.load(img), (sizeX, sizeY))
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
    def reset(self):
        mw.blit(self.img, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def __init__(self, img, sizeX, sizeY, speed=0, id=0):
        if id == 1:
            super().__init__(img, 0, maxY - sizeY, sizeX, sizeY, speed)  
        else:
            super().__init__(img, maxX - sizeX, maxY - sizeY, sizeX, sizeY, speed) 
        self.id = id   
    def keyProcessing(self):
        keys = key.get_pressed()
        if self.id == 1:
            if keys[K_w]:
                self.rect.y -= self.speed
            if keys[K_s]:
                self.rect.y += self.speed
        else:
            if keys[K_UP]:
                self.rect.y -= self.speed
            if keys[K_DOWN]:
                self.rect.y += self.speed

        if self.rect.y > (maxY - self.rect.height):
            self.rect.y = (maxY - self.rect.height)
        elif self.rect.y < 0:
            self.rect.y = 0

class Ball(GameSprite):
    def __init__(self, img, x, y, sizeX, sizeY, speed=0):
        super().__init__(img, x, y, sizeX, sizeY, speed)
        self.speedX = (1 - 2*(randint(0, 1))) * speed
        self.speedY = (1 - 2*(randint(0, 1))) * speed
    
    def move(self):
        self.rect.x += self.speedX
        self.rect.y += self.speedY
        if (self.rect.y <= 0):
            self.speedY *= -1
            return 3
        if ( self.rect.y + self.rect.height >= maxY):
            self.speedY *= -1
            return 4
        if (self.rect.x <= 0):
            self.speedX *= -1
            return 1
        if ( self.rect.x + self.rect.width >= maxX):
            self.speedX *= -1
            return 2
        return 0

maxX = 1280
maxY = 720
mw = display.set_mode((maxX, maxY))
display.set_caption('PingPong')
bgColor = (255, 255, 255)
#mixer.init()#инициализировать микшер
#mixer.music.load('space.ogg')#загрузить фоновую музыку
#mixer.music.play()#начать воспроизведение фоновой музыки
#fire = mixer.Sound('fire.ogg')#загрузить звук выстрела

game = True
clock = time.Clock()
#bg = GameSprite('galaxy.jpg', 0, 0, maxX, maxY)
playerL = Player('red.png',  25, 100, 5, 1)
playerR = Player('blue.png', 25, 100, 5, 2)
ball = Ball('ball.png', (maxX - 35)//2, (maxY - 35)//2, 35, 35, 3) 

font.init()
font_ = font.SysFont('Arial', 70)
victoryL = font_.render('Player 1 WON', True, (255, 0, 0))
victoryR = font_.render('Player 2 WON', True, (255, 0, 0))

gameRes = 0
while game:
    if gameRes == 0:
        mw.fill(bgColor)
        playerL.keyProcessing()      
        playerR.keyProcessing() 
        gameRes = ball.move()   
        if gameRes > 2:
            gameRes = 0
        if sprite.collide_rect(ball, playerL) or sprite.collide_rect(ball, playerR):
            ball.speedX *= -1 
        playerL.reset()
        playerR.reset()
        ball.reset()
    elif gameRes == 1:
        mw.blit(victoryL, (maxX//2, maxY//2))
    else:
        mw.blit(victoryR, (maxX//2, maxY//2))
    for e in event.get():
        if e.type == QUIT:
            game = False
    display.update()
    clock.tick(50)