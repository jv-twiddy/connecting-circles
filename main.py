# imports 
import pygame as py
import math as m 

# doing math:

# have 2 circles A and B 
class Circle:
    def __init__(self,x:float,y:float,r:float):
        self.x = x
        self.y = y
        self.r = r
    
    def get_cords(self):
        return [self.x, self.y]
    
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y

    def get_r(self):
        return self.r 
    
    def scale(self, s:float):
        # self.x = self.x*s
        # self.y = self.y*s
        self.r = self.r*s
    
    def move(self, x,y):
        self.x +=x
        self.y +=y


#circles.append( Circle(100,70,30))

# make arrays of borders for them to draw
def make_boarder(circle:Circle, divisions: int = 100):
    # get 100 points from around the circle
    points = [] # holds the points to draw 
    center = circle.get_cords()
    r = circle.get_r()
    cx = center[0]
    cy = center[1]
    for x in range(divisions):
        angle = (x/divisions)*m.pi*2
        # each point will be some trig off of the center 
        point = [cx+r*m.cos(angle),cy+r*m.sin(angle)]
        points.append(point)
    return points

def calc_connection_slopes(circles,connections,minma_coef = 1):
    grad_connections =[] # array of array of [index of circle , index of circle 2, gradient c1->c2, minima]
    for connection in connections:
        # calculate gradient 
        c1 = circles[connection[0]]
        c2 = circles[connection[1]]
        #           dy              /       dx
        dy =c2.get_y()-c1.get_y()
        dx = c2.get_x()-c1.get_y()
        if dx == 0:
            grad = None
        else:
            grad = dy/dx

        # calculate minma, the minimum distance from the line 
        if c1.get_r() > c2.get_r():
            lowest_r = c2.get_r()
        else:
            lowest_r = c1.get_r()
        # calc distance 
        distance = m.sqrt(dy*dy+dx*dx)
        # calc minma 
        if distance !=0:
            minma = lowest_r / 1.2
        else:
            minma = lowest_r 

        grad_connections.append([connection[0],connection[1],grad,minma])
    return grad_connections

# finds the point that the perpendicular that passes through the point 
# would pass through the connection 
def find_con_minma(point, c1, c2):
    # we need to find the intersect of the two lines 
    # so y1 = a1*x1 +b1 , y2 = a2*x2 +b2
    # where equation 1 is for the connection 
    # and equation 2 is for the perpendicular going through the point 
    # a2*x +b2 = a1*x +b1
    # so x = (b1-b2)/(a2-a1)
    grad = points_to_grad(c1.get_cords(),c2.get_cords()) # a1
    if grad == None: # vertical line 
        con_x = c1.get_x()
    elif grad == 0: # horizontal line 
        con_x = point[0]
    else: # non weird line 
        offset = c1.get_y() - c1.get_x()*grad # b1
        inv_grad = -1/ grad # a2 
        inv_offset = point[1] - point[0]*inv_grad # b2
        con_x = (offset- inv_offset)/(inv_grad - grad) # x 

    # if this is true then the intersect lies past the bounds of the connection 
    # we will return the closest point 
    if (con_x>c1.get_x() and con_x>c2.get_x()):
        if (c1.get_x()>c2.get_x()):
            return c1.get_cords()
        else: 
            return c2.get_cords()
    elif (con_x<c1.get_x() and con_x<c2.get_x()):
        if (c1.get_x()<c2.get_x()):
            return c1.get_cords()
        else: 
            return c2.get_cords()
    
    # now we know that the closest point lies between the two centers
    if grad == None: # vertical 
        return [con_x,point[1]]
    elif grad == 0: #horizontal
        return [con_x,c1.get_y()]
    else: 
        return [ con_x, con_x*inv_grad+inv_offset]
    
def get_inverse(grad):
    if grad == None:
        return 0
    elif grad == 0:
        return None
    else:
        return -1/grad
    
def points_to_grad(a, b):
    dy = b[1]-a[1]
    dx = b[0] -a[0]
    if dx == 0:
        return None
    else:
        return dy/dx

def get_distance(a,b):
    dy = b[1]-a[1]
    dx = b[0] -a[0]
    return m.sqrt(dy*dy+dx*dx)

def get_sign(num):
    if num == 0:
        return 1
    if num > 0:
        return 1
    return -1

def are_close(a,b, epsilon=0.001):
    # make a upper and lower a
    a_upper = [ a[0]+epsilon, a[1]+epsilon]
    a_lower = [a[0]-epsilon, a[1]-epsilon]
    if (b[0]>a_lower[0] and b[0]<a_upper[0]) and (b[1]>a_lower[1] and b[1]<a_upper[1]):
        return True
    return False

def find_closest(circles, connections, current, step):
    # [position[x,y], minimum distance, current distance, is circle]
    table = []
    for circle in circles:
        distance = get_distance(current,circle.get_cords())
        table.append([circle.get_cords(),circle.get_r(),distance, True])
    # find which we should reference from  
    for connection in connections:
        minma = find_con_minma(current,circles[connection[0]],circles[connection[1]])
        distance = get_distance(current,minma) 
        table.append([minma,connection[3],distance,False])
    
    closest = 0
    inside = False
    lowest = table[0][2]
    for y in range(len(table)):
        # if we are in just about the radius of a circle we should use that
        if (table[y][2] <= table[y][1] and table[y][3]): # we will probably want an OR here to make it get off the circle 
            lowest = table[y][2]
            closest = y
            inside = True
        elif table[y][2] < lowest and not inside: # 
            lowest = table[y][2]
            closest = y
    return table, closest

