import pygame as py 
from main import * 

circles = []
circles.append( Circle(250,250,100))
circles.append( Circle(400,150,50))
  
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0,255, 0)
  
# initialize pygame
py.init()
screen_size = (700, 500)
  
# create a window
screen = py.display.set_mode(screen_size)
screen_rect = screen.get_rect()
py.display.set_caption("pygame Test")
  
# clock is used to set a max fps
clock = py.time.Clock()
  
# create a demo surface, and draw a red line diagonally across it
#surface_size = (25, 45)
#test_surface = py.Surface([25,45])
#test_surface_rect = test_surface.get_rect(center=screen_rect.center)
#test_surface.fill(WHITE)
point_a = [50, 50]
  
running = True
while running:
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
    keys = py.key.get_pressed()

    if keys[py.K_w]:
        for circle in circles:
            circle.move(0,-3)
    if keys[py.K_s]:
        for circle in circles:
            circle.move(0,3)
    if keys[py.K_a]:
        for circle in circles:
            circle.move(-3,0)
    if keys[py.K_d]:
        for circle in circles:
            circle.move(3,0)
    if keys[py.K_UP]:
        point_a[1] -=3
    if keys[py.K_DOWN]:
        point_a[1] +=3
    if keys[py.K_LEFT]:
        point_a[0] -=3
    if keys[py.K_RIGHT]:
        point_a[0] +=3


    con_slopes = calc_connection_slopes(circles, [[0,1]])
    #print("conslopes:"+ str(con_slopes))

    point_b = find_con_minma(point_a,con_slopes[0],circles[0],circles[1])

    boarders = []
    for circle in circles:
        boarders.append(make_boarder(circle))
    #clear the screen
    screen.fill(WHITE)

    # draw our screen here
    for boarder in boarders:
        prev = None 
        for point in boarder:
            if prev == None:
                prev = point
                continue
            py.draw.aaline(screen,BLACK,prev,point)
            prev = point
        # draw the connection between first and last 
        py.draw.aaline(screen,BLACK,boarder[-1],boarder[0]) 

    py.draw.aaline(screen, BLACK,circles[0].get_cords(),circles[1].get_cords())

    py.draw.circle(screen,GREEN,point_a,1)
    py.draw.circle(screen,GREEN,point_b,1)

    py.draw.circle(screen,RED,circles[0].get_cords(),1)
    py.draw.circle(screen,RED,circles[1].get_cords(),1)
    # flip() updates the screen to make our changes visible
    py.display.flip()
      
    # how many updates per second
    clock.tick(60)
  
py.quit()

