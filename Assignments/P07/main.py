from quadTree import *
import pygame
from random import randint 

import os
  
# Get the size
# of the terminal
size = os.get_terminal_size()

#Determines the size of the screen
x,y = size
x *= 12
y *= 20
size = (x,y)
print("Size of Screen:",x,y)


pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption('QuadTree')
radius = 3

def genPoints(bbox, x):
    points  = []
    for p in range(x):
        x = randint(radius,bbox.w-radius)
        y = randint(radius,bbox.h-radius)
        points.append((x,y))
    return points

def highlightPoints(foundPoints):
        pygame.draw.circle(screen,(255,255,255),foundPoints,radius+3)

#Initializes the moving rectangle
Rectangle = pygame.Rect(0, 0, 100, 100)
if __name__=='__main__':

    print((size[0]//2,size[1]//2,size[0],size[1]))

    bbox = Rect(size[0]//2,size[1]//2,size[0],size[1])
    
    qt = QuadTree(bbox)

    #Generates points in BBOX
    points = genPoints(bbox,1000)

    # nw = (size[0]//4,size[1]//4,size[0]//2,size[1]//2)


    # for p in points:
    #     qt.insert(p);
      

    # foundPoints = []
    # qt.query(Rect(size[0]//4,size[1]//4,size[0]//2,size[1]//2),foundPoints)
    # print(foundPoints)

        
    # creating a bool value which checks
    # if game is running
    running = True
    
    # Game loop
    # keep game running till running is true
    while running:

      #Fills the screen with Maroon color
        screen.fill((128,0,0))
        
        # Check for event if user has pushed
        # any event in queue
        for event in pygame.event.get():
        
            # if event is of type quit then set
            # running bool to false
            if event.type == pygame.QUIT:
                running = False

      #Creates the rectangle 
        pygame.draw.rect(screen,(0,0,0),Rectangle,3)
        for p in points:
          #If point in rectangle highlight
          if Rectangle.collidepoint(p):
            highlightPoints(p)
            print(p)
          else:
            pygame.draw.circle(screen,(255,215,0),p,radius+3)

        #Moves rectangle to the right in row wise fashion
        Rectangle.move_ip(6,0)
      
        if Rectangle.right > x:
            Rectangle.move_ip(-x,100)
          
        if Rectangle.bottom > y:
            Rectangle.move_ip(-x,-y)
          
        pygame.time.delay(40)

        pygame.display.flip()