def connected_boarder(circles,connections,divisions:int =1000):
    boarder = []
    perimeter = 0
    for circle in circles:
        perimeter += circle.get_r()*m.pi 
    for connection in connections:
        perimeter += get_distance(circles[connection[0]].get_cords(), circles[connection[1]].get_cords()) * 2 

    step = perimeter/(divisions*0.6) ### special value may need yo be adjusted 
    prev_dir = [1,1]

    # get our circles
    c1 = circles[connections[0][0]]
    # start at some point 
    # start = [c1.get_x()-c1.get_r()/m.sqrt(2),c1.get_y()-c1.get_r()/m.sqrt(2)]
    start = [c1.get_x()-c1.get_r(),c1.get_y()]
    current = start
    # make a table of possible comparisons 
    finished = False
    x = 0
    while not finished:
        # tabel entry: [position[x,y], minimum distance, current distance, is circle]
        table, closest = find_closest(circles,connections,current,step)  

        # now with the closest we find the gradient and put it at the correct distance from it 
        # OR 
        # we find the tangent and move in that direction? 
        gradi = points_to_grad(current, table[closest][0])
        new_direction = get_inverse(gradi)
        if new_direction == None:
            angle = m.pi / 2
        else:
            angle = m.atan(new_direction)
        # we now find the two possible directions and move towards the one with the highest dot product with the previous 

        right_vect = [step*m.cos(angle),step*m.sin(angle)]
        left_vect = [-step*m.cos(angle),-step*m.sin(angle)]
        
        right_dot_prod = prev_dir[0]*right_vect[0]+prev_dir[1]*right_vect[1]
        left_dot_prod = prev_dir[0]*left_vect[0]+prev_dir[1]*left_vect[1]
        
        if right_dot_prod>left_dot_prod:
            mynext = [ current[0]+right_vect[0],current[1]+right_vect[1]]
            prev_dir = [right_vect[0],right_vect[1]]
        else: 
            mynext = [ current[0]+left_vect[0],current[1]+left_vect[1]]
            prev_dir = [left_vect[0],left_vect[1]]
                
        # find the differenece from the nearest and move it in that direction 
        distance = get_distance(mynext, table[closest][0])
        # ratio of how far it shoud be 
        if distance == 0:
            ratio_d = 1
        else:
            ratio_d = table[closest][1]/distance    
        # get the vector for the difference between 
        diff_closest = [mynext[0]-table[closest][0][0], mynext[1]-table[closest][0][1]]
        # the location of where it should be
        location = [table[closest][0][0]+diff_closest[0]*ratio_d,table[closest][0][1]+diff_closest[1]*ratio_d]
        # 
        midway = [location[0]*0.2+mynext[0]*0.8,location[1]*0.2+mynext[1]*0.8]
        
        #should_be = [change[0]*ratio_d,change[1]*ratio_d]
        
        boarder.append([current[0],current[1]])
        current = [midway[0],midway[1]]

        # upper limit:
        x+=1 
        if x == divisions*2:
            break
        if x>100 and are_close(current,boarder[0],step*2):
            break
    # for the connection we need to find the point at which we would be through the parrallel 
    #print(boarder)
    print("end")
    return boarder



# boarders = []
# boarders.append(make_boarder(circles[0]))
# boarders.append(make_boarder(circles[1]))

# do some pygame 
  
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
point_a = [50, 50] # debug guy 

circles = []
circles.append( Circle(50,50,20))
circles.append( Circle(80,30,10))

con_slopes = calc_connection_slopes(circles, [[0,1]])
circlei = 0

running = True
while running:
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
        if event.type == py.KEYDOWN: # CHANGING CIRCLE 
            if event.key == py.K_q:
                circlei +=1
                if circlei == len(circles):
                    circlei = 0
            if event.key == py.K_a: # add another circle
                s_circle = circles[circlei] 
                circles.append(Circle(s_circle.get_x(),s_circle.get_y(),s_circle.get_r()))
                con_slopes.append([circlei,len(circles)-1])
                circlei = len(circles)-1

    keys = py.key.get_pressed()
                    # scaling 
    if keys[py.K_w]:
        circles[circlei].scale(1.1)
    if keys[py.K_s]:
        circles[circlei].scale(1/1.1)
                    # movement
    if keys[py.K_UP]:
        circles[circlei].move(0,-3)
    if keys[py.K_DOWN]:
        circles[circlei].move(0,3)
    if keys[py.K_LEFT]:
        circles[circlei].move(-3,0)
    if keys[py.K_RIGHT]:
        circles[circlei].move(3,0)
                    
        

    print(circlei)
    con_slopes = calc_connection_slopes(circles, con_slopes)
    #print("conslopes:"+ str(con_slopes))

    point_b = find_con_minma(point_a,circles[0],circles[1])
        
    boarders = []
    for circle in circles:
        boarders.append(make_boarder(circle))
    con_slopes = calc_connection_slopes(circles, con_slopes)
    boarders.append(connected_boarder(circles, con_slopes))

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

    for x in range(len(circles)):
        if x == circlei:
            py.draw.circle(screen,RED,circles[x].get_cords(),4)
        else:    
            py.draw.circle(screen,GREEN,circles[x].get_cords(),4)
    
    # flip() updates the screen to make our changes visible
    py.display.flip()
      
    # how many updates per second
    clock.tick(60)
  
py.quit()

