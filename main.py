import pyxel
import math

HEIGHT = 200
WIDTH = 250

# HIELO --> 0.1
# ASFALTO --> 0.8
FRICTION_CONSTANT = 0.8

# CV
# 1300 --> superdeportivo
# 60-100 --> seat ibiza

# Aceleración
# 1940 cv --> 0 a 100 en 1.85 s

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
        if pyxel.btn(pyxel.KEY_UP):
            self.ac = 5/60
        elif pyxel.btn(pyxel.KEY_DOWN):
            self.ac = -6/60
        else:
            if self.vel != 0:
                self.ac = 3/60 * (-1 if self.vel > 0 else 1)
        
        if not int( self.vel ) == 0:
            if pyxel.btn(pyxel.KEY_RIGHT):
                self.angle -= 0.5/self.vel if self.vel>15 else 0.08
            elif pyxel.btn(pyxel.KEY_LEFT):
                self.angle += 0.5/self.vel if self.vel>15 else 0.08

        self.angle %= 2*math.pi

        print(self.vel)

        self.vel += self.ac

        if abs( self.vel ) < 0.01:
            self.vel = 0
        elif self.vel < -10:
            self.vel = -10

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
        x += e
    
    def move_y(self, e):
        y += e

class BackGround:
    def __init__(self):
        self.a = []
        for i in range(1, int(HEIGHT/10)):
            self.a.append(
                (
                    (i*20,0),
                    (i*20,HEIGHT)
                )
            )
        for i in range(1, int(HEIGHT/10)):
            self.a.append(
                (
                    (0, i*20),
                    (WIDTH, i*20)
                )
            )

    def draw(self):
        pyxel.cls(0)
        for i in self.a:
            pyxel.line(
                i[0][0],
                i[0][1],
                i[1][0],
                i[1][1],
                5
            )
    
    def move_x(self, e):
        for i in self.a:
            i[0] += e
            i[0] %= WIDTH
    
    def move_y(self, e):
        for i in self.a:
            i[1] += e
            i[1] %= HEIGHT

class Camera:
    def __init__(self):
        self.ac_x = 0
        self.ac_y = 0

    def update(self, car, *items):
        if (car.x != WIDTH/2):
            self.ac_x = (WIDTH/2 - car.x)(0.6*0.6)
        if (car.y != HEIGHT/2):
            self.ac_y = (WIDTH/2 - car.y)(0.6*0.6)
        
        for i in [car] + items:


class App:
    def __init__(self):
        self.car = Car((WIDTH/2, HEIGHT/2))
        self.floor = BackGround()

        pyxel.init(WIDTH, HEIGHT, caption='Gran Rutismo', fps=60)
        pyxel.load("./my_resource.pyxres")
        pyxel.run(self.update, self.draw)
    
    def update(self):
        self.car.update()

    def draw(self):
        self.floor.draw()
        self.car.draw()

App()