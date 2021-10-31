import random, sys, copy, os, pygame, math
from pygame.locals import *
try:
    import android
except ImportError:
    android = None

class Ball(pygame.sprite.Sprite):
    """Class for all the balls moving in the game"""
    def __init__(self,BLACK):
        self.X = random.randint(0,WINWIDTH)    
        self.Y = random.randint(0,WINHEIGHT)        
        self.D = random.randint(0,360)
        self.v = 5
        self.vx = int(math.cos(self.D/360.*math.pi*2)*self.v)
        self.vy = int( math.sin(self.D/360.*math.pi*2)*self.v )
        self.image = pygame.Surface((sizeball*2,sizeball*2))
        self.rect = self.image.get_rect()
        self.rect.left =self.X
        self.rect.top =self.Y
        self.image = self.image.convert_alpha()
        pygame.Surface.fill(self.image ,(0,0,0,0))        
        COLOUR = (  random.randint(0,255),  random.randint(0,255),  random.randint(0,255))
        pygame.draw.circle( self.image,COLOUR,(sizeball,sizeball ) ,sizeball)
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        counter = 1
        while len(pygame.sprite.spritecollide(self,balls,0)) > 0 and counter < 100:
            self.X = random.randint(0,WINWIDTH)
            self.Y = random.randint(0,WINHEIGHT)     
            self.rect.left =self.X
            self.rect.top =self.Y
            counter = counter +1
        
    def update(self):
        #moves the ball
        vy = self.vy
        newpos = self.rect.move((self.vx, self.vy))
#        newpos = self.rect
        if newpos.left <= -1:
            if self.D > 90 and self.D < 180:
                self.D = 180-self.D                
            elif self.D > 180 and self.D < 270:
                self.D = 180-self.D
            else:
                self.D  = self.D + 180    
            newpos.left = 0
        elif newpos.right >= WINWIDTH+1:
            if self.D> 0 and self.D < 90:
                self.D = 180-self.D                 
            elif self.D > 270 and self.D < 360:
                self.D = 180-self.D
            else:
                self.D = self.D+ 180
            newpos.right = WINWIDTH
        elif newpos.top <= -1:
            if self.D < 270:
                self.D = -self.D
            elif self.D > 270:
                self.D = -self.D
            else:
                self.D =self.D + 180
            newpos.top = 0
        elif newpos.bottom >= WINHEIGHT+1:
            if self.D > 0 and self.D < 90:
                self.D = -self.D
            elif self.D > 90 and self.D < 180:
                self.D = -self.D
            else:
                self.D = self.D + 180
            newpos.bottom = WINHEIGHT    
        oldpos = self.rect
        self.D = self.D%360
        self.vx = int(math.cos(self.D/360.*math.pi*2)*self.v)
        self.vy = int(math.sin(self.D/360.*math.pi*2)*self.v )
        self.rect = newpos
        #check if ball colides with the wall
        for wall in pygame.sprite.spritecollide(self,walls,0):
            if wall.D ==1:
                if wall.rect.bottom  <= self.rect.bottom:
                    if self.D == 270:
                        self.D = self.D + 180
                    else:
                        self.D = -self.D
                    newpos.top =  wall.rect.bottom
                elif wall.rect.bottom  >= self.rect.bottom:
                    if self.D > 0 and self.D < 90:
                        self.D = -self.D
                    elif self.D > 90 and self.D < 180:
                        self.D = -self.D
                    else:
                        self.D = self.D + 180
                    newpos.bottom = wall.rect.top
            else:
                if wall.rect.right >= self.rect.right:
                    self.D = 180-self.D
                    newpos.right = wall.rect.left
                elif wall.rect.right <= self.rect.right:
                    self.D = 180-self.D
                    newpos.left = wall.rect.right
        self.rect = oldpos
        self.D = self.D%360
        self.vx = int(math.cos(self.D/360.*math.pi*2)*self.v)
        self.vy =int( math.sin(self.D/360.*math.pi*2)*self.v )
        self.rect = newpos     
           
        #checking for colissions with other balls
        for ball in pygame.sprite.spritecollide(self,balls,0):
            # check if it is not the ball self andf it is n the circle.
            if ball != self and pygame.sprite.collide_circle(self,ball):
                #switching the directions of the balls
                oldD = self.D
                self.D = ball.D%360
                ball.D = oldD%360
                #putting then back so they are not on top of each other.
                y1 = self.rect.top
                x1 = self.rect.left
                y2 = ball.rect.top
                x2 = ball.rect.left
                x1  = math.cos(self.D/360.*math.pi*2)*self.v
                y1  = math.sin(self.D/360.*math.pi*2)*self.v
                x2  = math.cos(ball.D/360.*math.pi*2)*ball.v
                y2  = math.sin(ball.D/360.*math.pi*2)*ball.v
                self.rect.move(x1,y1)
                self.D = self.D%360
                self.vx = math.cos(self.D/360.*math.pi*2)*self.v
                self.vy = math.sin(self.D/360.*math.pi*2)*self.v 
                # setting ball to correct position
                ball.D = ball.D%360
                ball.rect.move(x2,y2)
                ball.vx = math.cos(ball.D/360.*math.pi*2)*ball.v
                ball.vy = math.sin(ball.D/360.*math.pi*2)*ball.v

            

                
