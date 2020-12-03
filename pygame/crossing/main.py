import random, sys, copy, os, pygame
from pygame.locals import *
try:
    import android
except ImportError:
    android = None


#multiplayer

def main():
    global FPSCLOCK, DISPLAYSURF, ALPHADISPLAYSURF,menuitem    
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
    
    WINWIDTH     = 800# mynative[0][0] # width of the program's window, in pixels
    WINHEIGHT    = 600# mynative[0][1] # height in pixels
    FPS          = 100  # number of frames per second
    PLAYERHEIGHT = int(WINWIDTH/50)   # height of the player in pixels
    PLAYERWIDTH  = int(WINWIDTH/50)

    Player0bj = {'x'     :int(WINWIDTH /2),
                 'y'     :WINHEIGHT-PLAYERHEIGHT,
                 'xstart':WINWIDTH /2,
                 'ystart':WINHEIGHT-PLAYERHEIGHT,
                 'lives' : 3,
                 'points': 10000}
    
    [CARHEIGHT,CARWIDTH, road0bj, car0bj,Player0bj,NIGHT,NLANES]=start(WINHEIGHT,WINWIDTH,PLAYERHEIGHT,Player0bj)
    
      #Initializing pygame
    
    pygame.key.set_repeat(1)
    # making a clock
    FPSCLOCK = pygame.time.Clock()
    #creating a Display surface and a aplha surface
    DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT) )
    ALPHADISPLAYSURF = DISPLAYSURF.convert_alpha()
    #plotting the background for the game
    plotbackground(GREEN)
    #plotting the road
    plotroad(road0bj,WHITE,GRAY,WINWIDTH,WINHEIGHT)
    restarting = False
    Moveleft  = False
    Moveright = False
    Moveup    = False
    Movedown  = False
    Buttonpressed = False
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if(event.key == K_ESCAPE):
                     terminate()
                elif(event.key == K_LEFT or event.key ==K_KP4):
                    Moveleft  = True
                    Moveright = False
                    Movedown  = False
                    Moveup    = False
                elif(event.key == K_RIGHT or event.key ==K_KP6):
                    Moveleft  = False
                    Moveright = True
                    Movedown  = False
                    Moveup    = False
                elif(event.key == K_UP or event.key ==K_KP8):
                    Moveleft  = False
                    Moveright = False
                    Movedown  = False
                    Moveup    = True
                elif(event.key == K_DOWN or event.key ==K_KP2):
                    Moveleft  = False
                    Moveright = False
                    Movedown  = True
                    Moveup    = False
                elif (event.key == K_KP7):
                    Moveleft  = True
                    Moveup    = True
                    Moveright = False
                    Movedown  = False
                elif (event.key == K_KP9):
                    Moveright = True
                    Moveup    = True
                    Moveleft  = False
                    Movedown  = False
                elif (event.key == K_KP3):
                    Moveright = True
                    Movedown  = True
                    Moveleft  = False
                    Moveup    = False
                elif (event.key == K_KP1):
                    Moveleft  = True
                    Movedown  = True
                    Moveup    = False
                    Moveright = False
            elif event.type == MOUSEBUTTONDOWN:                
                Buttonpressed = True
            elif event.type == MOUSEBUTTONUP:
                Moveleft  = False
                Moveright = False
                Moveup    = False
                Movedown  = False
                Buttonpressed = False
            if Buttonpressed:
                (mousex,mousey) = pygame.mouse.get_pos()
                if mousex > (Player0bj['x']+PLAYERWIDTH):
                    Moveright = True
                    Moveleft  = False
                elif mousex <(Player0bj['x']):
                    Moveright = False
                    Moveleft  = True
                else:
                    Moveright = False
                    Moveleft  = False
                if mousey > (Player0bj['y']+PLAYERHEIGHT) :
                    Movedown = True
                    Moveup   = False
                elif mousey < (Player0bj['y']):
                    Movedown = False
                    Moveup  = True
                else:
                    Movedown = False
                    Moveup   = False


        moveplayer(Player0bj,Moveup,Movedown,Moveleft,Moveright,WINWIDTH,WINHEIGHT,PLAYERHEIGHT,PLAYERWIDTH)
        if android == None:
            Moveleft  = False
            Moveright = False
            Moveup    = False
            Movedown  = False

        movecar(car0bj,WINWIDTH,CARWIDTH)
        [CARHEIGHT,CARWIDTH, road0bj, car0bj,NLANES,NIGHT,restarting]=checkcolission(Player0bj,car0bj,road0bj,PLAYERHEIGHT,PLAYERWIDTH,CARHEIGHT,CARWIDTH,NLANES,WINHEIGHT,WINWIDTH,NIGHT)
        if restarting:
            restarting = False
            Moveleft  = False
            Movedown  = False
            Moveup    = False
            Moveright = False         
        plotbackground(GREEN)
        pygame.draw.rect(ALPHADISPLAYSURF,(0,0,0,NIGHT*240),(0,0,WINWIDTH,WINHEIGHT))
        plotroad(road0bj,WHITE,GRAY,WINWIDTH,WINHEIGHT)
        plotplayer(Player0bj,YELLOW,PLAYERHEIGHT,PLAYERWIDTH)
        plotcar(car0bj,CARHEIGHT,CARWIDTH)
        DISPLAYSURF.blit(ALPHADISPLAYSURF,(0,0))
        plothealth(Player0bj,RED)
        pygame.display.update()
        Player0bj['points'] = Player0bj['points'] -1
        FPSCLOCK.tick(FPS)


        
