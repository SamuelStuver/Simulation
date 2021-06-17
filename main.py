from things import Dot, Color
import sys
import time
import random
import pygame
from pygame.math import Vector2


class Simulation:
    def __init__(self, name="", pixel_width=500, pixel_height=500, background_color=Color.black.value):
        pygame.init()
        self.name = name
        size = (pixel_width, pixel_height)
        self.background_color = background_color
        self.screen = pygame.display.set_mode(size)
        self.screen.fill(self.background_color)
        self.objects = []

    @property
    def screen_center(self):
        return Vector2(self.screen.get_width()/2., self.screen.get_height()/2.)

    @property
    def screen_width(self):
        return self.screen.get_width()

    @property
    def screen_height(self):
        return self.screen.get_height()

    def run(self):
        print(f"Running Simulation: {self.name}")
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

            for obj in self.objects:
                obj.draw(self)
                # obj.move_by([0.01, 0.01])
                obj.random_walk(max_distance=0.01)

            self.update(leave_trace=False)

    def add_object(self, object):
        self.objects.append(object)

    def update(self, leave_trace=False):
        pygame.display.flip()
        if not leave_trace:
            self.screen.fill(self.background_color)


if __name__ == "__main__":
    name = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
    sim = Simulation(name, pixel_width=1000, pixel_height=1000)
    for i in range(1000):
        sim.add_object(Dot(color=(random.uniform(50,255), random.uniform(50,255), random.uniform(50,255))))

    sim.run()