class Mouse(pygame.sprite.Sprite):
    #class for the mouse cursos
    def __init__(self):
        
        (mousex,mousey) = pygame.mouse.get_pos()
        self.image      = pygame.Surface((sizeball*2,sizeball*2))
        self.rect       = self.image.get_rect()
        self.rect.left  = mousex
        self.rect.top   = mousey
        self.dir        = 1 #direction of mousbutton 1 is x, 0 is y
        self.BUTTON     = False # true when button 1 is presses
        pygame.Surface.fill(self.image ,(0,0,0))
        pygame.draw.line(self.image,RED,(0,sizeball),(sizeball*2,sizeball))
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        
    def update(self):
        global NBALS, lives
        BLACK   = (  0,   0,   0,0)
        ispeed= 30 
        if self.BUTTON:
            #if the button is presses the cursor is inflated in x or y direction
            if self.dir == 1:
                self.rect  =  self.rect.inflate(ispeed,0)
            else:
                self.rect= self.rect.inflate(0,ispeed)
            colwall  = pygame.sprite.spritecollide(self,walls,0)
            FINISHED = False
            i = -1
            colwal = []
            colwitwall = False
            colwitsame = False
            for cwall in colwall:
                i = i+1
                if cwall.D != self.dir:
                    colwitwall = True
                    colwal.append(i)
                else:
                    colwitsame = True

            if len(pygame.sprite.spritecollide(self,balls,0)) > 0:
                lives = lives - 1
                self = reset(BLACK)
            elif colwitsame:
                self.reset()
            elif self.rect.left   <= 0 and self.dir == 1:
                if self.rect.right  >= WINWIDTH:
                    self.rect      = self.rect.inflate(-ispeed,0)
                    distance       = WINWIDTH - self.rect.width
                    self.rect      = self.rect.inflate(distance,0)
                    self.rect.left = 0
                    FINISHED       = True                    
                elif colwitwall:
                    if len(colwal) ==1:
                        self.rect      = self.rect.inflate(-ispeed,0)
                        distance       = self.rect.left
                        distance       = distance + colwall[colwal[0]].rect.left - self.rect.right
                        self.rect      = self.rect.inflate(distance,0)
                        self.rect.left = 0
                        FINISHED       = True
                else:
                    self.rect      = self.rect.inflate(-ispeed,0)
                    distance       = self.rect.left
                    self.rect      = self.rect.inflate(int(ispeed/2)+distance,0)
                    self.rect.left = 0
                    
            elif self.rect.right  >= WINWIDTH and self.dir == 1:
                if self.rect.left  <= 0:
                    self.rect      = self.rect.inflate(-ispeed,0)
                    distance       = WINWIDTH - self.rect.right
                    self.rect      = self.rect.inflate(distance,0)
                    self.rect.left = 0
                    FINISHED       = True
                elif colwitwall:
                    if len(colwal) ==1:
                         self.rect      = self.rect.inflate(-ispeed,0)
                         distance       = WINWIDTH - self.rect.right
                         distance       = distance + self.rect.left - colwall[colwal[0]].rect.right
                         self.rect      = self.rect.inflate(distance,0)
                         self.rect.right= WINWIDTH
                         FINISHED       = True                    
                else:
                    self.rect       = self.rect.inflate(-ispeed,0)
                    distance        = WINWIDTH - self.rect.right
                    self.rect       = self.rect.inflate(int(ispeed/2)+distance,0)
                    self.rect.right = WINWIDTH
                    
            elif self.rect.top <= 0 and self.dir == 0:
                if self.rect.bottom > WINHEIGHT:
                    self.rect      = self.rect.inflate(0,-ispeed)
                    distance       = WINHEIGHT - self.rect.height
                    self.rect      = self.rect.inflate(0,distance)
                    self.rect.top  = 0
                    FINISHED       = True
                elif colwitwall:
                    if len(colwal) ==1:
                            self.rect      = self.rect.inflate(0,-ispeed)
                            distance       = self.rect.top
                            distance       = distance + colwall[colwal[0]].rect.top - self.rect.bottom
                            self.rect      = self.rect.inflate(0,distance)
                            self.rect.top = 0
                            FINISHED       = True   
                else:
                    self.rect      = self.rect.inflate(0,-ispeed)
                    distance       = self.rect.top
                    self.rect      = self.rect.inflate(0,int(ispeed/2)+distance)
                    self.rect.top  = 0
             
            elif self.rect.bottom > WINHEIGHT and self.dir == 0:
                if self.rect.top <= 0:
                    self.rect      = self.rect.inflate(0,-ispeed)
                    distance       = WINHEIGHT - self.rect.height
                    self.rect      = self.rect.inflate(0,distance)
                    self.rect.bottom  = WINHEIGHT
                    FINISHED       = True
                elif colwitwall:
                    if len(colwal) ==1:
                            self.rect      = self.rect.inflate(0,-ispeed)
                            distance       = WINHEIGHT - self.rect.bottom
                            distance       = distance + self.rect.top - colwall[colwal[0]].rect.bottom
                            self.rect      = self.rect.inflate(0,distance)
                            self.rect.bottom = WINHEIGHT
                            FINISHED       = True     
                else:
                    self.rect        = self.rect.inflate(0,-ispeed)
                    distance         = WINHEIGHT - self.rect.bottom
                    self.rect        = self.rect.inflate(0,int(ispeed/2)+distance)
                    self.rect.bottom = WINHEIGHT
            elif colwitwall:
                if len(colwal) == 1:
                    if self.dir == 1:
                        size = self.rect.width
                        self.rect  = self.rect.inflate(-ispeed,0)
                        size = self.rect.width
                        if self.rect.left < colwall[colwal[0]].rect.left:
                            distance = colwall[colwal[0]].rect.left - self.rect.right
                            left = self.rect.left
                            right= self.rect.right
                            top  = self.rect.top
                            bottom = self.rect.bottom
                            self.rect  =self.rect.inflate(int(ispeed/2)+distance,0)
                            size = self.rect.width
                            self.rect.right =  colwall[colwal[0]].rect.left
                            left = self.rect.left
                            right= self.rect.right
                            top  = self.rect.top
                            bottom = self.rect.bottom
                            size = self.rect.width
                        else:
                            distance  =self.rect.left - colwall[colwal[0]].rect.right
                            self.rect =self.rect.inflate(int(ispeed/2)+distance,0)
                            self.rect.left =  colwall[colwal[0]].rect.right
                    elif self.dir == 0:
                        self.rect  =  self.rect.inflate(0,-ispeed)
                        distance1  =  abs(self.rect.top - colwall[colwal[0]].rect.bottom)
                        distance2  =  abs(colwall[colwal[0]].rect.top- self.rect.bottom)
                        distance   = min(distance1,distance2)
                        self.rect  = self.rect.inflate(0,int(ispeed/2)+distance)
                        if distance == distance1:
                            self.rect.top =  colwall[colwal[0]].rect.bottom
                        else:
                            self.rect.bottom =  colwall[colwal[0]].rect.top
                elif len(colwal) == 2:
                    FINISHED = True
                    if self.dir == 1:
                        self.rect  =  self.rect.inflate(-ispeed,0)
                        distance1  = abs(self.rect.left - colwall[colwal[0]].rect.right)
                        distance2  = abs(colwall[colwal[0]].rect.left- self.rect.right)
                        distance   = min(distance1,distance2)
                        distance1  = abs(self.rect.left - colwall[colwal[1]].rect.right)
                        distance2  = abs(colwall[colwal[1]].rect.left- self.rect.right)
                        distance   = distance + min(distance1,distance2)
                        self.rect  = self.rect.inflate(distance,0)
                        if min(distance1,distance2) == distance1:
                            self.rect.left =  colwall[colwal[1]].rect.right
                        else:
                            self.rect.right =  colwall[colwal[1]].rect.left
                    elif self.dir == 0:
                        self.rect  =  self.rect.inflate(0,-ispeed)
                        distance1  =  abs(self.rect.top - colwall[colwal[0]].rect.bottom)
                        distance2  =  abs(colwall[colwal[0]].rect.top- self.rect.bottom)
                        distance   =  min(distance1,distance2)
                        distance1  =  abs(self.rect.top - colwall[colwal[1]].rect.bottom)
                        distance2  =  abs(colwall[colwal[1]].rect.top- self.rect.bottom)
                        distance   = distance + min(distance1,distance2)
                        self.rect  = self.rect.inflate(0,distance)
                        if min(distance1,distance2) == distance1:
                            self.rect.top =  colwall[colwal[1]].rect.bottom
                        else:
                            self.rect.bottom =  colwall[colwal[1]].rect.top
                            
            if self.dir == 1 and FINISHED:                                                        
                walls.append(wall(self.rect.left,self.rect.top,self.dir,self.rect.width))                    
                self.reset()
            elif self.dir == 0 and FINISHED:
                left = self.rect.left
                top = self.rect.top
                width = self.rect.bottom-self.rect.top
                width2 = self.rect.height
                walls.append(wall(self.rect.left,self.rect.top,self.dir,self.rect.height))                    
                self.reset()
            self.image = pygame.Surface(self.rect.size)
            pygame.Surface.fill(self.image ,(0,0,0))

        else:
            if android:
                mousex = pointx
                mousey = pointy
            else:
                (mousex,mousey) = pygame.mouse.get_pos()
            self.rect.left  = mousex
            self.rect.top   = mousey

        
    def turn(self):
        self.dir        = (self.dir +1) %2
        if self.dir == 1:
            pygame.Surface.fill(self.image ,(0,0,0))
            pygame.draw.line(self.image,RED,(0,sizeball),(sizeball*2,sizeball))
        else:
            pygame.Surface.fill(self.image ,(0,0,0))
            pygame.draw.line(self.image,RED,(sizeball,0),(sizeball,2*sizeball))
            
    def reset(self):
        #resets mouse to nromal size when mosue button is released
        (mousex,mousey) = pygame.mouse.get_pos()
        self.image      = pygame.Surface((sizeball*2,sizeball*2))
        self.rect       = self.image.get_rect()
        self.rect.left  = mousex
        self.rect.top   = mousey
        self.BUTTON     = False
        pygame.Surface.fill(self.image ,(0,0,0))
        if self.dir == 1:
            pygame.draw.line(self.image,RED,(0,sizeball),(sizeball*2,sizeball))
        else:
            pygame.draw.line(self.image,RED,(sizeball,0),(sizeball,2*sizeball))

