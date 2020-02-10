import pyxel
import math

HEIGHT = 200
WIDTH = 250

class Sprite:
    def __init__(self, bank, start_coords, end_coords, col):
        self.start_coords = start_coords
        self.avanced = (
            end_coords[0] - self.start_coords[0],
            end_coords[1] - self.start_coords[1]
        )
        self.bank = bank
        self.col = col
    
    def draw(self, x, y):
        pyxel.blt(x, y, self.bank, self.start_coords[0], self.start_coords[1], self.avanced[0], self.avanced[1], colkey = self.col)

class Car:
    def __init__(self, coords):
       self.x = coords[0]
       self.y = coords[1]
       self.vel = 0
       self.fuel = 40
       self.waste_each_100 = 4.1
       self.angle = math.pi/2
       self.ac = 0
       self.sprites = {
            'UP':(
                Sprite(0, (106, 40), (118, 58), 0), 
                (6, 6)
            ), 
            'DOWN':(
               Sprite(0, (234, 39), (246, 59), 0),
               (6, 9)
            ),
            'RIGHT':(
                Sprite(0, (162, 42), (190, 56), 0),
                (12, 5)
            ), 
           'LEFT':(
               Sprite(0, (34, 42), (62, 55), 0) , 
               (12, 5)
            ),
            'UP_RIGHT':(
               Sprite(0, (130, 39), (157, 58), 0) , 
               (13, 6)
            ),
            'UP_LEFT':(
               Sprite(0, (67, 40), (93, 58), 0) , 
               (12, 5)
            ),
            'DOWN_RIGHT':(
               Sprite(0, (195, 39), (222, 58), 0) , 
               (12, 5)
            ),
            'DOWN_LEFT':(
               Sprite(0, (2, 39), (29, 58), 0) , 
               (14, 7)
            )
       }

    def update(self):
        if self.fuel < 0:
            self.fuel = 0

        if pyxel.btn(pyxel.KEY_UP) and self.fuel > 0:
            self.ac = (10/12000 * abs(210 - self.vel))
            self.fuel -= abs( 0.1*self.waste_each_100/100/(self.vel/10 if self.vel >= 10 else 1) )
        elif pyxel.btn(pyxel.KEY_DOWN):
            if int(self.vel) > 0:
                self.ac = -30/60
            elif self.fuel > 0:
                self.ac = -30/60
                self.fuel -= abs( 0.1*self.waste_each_100/100)
            else:
                self.ac = 0
        elif self.vel != 0:
            self.ac = 4/60 * (-1 if self.vel > 0 else 1)
        
        if not int( self.vel ) == 0:
            if pyxel.btn(pyxel.KEY_RIGHT):
                self.angle -= 0.5/self.vel if self.vel>15 else 0.08
            elif pyxel.btn(pyxel.KEY_LEFT):
                self.angle += 0.5/self.vel if self.vel>15 else 0.08

        self.angle %= 2*math.pi

        self.vel += self.ac

        print(int( self.vel ), self.fuel)

        if abs( self.vel ) < 0.01:
            self.vel = 0
        elif self.vel < -15:
            self.vel = -15

        self.x += 0.1* self.vel*math.cos(self.angle)
        self.y -= 0.1* self.vel*math.sin(self.angle)

    def draw(self):
        to_draw = None
        
        if (self.angle <= math.pi/8) or (self.angle >= math.pi*15/8):
            to_draw = 'RIGHT'
        elif (self.angle >= math.pi*13/8):
            to_draw = 'DOWN_RIGHT'
        elif (self.angle >= math.pi*11/8):
            to_draw = 'DOWN'
        elif (self.angle >= math.pi*9/8):
            to_draw = 'DOWN_LEFT'
        elif (self.angle >= math.pi*7/8):
            to_draw = 'LEFT'
        elif (self.angle >= math.pi*5/8):
            to_draw = 'UP_LEFT'
        elif (self.angle >= math.pi*3/8):
            to_draw = 'UP'
        else:
            to_draw = 'UP_RIGHT'

        self.sprites[to_draw][0].draw(self.x - self.sprites[to_draw][1][0], self.y- self.sprites[to_draw][1][1])
    
    def move_x(self, e):
        self.x += e
    
    def move_y(self, e):
        self.y += e

