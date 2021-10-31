import pygame, sys
import random, math
from pygame.locals import *
import pandas as pd
class muur(pygame.sprite.Sprite):
    def __init__(self,x,y,grote,kleur):

        self.image      = pygame.Surface((grote,grote))
        self.rect       = self.image.get_rect()
        self.rect.left  = x
        self.rect.top   = y
        pygame.Surface.fill(self.image ,kleur)
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer

    def update(self,x,y):
        self.rect.left  = x
        self.rect.top   = y

class speler(pygame.sprite.Sprite):
    def __init__(self,grote,catImg):
        self.grote = grote
        self.image      = pygame.Surface((int(grote), int(grote)))
        self.rect       = self.image.get_rect()
        self.snelheid   = 5
        self.rect.left  = startx
        self.rect.top   = starty
        self.image = self.image.convert_alpha()
        pygame.Surface.fill(self.image ,(10,0,0,100))
        catImg2 = pygame.transform.scale(catImg, (int(grote), int(grote)))
        self.image.blit(catImg2, (0, 0))
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
    def update(self,links,rechts,boven,beneden):
        if rechts:
            self.rect.left += self.snelheid
            if self.rect.left > scherm_grote_x - self.grote:
                self.rect.left = scherm_grote_x - self.grote
            if len(pygame.sprite.spritecollide(self,muren,0)) != 0:
                self.rect.left -= self.snelheid
        if links:
            self.rect.left -= self.snelheid
            if self.rect.left < 0:
                self.rect.left = 0
            if len(pygame.sprite.spritecollide(self, muren, 0)) != 0:
                self.rect.left += self.snelheid
        if boven:
            self.rect.top -= self.snelheid
            if self.rect.top < 0:
                self.rect.top = 0
            if len(pygame.sprite.spritecollide(self, muren, 0)) != 0:
                self.rect.top += self.snelheid
        if beneden:
            self.rect.top += self.snelheid
            if self.rect.top > scherm_grote_y - self.grote:
                self.rect.top = scherm_grote_y - self.grote
            if len(pygame.sprite.spritecollide(self, muren, 0)) != 0:
                self.rect.top -= self.snelheid
        if pygame.sprite.collide_rect(self, doel):
            self.rect.left = startx
            self.rect.top = starty
def main():
    global scherm_grote_y, scherm_grote_x,sizeball, muren, doel, startx, starty
    pygame.init()

    FPS = 60       # frames per second setting
    fpsClock = pygame.time.Clock()

    scherm_grote_x = 500
    scherm_grote_y = 500
    aantal_tegels_x = 10
    Aantal_tegels_y = 10
    grote_muur = scherm_grote_x / aantal_tegels_x
    # set up the window

    DISPLAYSURF = pygame.display.set_mode((scherm_grote_x, scherm_grote_y))
    pygame.display.set_caption('Doolhof')

    AQUA = (0, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)
    FUCHSIA = (255, 0, 255)
    GRAY = (128, 128, 128)
    GREEN = (0, 128, 0)
    LIME = (0, 255, 0)
    MAROON = (128, 0, 0)
    NAVYBLUE = (0, 0, 128)
    OLIVE = (128, 128, 0)
    PURPLE = (128, 0, 128)
    RED = (255, 0, 0)
    SILVER = (192, 192, 192)
    TEAL = (0, 128, 128)
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)
    grote_kat = grote_muur - 25
    catImg = pygame.image.load('boy.png')
    catx = 10
    caty = 10
    links = False
    rechts = False
    boven = False
    beneden = False
    snelheid = 10
    muren = []
    allsprites = pygame.sprite.RenderPlain()
    startx = 0
    starty = 0 #scherm_grote_y - grote_kat
    coor = [[1,0],[1,1],[1,2]]
    df = pd.read_excel(r'doolhof1.xlsx')  # for an earlier version of Excel, you may need to use the file extension of 'xls'
    x = pd.DataFrame(df, columns=['x'])
    y = pd.DataFrame(df, columns=['y'])
    for row in df.values:
        x = row[0] - 1
        y = -(row[1]-11) - 1
        muren.append(muur(x * grote_muur, y * grote_muur, grote_muur , SILVER ))
    Speler = speler( grote_kat, catImg)
    x = 2
    y = 9
    doel = muur(x * grote_muur, y * grote_muur, grote_muur , BLACK )
    allsprites.add(muren)
    allsprites.add(Speler)
    allsprites.add(doel)
    while True: # the main game loop

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    rechts = True
                elif event.key == K_DOWN:
                    beneden = True
                elif event.key == K_LEFT:
                    links = True
                elif event.key == K_UP:
                    boven = True
            if event.type == KEYUP:
                if event.key == K_RIGHT:
                    rechts = False
                elif event.key == K_DOWN:
                    beneden = False
                elif event.key == K_LEFT:
                    links = False
                elif event.key == K_UP:
                    boven = False


        DISPLAYSURF.fill(SILVER)
        Speler.update(links,rechts,boven,beneden)


        allsprites.draw(DISPLAYSURF)

        pygame.display.update()
        fpsClock.tick(FPS)

if __name__ == '__main__':
    main()