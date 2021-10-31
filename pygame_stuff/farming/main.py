import random, sys, copy, os, pygame, math, tiles
from pygame.locals import *
try:
    import android
except ImportError:
    android = None

def main():
    global DISPLAYSURF,menuitem    
# defining collors to be used later
    AQUA    = (  0, 255, 255)
    BLACK   = (  0,   0,   0)
    BLUE    = (  0,   0, 255)
    FUCHSIA = (255,   0, 255)
    GRAY    = (128, 128, 128)
    GREEN   = (  0, 128,   0)
    LIME    = (  0, 255,   0)
    MAROON  = (128,   0,   0)
    NAVYBLUE= (  0,   0, 128)
    OLIVE   = (128, 128,   0)
    PURPLE  = (128,   0, 128)
    RED     = (255,   0,   0)
    SILVER  = (192, 192, 192)
    TEAL    = (  0, 128, 128)
    WHITE   = (255, 255, 255,0)
    YELLOW  = (255, 255,   0)
    
    pygame.init()
    mynative = pygame.display.list_modes() # Default
    s_res = (mynative[0][0],mynative[0][1])
    if android:
        android.init()
        android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)
    
    WINWIDTH     = mynative[0][0] # width of the program's window, in pixels
    WINHEIGHT    = mynative[0][1] # height in pixels
    FPS          = 60  # number of frames per second
    
    n_hori_tiles = 3;
    sizetile = math.floor(WINWIDTH/n_hori_tiles)
    n_vert_tiles = math.floor(WINHEIGHT/sizetile)
     
    # making a clock
    FPSCLOCK = pygame.time.Clock()
    #creating a Display surface and a aplha surface
    DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT) ,FULLSCREEN)

    #plotting the background for the game
    plotbackground(GREEN)


    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if(event.key == K_ESCAPE):
                     terminate()
 

        plotbackground(GREEN)
        pygame.display.update()
        FPSCLOCK.tick(FPS)


        
def plotbackground(COLOUR):
#plots the background map
    global DISPLAYSURF
    DISPLAYSURF.fill(COLOUR)


 
def terminate():
    pygame.quit()
    sys.exit()


    
if __name__ == '__main__':
    main()