class wall(pygame.sprite.Sprite):
    def __init__(self,X,Y,D,size):
        (mousex,mousey) = pygame.mouse.get_pos()
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.D = D
        if D == 1: #x-direction
            self.image      = pygame.Surface((abs(size),2*sizeball))
            self.rect       = self.image.get_rect()
            self.rect.left  = X
            self.rect.top   = Y

            cont = True
            #loop to inflate downwards the wall untile we hit another ball, other wall or the side.
            while cont:
                self.rect      = self.rect.inflate(0,2*sizeball)
                self.rect.top  = Y
                colwall        = pygame.sprite.spritecollide(self,walls,0)
                if len(pygame.sprite.spritecollide(self,balls,0)) > 0:
                    #ball below wall
                    cont            = False
                    self.image      = pygame.Surface((abs(size),2*sizeball))                    
                    self.rect       = self.image.get_rect()
                    self.rect.left  = X
                    self.rect.top   = Y
                    break
                elif self.rect.bottom > WINHEIGHT:
                    #growing of screen
                    self.rect      = self.rect.inflate(0,-2*sizeball)
                    self.rect.top  = Y
                    distance       = WINHEIGHT - self.rect.bottom
                    self.rect      = self.rect.inflate(0,distance)
                    self.rect.top  = Y
                    self.image     = pygame.Surface((abs(size),self.rect.height)) 
                    cont           = False
                elif len(colwall) > 0:
                    if self.D == colwall[0].D:
                        #hitting another wall deflating the wall one step
                        self.rect      = self.rect.inflate(0,-2*sizeball)
                        self.rect.top  = Y
                        distance       = colwall[0].rect.top - self.rect.bottom
                        self.rect      = self.rect.inflate(0,distance)
                        self.image     = pygame.Surface((abs(size),self.rect.height)) 
                        self.rect.top  = Y
                        cont           = False
                        break


            cont2 = True
            #loop to inflate upwards the wall untile we hit another ball, other wall or the side.
            while cont2:
                self.rect         = self.rect.inflate(0,2*sizeball)
                self.rect.bottom  = Y + 2*sizeball
                colwall           = pygame.sprite.spritecollide(self,walls,0)
                if len(pygame.sprite.spritecollide(self,balls,0)) > 0:
                    #ball above wall                
                    self.rect      = self.image.get_rect()
                    self.rect.left = X
                    self.rect.top  = Y
                    cont2          = False
                    break
                elif self.rect.top <= 0:
                    #growing of screen
                    self.rect        = self.rect.inflate(0,-2*sizeball)
                    self.rect.bottom = Y + 2*sizeball
                    distance         = self.rect.top
                    self.rect        = self.rect.inflate(0,distance)
                    self.rect.bottom = Y + 2*sizeball
                    self.image       = pygame.Surface((abs(size),self.rect.height))
                    cont2            = False
                elif len(colwall) > 0:
                    if self.D == colwall[0].D:
                    #hitting another wall deflating the wall one step
                        self.rect        = self.rect.inflate(0,-2*sizeball)
                        self.rect.bottom = Y + 2*sizeball
                        distance         = self.rect.top - colwall[0].rect.bottom 
                        self.rect        = self.rect.inflate(0,distance)
                        self.rect.bottom = Y + 2*sizeball
                        self.image       = pygame.Surface((abs(size),self.rect.height))
                        cont2            = False
                        break


        else: #other direction Y
            
            self.image      = pygame.Surface((2*sizeball,abs(size)))
            self.rect       = self.image.get_rect()
            self.rect.left  = X
            self.rect.top   = Y

            cont = True
            #loop to inflate right the wall untile we hit another ball, other wall or the side.
            while cont:
                self.rect      = self.rect.inflate(2*sizeball,0)
                self.rect.left = X
                colwall        = pygame.sprite.spritecollide(self,walls,0)
                right          = self.rect.right
                if len(pygame.sprite.spritecollide(self,balls,0)) > 0:
                    #ball below wall
                    cont            = False
                    self.image      = pygame.Surface((2*sizeball,abs(size)))                    
                    self.rect       = self.image.get_rect()
                    self.rect.left  = X
                    self.rect.top   = Y
                    break
                elif self.rect.right > WINWIDTH:
                    #growing of screen
                    self.rect      = self.rect.inflate(-2*sizeball,0)
                    self.rect.left = X
                    distance       = WINWIDTH - self.rect.right
                    self.rect      = self.rect.inflate(distance,0)
                    self.rect.left = X
                    self.image     = pygame.Surface((self.rect.width,abs(size))) 
                    cont           = False
                elif len(colwall) > 0:
                    dire = colwall[0].D
                    if self.D == colwall[0].D:
                    #hitting another wall deflating the wall one step
                        self.rect      = self.rect.inflate(-2*sizeball,0)
                        self.rect.left = X
                        distance       = colwall[0].rect.left - self.rect.right
                        self.rect      = self.rect.inflate(distance,0)
                        self.image     = pygame.Surface((self.rect.width,abs(size))) 
                        self.rect.left = X
                        cont           = False
                        break


            cont2 = True
            #loop to inflate left the wall untile we hit another ball, other wall or the side.
            while cont2:
                self.rect       = self.rect.inflate(2*sizeball,0)
                self.rect.right = X + 2 * sizeball
                colwall         = pygame.sprite.spritecollide(self,walls,0)
                if len(pygame.sprite.spritecollide(self,balls,0)) > 0:
                    #ball below wall
                    cont2            = False                   
                    self.rect       = self.image.get_rect()
                    self.rect.left  = X
                    self.rect.top   = Y
                    break

                elif self.rect.left < 0:
                    #growing of screen
                    self.rect       = self.rect.inflate(-2*sizeball,0)
                    self.rect.right = X + 2 * sizeball
                    distance        = self.rect.left
                    self.rect       = self.rect.inflate(distance,0)
                    self.rect.right = X + 2 * sizeball
                    self.image      = pygame.Surface((self.rect.width,abs(size))) 
                    cont2           = False
                elif len(colwall) > 0:
                    if self.D == colwall[0].D:
                    #hitting another wall deflating the wall one step
                        self.rect      = self.rect.inflate(-2*sizeball,0)
                        self.rect.right = X + 2 * sizeball
                        distance       = self.rect.left -  colwall[0].rect.right
                        self.rect      = self.rect.inflate(distance,0)
                        self.image     = pygame.Surface((self.rect.width,abs(size))) 
                        self.rect.right = X + 2 * sizeball
                        cont2           = False
                        break   
        KLEUR = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        pygame.Surface.fill(self.image ,KLEUR)
                    
            
            