def plotbackground(COLOUR):
#plots the background map
    global DISPLAYSURF
    DISPLAYSURF.fill(COLOUR)


    
def plotroad(road0bj,WHITE,GRAY,WINWIDTH,WINHEIGHT):
    global DISPLAYSURF
    WIDTHSTRIPE  = 40
    HEIGHTSTRIPE = int(WINHEIGHT/(len(road0bj)+2)*0.05)+1
    HEIGHTLANE = int(WINHEIGHT/(len(road0bj)+2))
    pygame.draw.rect(DISPLAYSURF,GRAY,(0,(1)*HEIGHTLANE,WINWIDTH,len(road0bj)*HEIGHTLANE))
    for j in range(len(road0bj)-1):
        roads = road0bj[j]       
        for i in range( int(WINWIDTH/(2*WIDTHSTRIPE))+2):
            pygame.draw.rect(DISPLAYSURF,WHITE,(WIDTHSTRIPE*(2*i-1),(j+2)*HEIGHTLANE-HEIGHTSTRIPE/2 ,WIDTHSTRIPE,HEIGHTSTRIPE ))     
    pygame.draw.rect(DISPLAYSURF,WHITE,(0,HEIGHTLANE,WINWIDTH,HEIGHTSTRIPE))
    pygame.draw.rect(DISPLAYSURF,WHITE,(0,(len(road0bj)+1)*HEIGHTLANE,WINWIDTH,HEIGHTSTRIPE))



def plotplayer(Player0bj,COLOUR,PLAYERHEIGHT,PLAYERWIDTH):
    global DISPLAYSURF   
    pygame.draw.rect(DISPLAYSURF,COLOUR,(Player0bj['x'],Player0bj['y'],PLAYERWIDTH,PLAYERHEIGHT))



def plotcar(car0bj,CARHEIGHT,CARWIDTH):
    global DISPLAYSURF, ALPHADISPLAYSURF
    kleur = (255,255,255,100)
    LH = int(CARHEIGHT / 5)
    LS = int(CARHEIGHT /2)
    LD = 1
    for car in car0bj:
        pygame.draw.rect(DISPLAYSURF,car['Colour'],(car['x'],car['y'],CARWIDTH,CARHEIGHT))
        pygame.draw.rect(DISPLAYSURF,(0,0,0),(car['x'],car['y'],CARWIDTH,CARHEIGHT),4)
        pygame.draw.rect(DISPLAYSURF,(0,0,0),(car['x'],car['y'],int(CARWIDTH/4),CARHEIGHT),4)
        pygame.draw.rect(DISPLAYSURF,(0,0,0),(car['x']+int(3*CARWIDTH/4),car['y'],int(CARWIDTH/4),CARHEIGHT),4)
        #lights
        if car['speed'] > 0:            
            pygame.draw.polygon(ALPHADISPLAYSURF,(255, 255, 255,100),((car['x']+CARWIDTH,car['y']),(car['x']+CARWIDTH,car['y']+LH),(car['x']+(LD+1)*CARWIDTH,car['y']+LS),(car['x']+(LD+1)*CARWIDTH,car['y']-LS+LH)))
            pygame.draw.polygon(ALPHADISPLAYSURF,(255, 255, 255,100),((car['x']+CARWIDTH,car['y']+CARHEIGHT-LH),(car['x']+CARWIDTH,car['y']+CARHEIGHT),(car['x']+(LD+1)*CARWIDTH,car['y']+LS+CARHEIGHT),(car['x']+(LD+1)*CARWIDTH,car['y']-LS+LH+CARHEIGHT)))
          
        else:            
            pygame.draw.polygon(ALPHADISPLAYSURF,(255, 255, 255,100),((car['x'],car['y']),(car['x'],car['y']+LH),(car['x']-LD*CARWIDTH,car['y']+LS),(car['x']-LD*CARWIDTH,car['y']-LS+LH)))
            pygame.draw.polygon(ALPHADISPLAYSURF,(255, 255, 255,100),((car['x'],car['y']+CARHEIGHT-LH),(car['x'],car['y']+CARHEIGHT),(car['x']-LD*CARWIDTH,car['y']+LS+CARHEIGHT),(car['x']-LD*CARWIDTH,car['y']-LS+LH+CARHEIGHT)))


