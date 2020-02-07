import pyxel

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
    def __init__(self, cv, mass, coords):
       self.cv = cv
       self.mass = mass
       self.x = coords[0]
       self.y = coords[1]
       self.vel = 0
       self.angle = 90
       # self.ac_x = 0
       # self.ac_y = 0
       self.friction_ac = FRICTION_CONSTANT*self.mass*9.8

    def update(self):
        if pyxel.btn(pyxel.KEY_UP):
            self.vel_x +=  self.vel*

        self.x += self.vel_x
        self.y += self.vel_y

    def draw(self):
        pyxel.circ(self.x, self.y, 3, 7)

class App:
    def __init__(self):
        self.car = Car(60, (WIDTH/2, HEIGHT/2))

        pyxel.init(WIDTH, HEIGHT, caption='Gran Rutismo', fps=60)
        pyxel.run(self.update, self.draw)
    
    def update(self):
        self.car.update()

    def draw(self):
        pyxel.cls(0)
        self.car.draw()

App()