class wall2(pygame.sprite.Sprite):
    def __init__(self,X,Y,D,size):
        (mousex,mousey) = pygame.mouse.get_pos()
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        if D == 1:
            #determining which two walls are the closest
            distancetop2    = Y
            distancebottom2 = WINHEIGHT - Y
            for wall in walls:
                if abs(wall.rect.left) - X < sizeball:
                    distancetop = Y - wall.rect.bottom
                    distancebottom = wall.rect.top - (Y + sizeball*2)
                
                    if distancetop < distancetop2 and distancetop > 0 and wall.rect.top < Y:
                        distancetop2 = distancetop
                        closesttop   = wall
                    if distancebottom < distancebottom2 and distancebottom > 0 and wall.rect.top > Y:
                        distancebottom2 = distancebottom
                        closestbottom   = wall

            #testing if there is a ball between wall and top wall
            self.image      = pygame.Surface((abs(size),sizeball*2+distancetop2))
            self.rect       = self.image.get_rect()
            self.rect.left  = X
            self.rect.top   = 0+Y-distancetop2
            self.D          = D
            ballontop       = len(pygame.sprite.spritecollide(self,balls,0)) > 0
            #testing if there is a ball between wall and bottom wall
            self.image      = pygame.Surface((abs(size),sizeball*2+distancebottom2))
            self.rect       = self.image.get_rect()
            self.rect.left  = X
            self.rect.top   = 0+Y
            self.D          = D
            ballonbottom    =  len(pygame.sprite.spritecollide(self,balls,0)) > 0
            if ballontop and ballonbottom:
                self.image      = pygame.Surface((abs(size),sizeball*2))
                self.rect       = self.image.get_rect()
                self.rect.left  = X
                self.rect.top   = Y
                self.D          = D              
            elif ballonbottom:
                self.image      = pygame.Surface((abs(size),sizeball*2+distancetop2))
                self.rect       = self.image.get_rect()
                self.rect.left  = X
                self.rect.top   = 0+Y-distancetop2
                self.D          = D    
                        

        else:
            
            distanceleft2    = X
            distanceright2 = WINWIDTH - X
            for wall in walls:
                if abs(wall.rect.top - Y) < sizeball:
                    distanceleft = X - wall.rect.right
                    distanceright = wall.rect.left - (X + sizeball*2)
                    if distanceleft < distanceleft2 and distanceleft > 0 and wall.rect.left < X:
                        distanceleft2 = distanceleft
                        closestleft   = wall
                    if distanceright < distanceright2 and distanceright > 0 and wall.rect.right > X:
                        distanceright2 = distanceright
                        closestright   = wall

            #testing if there is a ball betwoon wall and top wall
            self.image      = pygame.Surface((sizeball*2+distanceleft2,abs(size)))
            self.rect       = self.image.get_rect()
            self.rect.left  = X-distanceleft2
            self.rect.top   = 0+Y
            self.D          = D
            ballonleft  =  len(pygame.sprite.spritecollide(self,balls,0)) > 0
            #testing if there is a ball betwoon wall and bottom wall
            self.image      = pygame.Surface((sizeball*2+distanceright2,abs(size),))
            self.rect       = self.image.get_rect()
            self.rect.left  = X
            self.rect.top   = 0+Y
            self.D          = D
            ballonright     =  len(pygame.sprite.spritecollide(self,balls,0)) > 0
            if ballonleft and ballonright:
                self.image      = pygame.Surface((sizeball*2,abs(size)))
                self.rect       = self.image.get_rect()
                self.rect.left  = X
                self.rect.top   = Y
                self.D          = D              
            elif ballonright:
                self.image      = pygame.Surface((sizeball*2+distanceleft2,abs(size)))
                self.rect       = self.image.get_rect()
                self.rect.left  = X-distanceleft2
                self.rect.top   = 0+Y
                self.D          = D  
