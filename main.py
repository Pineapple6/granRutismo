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

class Car:
    def __init__(self, coords):
       self.x = coords[0]
       self.y = coords[1]
       self.vel = 0
       self.angle = math.pi/2
       self.ac = 0

    def update(self):
        if pyxel.btn(pyxel.KEY_UP):
            self.ac = 5/60
        elif pyxel.btn(pyxel.KEY_DOWN):
            self.ac = -5/60
        else:
            self.ac += 1/60 * (-1 if self.vel > 0 else 1)
        
        if not int( self.vel ) == 0:
            if pyxel.btn(pyxel.KEY_RIGHT):
                self.angle -= 0.3/self.vel
            elif pyxel.btn(pyxel.KEY_LEFT):
                self.angle += 0.3/self.vel
        
        if abs( self.vel ) < 0.01:
            self.vel = 0

        self.vel += self.ac
        print(self.vel)
        self.x += 0.1*self.vel*math.cos(self.angle)
        self.y -= 0.1*self.vel*math.sin(self.angle)

    def draw(self):
        pyxel.circ(self.x, self.y, 3, 7)

class App:
    def __init__(self):
        self.car = Car((WIDTH/2, HEIGHT/2))

        pyxel.init(WIDTH, HEIGHT, caption='Gran Rutismo', fps=60)
        pyxel.run(self.update, self.draw)
    
    def update(self):
        self.car.update()

    def draw(self):
        pyxel.cls(0)
        self.car.draw()

App()