def plothealth(Player0bj,COLOUR):
    global DISPLAYSURF
    for i  in range(Player0bj['lives']):
        pygame.draw.rect(DISPLAYSURF,COLOUR,(20+i*20,20,10,10))
        pygame.font.SysFont 
    menuFont0bj = pygame.font.SysFont ('freesansbold.ttf',30)
    AQUA    = (  0, 255, 255)
    message = str( Player0bj['points'])
    points = menuFont0bj.render(message, True , AQUA)
    textrect = points.get_rect()
    textrect.center=(50,50)
    DISPLAYSURF.blit(points,textrect)    



def moveplayer(Player0bj,Moveup,Movedown,Moveleft,Moveright,WINWIDTH,WINHEIGHT,PLAYERHEIGHT,PLAYERWIDTH): 
    Moverate = 5
    if Moveleft and Moveup:
        Player0bj['x']    -= Moverate
        Player0bj['y']    -= Moverate
    elif Moveright and Moveup:
        Player0bj['x']    += Moverate
        Player0bj['y']    -= Moverate
    elif Moveleft and Movedown:
        Player0bj['x']    -= Moverate
        Player0bj['y']    += Moverate
    elif Moveright and Movedown:
        Player0bj['x']    += Moverate
        Player0bj['y']    += Moverate
    elif Moveleft:
        Player0bj['x']    -= Moverate
    elif Moveright:
        Player0bj['x']    += Moverate
    elif Moveup:
        Player0bj['y']    -= Moverate
    elif Movedown:
        Player0bj['y']    += Moverate
    if  Player0bj['y']  <= 0:
        Player0bj['y']  = 0
    elif Player0bj['y']  >= WINHEIGHT-PLAYERHEIGHT:
       Player0bj['y']  = WINHEIGHT-PLAYERHEIGHT
    if  Player0bj['x']  <= 0:
        Player0bj['x']  = 0
    elif Player0bj['x']  >= WINWIDTH-PLAYERWIDTH:
       Player0bj['x']  = WINWIDTH-PLAYERWIDTH


       
def makenewcar(i,j,road,WINWIDTH,NLANES,WINHEIGHT,CARHEIGHT,CARWIDTH):
    HEIGHTSTRIPE = int(WINHEIGHT/(NLANES+2)*0.05)+1
    if road['Dire'] == 'left':
        speed = -road['speed']
        #x= WINWIDTH-j*(int(WINWIDTH/road['NCARS'])+2*CARWIDTH)
    else:
        speed = road['speed']
    x = j*int(WINWIDTH/road['NCARS'])+2*CARWIDTH
    y1 = (i+1.5)*(float(WINHEIGHT)/(float(NLANES+2)))
    y2 = int(float(CARHEIGHT)/2)
    y3= int(float(HEIGHTSTRIPE)/2)
    y = y1-y2-y3
    y = int(y)
    car={'x'  : x,
         'y'  : y,
         'Colour' : (  random.randint(0,255),  random.randint(0,255),  random.randint(0,255)),
         'speed' :  speed}
    return car



def movecar(car0bj,WINWIDTH,CARWIDTH):
    for i in range(len( car0bj)-1,-1,-1):
        car = car0bj[i]
        car['x'] = car['x'] + car['speed']

        if car['x'] >= WINWIDTH and car['speed'] > 0:
            car['x'] = 0-2*CARWIDTH
        elif car['x'] <= (0-CARWIDTH) and car['speed'] < 0:
            car['x'] = WINWIDTH+CARWIDTH