#error in not check which wall is the closest when there is a division of the screen
        KLEUR = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        pygame.Surface.fill(self.image ,KLEUR)

        
class Texting(pygame.sprite.Sprite):
    def __init__(self):
        self.image      = pygame.Surface((sizeball*4,sizeball*2))
        self.rect       = self.image.get_rect()
        self.rect.left  = 0
        self.rect.top   = 0
        #self.image = self.image.convert_alpha()        
        

        menuFont0bj = pygame.font.Font (None,30)    
        AQUA    = (  0, 255, 255)
        SILVER  = (192, 192, 192)
        message = '0%'
        text = menuFont0bj.render(message, True , AQUA,SILVER)
        textrect = text.get_rect()
        textrect.center=(self.rect.center)
        self.image.blit(text,self.rect) 
        
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer    
    def update(self):
        global walls,mouse, WINWIDTH, WINHEIGHT,NBALS,percentage
        area = 0.
        for wall in walls:
            area = area + wall.rect.width*wall.rect.height
        percentage  = int(area/(float(WINWIDTH*WINHEIGHT))*100)
        BLACK   = (  0,   0,   0,0)
        menuFont0bj = pygame.font.Font (None,30)    
        AQUA    = (  0, 255, 255)
        SILVER  = (192, 192, 192)
        value = str(int(area/(float(WINWIDTH*WINHEIGHT))*100))
        per = '%'
        message = value + per
        text = menuFont0bj.render(message, True , AQUA,SILVER)
        textrect = text.get_rect()
        textrect.center=(self.rect.center)
        pygame.Surface.fill(self.image ,SILVER)
        self.image.blit(text,self.rect) 
        