class CarHUD:
    def draw(self, car):
        VEL_POS = (40, 200)
        GAS_POS = (90, 200)

        pyxel.circ(GAS_POS[0], GAS_POS[1], 15, 0)
        pyxel.circb(GAS_POS[0], GAS_POS[1], 16, 7)

        angle_gas = -math.pi*7/8+(6/320*math.pi*car.fuel)
        pyxel.line(GAS_POS[0], GAS_POS[1], GAS_POS[0] + 8*math.cos(angle_gas), GAS_POS[1] + 8*math.sin(angle_gas), 9)
        pyxel.text(GAS_POS[0]+10, GAS_POS[1]-7, "F", 7)
        pyxel.text(GAS_POS[0]-12, GAS_POS[1]-7, "E", 7)

        if car.fuel <= 5 and car.fuel > 0:
            if int(pyxel.frame_count/10)%8 < 4:
                Sprite(1, (0, 0), (15, 15), 0).draw(GAS_POS[0]-8, GAS_POS[1]-17)
        elif car.fuel == 0:
            Sprite(1, (0, 0), (15, 15), 0).draw(GAS_POS[0]-8, GAS_POS[1]-17)

        pyxel.circ(VEL_POS[0], VEL_POS[1], 30, 0)
        pyxel.circb(VEL_POS[0], VEL_POS[1], 31, 7)
        if (car.vel >= 0) or ( abs(car.vel) < 1 ):
            pyxel.line(VEL_POS[0], VEL_POS[1], VEL_POS[0] + 25*math.cos(math.pi+0.1+(math.pi/200*car.vel)), VEL_POS[1] + 25*math.sin(math.pi+0.1+(math.pi/200*car.vel)), 8)
        else:
            pyxel.line(VEL_POS[0], VEL_POS[1], VEL_POS[0] + 25*math.cos(math.pi+0.1+abs(math.pi/200*car.vel)), VEL_POS[1] + 25*math.sin(math.pi+0.1+abs(math.pi/200*car.vel)), 8)
            pyxel.text(VEL_POS[0]+13, VEL_POS[1] - 23, "R", 8)

class BackGround:
    def __init__(self):
        self.horizontal = []
        self.vertical = []
        for i in range(1, int(HEIGHT/14)):
            self.vertical.append(
                [
                    [i*20,0],
                    [i*20,HEIGHT]

                ]
            )
        for i in range(1, int(HEIGHT/10)):
            self.horizontal.append(
                [
                    [0, i*20],
                    [WIDTH, i*20]
                ]
            )

    def draw(self):
        pyxel.cls(0)
        for i in self.vertical + self.horizontal:
            pyxel.line(
                i[0][0],
                i[0][1],
                i[1][0],
                i[1][1],
                5
            )
    
    def move_x(self, e):
        new = []
        for i in self.vertical:
            new.append(
                [
                [(i[0][0] + e)%WIDTH, i[0][1]],
                [(i[1][0] + e)%WIDTH, i[1][1]]
                ]
            )
        self.vertical = new
            
    
    def move_y(self, e):
        new = []
        for i in self.horizontal:
            new.append( 
                [
                [i[0][0], (i[0][1]+e)%HEIGHT],
                [i[1][0], (i[1][1]+e)%HEIGHT]
                ]
            )
        self.horizontal = new

class Camera:
    def __init__(self):
        self.vel_x = 0
        self.vel_y = 0

    def update(self, car, items):
        if (car.x != WIDTH/2):
            self.vel_x = (WIDTH/2 - car.x)*0.002*abs(int(car.vel))
        if (car.y != HEIGHT/2):
            self.vel_y = (HEIGHT/2 - car.y)*0.002*abs(int(car.vel))
        
        for i in [car] + items:
            i.move_x(self.vel_x) 
            i.move_y(self.vel_y)


class App:
    def __init__(self):
        self.car = Car((WIDTH/2, HEIGHT/2))
        self.floor = BackGround()
        self.camera = Camera()
        self.hud = CarHUD()

        pyxel.init(WIDTH, HEIGHT, caption='Gran Rutismo', fps=60)
        pyxel.load("./my_resource.pyxres")
        pyxel.run(self.update, self.draw)
    
    def update(self):
        self.car.update()
        self.camera.update(self.car, [self.floor])

    def draw(self):
        self.floor.draw()
        self.car.draw()
        self.hud.draw(self.car)

App()