def checkcolission(Player0bj,car0bj,road0bj,PLAYERHEIGHT,PLAYERWIDTH,CARHEIGHT,CARWIDTH,NLANES,WINHEIGHT,WINWIDTH,NIGHT, PLAYER):
    restarting = False
    for car in car0bj:
        if Player0bj['x'] +PLAYERWIDTH > car['x'] and Player0bj['x'] < car['x']+CARWIDTH:
            if Player0bj['y']+PLAYERHEIGHT> car['y'] and Player0bj['y'] < car['y']+CARHEIGHT:
                Player0bj['x'] =  Player0bj['xstart'] 
                Player0bj['y'] =  Player0bj['ystart']
                Player0bj['lives'] = Player0bj['lives']-1
                if android:
                    android.vibrate(1)    
                    
                if Player0bj['lives'] == 0:
                    message = 'You lost, press a key to restart'
                    [CARHEIGHT,CARWIDTH, road0bj, car0bj,Player0bj,NIGHT,NLANES]=winlose(CARHEIGHT,CARWIDTH, road0bj, car0bj,Player0bj,NIGHT,NLANES,WINHEIGHT,WINWIDTH,PLAYERHEIGHT,message)
                    restarting = True
    if Player0bj['y'] == 0:
        Player0bj['x'] =  Player0bj['xstart']
        Player0bj['y'] =  Player0bj['ystart']
        Player0bj['lives' ]  = Player0bj['lives' ]  + 1
        NLANES = NLANES +1
        if NLANES > 5:
            NLANES = 3
            NIGHT  =  NIGHT
            PLAYER += 1
            if PLAYER > 4:
                message = 'De sleutel ligt in Jeruzalem'
                [CARHEIGHT,CARWIDTH, road0bj, car0bj,Player0bj,NIGHT,NLANES]=winlose(CARHEIGHT,CARWIDTH, road0bj, car0bj,Player0bj,NIGHT,NLANES,WINHEIGHT,WINWIDTH,PLAYERHEIGHT,message)
                restarting = True
        [CARHEIGHT,CARWIDTH, road0bj, car0bj]=makelanesandcars(NLANES,WINHEIGHT,WINWIDTH)
    return CARHEIGHT,CARWIDTH, road0bj, car0bj, NLANES, NIGHT, restarting


                
def makelanesandcars(NLANES,WINHEIGHT,WINWIDTH):
    CARHEIGHT    = int(WINHEIGHT/(2+NLANES)*0.75)
    CARWIDTH = CARHEIGHT*2
    road0bj   = []
    car0bj = []
    for i in range(NLANES):
        di = random.randint(0,1000)
        if di < 500:
            dire = 'left'
        else:
            dire = 'right'
        speed = random.randint(1,5)
        road0bj.append({'line' :'stripe',
                        'Dire' :dire,
                        'speed': int(speed),
                        'NCARS': random.randint(1,max(1,int(WINWIDTH/(3*CARWIDTH))))    })
        road = road0bj[i]
        for j in range (road['NCARS']):
            car0bj.append(makenewcar(i,j,road,WINWIDTH,NLANES, WINHEIGHT,CARHEIGHT,CARWIDTH))
    return CARHEIGHT,CARWIDTH, road0bj, car0bj



def winlose(CARHEIGHT,CARWIDTH, road0bj, car0bj,Player0bj,NIGHT,NLANES,WINHEIGHT,WINWIDTH,PLAYERHEIGHT,message):
    global DISPLAYSURF
    FPS = 100
    menuFont0bj =pygame.font.SysFont ('freesansbold.ttf',60)
    AQUA    = (  0, 255, 255)
    SILVER  = (192, 192, 192)
    lost = menuFont0bj.render(message, True , AQUA,SILVER)
    textrect = lost.get_rect()
    textrect.center=(WINWIDTH/2,WINHEIGHT/2,)
    DISPLAYSURF.blit(lost,textrect)    
    pygame.display.update()
    waiting = True
    pygame.key.set_repeat(100)
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()            
            elif event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
                waiting = False
                [CARHEIGHT,CARWIDTH, road0bj, car0bj,Player0bj,NIGHT,NLANES]=start(WINHEIGHT,WINWIDTH,PLAYERHEIGHT,Player0bj)
        FPSCLOCK.tick(FPS)
    pygame.key.set_repeat(1)
    return CARHEIGHT,CARWIDTH, road0bj, car0bj,Player0bj,NIGHT,NLANES
    
def start(WINHEIGHT,WINWIDTH,PLAYERHEIGHT,Player0bj):
    
    NIGHT = 0
    NLANES = 3 # number of lanes
    PLAYER = 1
    # creating the lanes and the cars
    [CARHEIGHT,CARWIDTH, road0bj, car0bj]=makelanesandcars(NLANES,WINHEIGHT,WINWIDTH)

    #making the player
    
    Player0bj['x']      = WINWIDTH /2
    Player0bj['y']      = WINHEIGHT-PLAYERHEIGHT
    Player0bj['xstart'] = WINWIDTH /2
    Player0bj['ystart'] = WINHEIGHT-PLAYERHEIGHT
    Player0bj['lives' ] = 3
    Player0bj['points' ] = 10000
    return  CARHEIGHT,CARWIDTH, road0bj, car0bj,Player0bj,NIGHT,NLANES



def terminate():
    pygame.quit()
    sys.exit()


    
if __name__ == '__main__':
    main()
