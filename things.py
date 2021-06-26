import random
import enum
import math
import numpy as np
import time
from pygame import Vector2, Rect, draw

class Color(enum.Enum):
    white = (255, 255, 255)
    black = (0, 0, 0)


class Dot:
    def __init__(self, mass=0, position=Vector2(0, 0), radius=1, color=Color.white.value, randomize=False, seed=None):
        if randomize:
            if seed:
                self.randomize(seed=seed)
            else:
                self.randomize()
        else:
            self.mass = mass
            self.position = position
            self.radius = radius
            self.color = color

    @property
    def x(self):
        return self.position[0]

    @property
    def y(self):
        return self.position[1]

    def randomize(self, seed=None):
        random.seed(seed)
        self.mass = random.random()
        self.position = Vector2([random.uniform(-1, 1), random.uniform(-1, 1)])
        self.radius = random.uniform(0,5)
        self.color = (random.uniform(50,255), random.uniform(50,255), random.uniform(50,255))

    def move_by(self, offset_vector):
        new_position = self.position + offset_vector
        self.position = new_position

    def move_to(self, new_position):
        self.position = Vector2(new_position)

    def change_mass_by(self, amount):
        self.mass += amount

    def change_mass_to(self, new_mass):
        self.mass = new_mass

    def draw(self, simulation):
        pixel_position = simulation.screen_center
        pixel_position[0] += (self.position[0]*simulation.screen_width/2.)
        pixel_position[1] -= (self.position[1]*simulation.screen_height/2.)

        draw.circle(simulation.screen, self.color, pixel_position, self.radius)

    def random_walk(self, max_distance=1):
        """
        1. Create a random vector
        2. Normalize the vector
        3. Scale the vector to a random length up to the max length
        """
        offset = Vector2(random.uniform(-1,1), random.uniform(-1,1))
        offset.normalize()
        offset.scale_to_length(random.uniform(0, max_distance))

        self.move_by(offset)
        return offset

    def __str__(self):
        outstring = f"Mass: {self.mass:0.2f}\nPosition: [{self.x:0.2f},{self.y:0.2f}]"
        return outstring


class LifeMatrix:
    def __init__(self, x_size, y_size, pixel_ratio=1):
        self.x_size = x_size
        self.y_size = y_size
        self.pixel_ratio = pixel_ratio
        self.matrix = np.zeros((x_size, y_size))

    def initialize(self):
        self.initialize_lines()

    def initialize_random(self):
        for x in range(self.x_size):
            for y in range(self.y_size):
                self.matrix[x,y] = random.randint(0, 1)

        print(self)

    def initialize_lines(self):
        x_range = [int(self.x_size/4), 3*int(self.x_size/4)]
        y_range = [int(self.y_size/4), 3*int(self.y_size/4)]
        for x in range(x_range[0], x_range[1], 1):
            for y in range(y_range[0], y_range[1], 1):
                self.matrix[x,y] = random.randint(0, 1)

        print(self)

    def draw_to_screen(self, simulation):

        for x in range(self.x_size):
            for y in range(self.y_size):
                if self.matrix[x, y] == 1:
                    pos = [x*self.pixel_ratio, y*self.pixel_ratio]
                    rect = Rect(pos[0], pos[1], self.pixel_ratio, self.pixel_ratio)

                    simulation.screen.fill(Color.white.value, rect=rect)

    def check_neighbors(self, x_0, y_0):
        neighbors = [
            (x_0-1, y_0+1), (x_0, y_0+1), (x_0+1, y_0+1),
            (x_0-1, y_0), (x_0+1, y_0+1),
            (x_0-1, y_0-1), (x_0, y_0-1), (x_0+1, y_0-1),
        ]
        n_live = 0
        for n in neighbors:
            if self.matrix[n[0] % self.x_size, n[1] % self.y_size] == 1:
                n_live += 1
        return n_live

    def is_alive(self, x, y):
        return self.matrix[x, y]

    def flip(self, x, y):
        if self.matrix[x, y]:
            self.matrix[x, y] = 0
        else:
            self.matrix[x, y] = 1

    def mutate(self, x, y, p=0.01):
        random_val = random.uniform(0, 1)
        if self.is_alive(x, y):
            if random_val < p:
                self.flip(x, y)  # Dead
                print(f"MUTATION: {x, y}")
                return True
            else:

                return False

    def step(self, delay=None):
        if delay:
            time.sleep(delay)
        for x in range(self.x_size):
            for y in range(self.y_size):
                live_neighbors = self.check_neighbors(x, y)

                # Random flip with probability
                self.mutate(x, y, p=0.005)

                if self.is_alive(x, y):
                    if live_neighbors in [2, 3]:  # if 2 or 3 Live neighbors -> Alive
                        self.matrix[x, y] = 1
                    else:
                        self.matrix[x, y] = 0  # Dead

                else:
                    if live_neighbors == 3:  # if == 3 Live neighbors -> Alive
                        self.matrix[x, y] = 1

    def __str__(self):
        return str(self.matrix)


if __name__ == "__main__":
    dot = Dot(seed=10)
    print(dot)