def main():
    global DISPLAYSURF, NBALS
    global WINHEIGHT, WINWIDTH, BGCOLOUR, balls, sizeball, RED, GREEN,walls, NBALS, allsprites, walls, text,pointx,pointy, lives

    AQUA    = (  0, 255, 255)
    BLACK   = (  0,   0,   0,0)
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
    BGCOLOUR = WHITE  
    WINWIDTH     = 600 # width of the program's window, in pixels
    WINHEIGHT    = 600 # height in pixels
    FPS          = 25  # number of frames per second
    NBALS        = 2
    lives        = 3
    pygame.init()
    sizeball     = 10
    mynative = pygame.display.list_modes() # Default
    s_res = (mynative[0][0],mynative[0][1])
    if android:
        android.init()
        android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)    
        WINWIDTH     = mynative[0][0] # width of the program's window, in pixels
        WINHEIGHT    = mynative[0][1] # height in pixels
        DISPLAYSURF  = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
        HEIGHTHUD    = int(WINHEIGHT/5)
        WINHEIGHT    = WINHEIGHT - HEIGHTHUD
        pointx       =  int(WINWIDTH/2)
        pointy       =   int(WINHEIGHT/2)
    else:
        WINWIDTH  = 640
        WINHEIGHT = 480
        DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
        HEIGHTHUD = int(WINHEIGHT/5)
        WINHEIGHT = WINHEIGHT - HEIGHTHUD
        pointx      =  int(WINWIDTH/2)
        pointy     =   int(WINHEIGHT/2)

    pygame.key.set_repeat(10)
    pygame.mouse.set_visible(False)
    # making a clock
    FPSCLOCK = pygame.time.Clock()
    #creating a Display surface and an alpha surface

    DISPLAYSURF.fill(BGCOLOUR)
    walls = []
    balls = []    
    allsprites = pygame.sprite.RenderPlain(balls,walls)
    mouse= reset(BLACK)
    allsprites.add(mouse)
    while True:        
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if(event.key == K_ESCAPE):
                     terminate()
            elif event.type == MOUSEBUTTONDOWN:
                if android:
                    (mousex,mousey) = pygame.mouse.get_pos()
                    if mousey > WINHEIGHT:                    
                        if mousex < WINWIDTH/2:
                           mouse.BUTTON = True
                           pygame.mouse.set_pos([pointx,pointy])
                        else:
                            mouse.turn()
                    else:
                        pointx = mousex
                        pointy = mousey
                else:
                    [m1,m2,m3] = pygame.mouse.get_pressed()
                    if m1:                    
                    #allsprites.remove(balls)
                    #balls.append( Ball(BLACK))
                    #allsprites.add(balls)
                        mouse.BUTTON = True
                    elif m3:
                        mouse.turn()
            elif event.type == MOUSEBUTTONUP:
                mouse.BUTTON = False
                mouse.reset()
        allsprites.remove(walls)
        allsprites.update()
        text.update()
        allsprites.add(walls)
        DISPLAYSURF.fill(BGCOLOUR)
        #if android:
        drawHUD(AQUA,SILVER,HEIGHTHUD)
        allsprites.draw(DISPLAYSURF)
        text.draw(DISPLAYSURF)
        plothealth(lives,RED)
        pygame.display.update()
        if percentage > 75:
            NBALS = NBALS+1
            allsprites.remove(mouse)
            mouse = reset(BLACK)
            allsprites.add(mouse)
        FPSCLOCK.tick(FPS)
        
