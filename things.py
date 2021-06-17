import random
import enum
import math
import numpy as np
from pygame import Vector2, draw

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


if __name__ == "__main__":
    dot = Dot(seed=10)
    print(dot)