def terminate():
    pygame.quit()
    sys.exit()

def reset(BLACK):
    global walls, balls, allsprites, text, lives, NBALS
    allsprites.remove(walls)
    allsprites.remove(balls)
    walls = []
    balls = []
    if lives < 0:
        nokeypressed = True
        while nokeypressed:
            SILVER  = (192, 192, 192)
            AQUA    = (  0, 255, 255)
            menuFont0bj = pygame.font.Font (None,50)    
            message = 'Press a button or key'
            text = menuFont0bj.render(message, True , SILVER,AQUA)
            textrect = text.get_rect()
            textrect.center = (int(WINWIDTH/2),int(WINHEIGHT/2))
            DISPLAYSURF.blit(text,textrect)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()
                elif event.type == KEYDOWN:
                    nokeypressed = False
                elif  event.type == MOUSEBUTTONDOWN:
                    nokeypressed = False
        NBALS = 2
        lives = 3
    else:
        nokeypressed = True
        while nokeypressed:
            SILVER  = (192, 192, 192)
            AQUA    = (  0, 255, 255)
            menuFont0bj = pygame.font.Font (None,40)    
            message = 'Press a button or key to start with '
            message = message +  str(NBALS) + ' balls'
            text = menuFont0bj.render(message, True , SILVER,AQUA)
            textrect = text.get_rect()
            textrect.center = (int(WINWIDTH/2),int(WINHEIGHT/2))
            DISPLAYSURF.blit(text,textrect)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()
                elif event.type == KEYDOWN:
                    nokeypressed = False
                elif  event.type == MOUSEBUTTONDOWN:
                    nokeypressed = False        
    for i in range(NBALS):
        #position of ball should not collide with other balls
        balls.append( Ball(BLACK))
    texting = Texting()
    text=pygame.sprite.RenderPlain(texting)
    mouse = Mouse()
    mouse.reset()
    allsprites.add(balls)
    return mouse

def drawHUD(AQUA,SILVER,HEIGHTHUD):
    pygame.draw.rect(DISPLAYSURF,AQUA,(0,WINHEIGHT,int(WINWIDTH/2),HEIGHTHUD))
    pygame.draw.rect(DISPLAYSURF,SILVER,(int(WINWIDTH/2),WINHEIGHT,WINWIDTH,HEIGHTHUD))
    menuFont0bj = pygame.font.Font (None,100)    
    message = 'DRAW'
    text = menuFont0bj.render(message, True , SILVER,AQUA)
    textrect = text.get_rect()
    textrect.center = (int(WINWIDTH/4),WINHEIGHT+int(HEIGHTHUD/2))
    DISPLAYSURF.blit(text,textrect)
    message = 'TURN'
    text = menuFont0bj.render(message, True , AQUA,SILVER)
    textrect = text.get_rect()
    textrect.center = (int(3*WINWIDTH/4),WINHEIGHT+int(HEIGHTHUD/2))
    DISPLAYSURF.blit(text,textrect)
    
def plothealth(lives,COLOUR):
    for i  in range(lives):
        pygame.draw.rect(DISPLAYSURF,COLOUR,(20+i*20,20,10,10))

if __name__ == '__main__':
    main()
