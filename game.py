import pygame
import config as con
from object import *
from random import randint


class Game:
    def __init__(self, caption, width, height, back_image_filename, frame_rate):
        self.background_image = pygame.image.load(back_image_filename)
        self.frame_rate = frame_rate
        self.game_over = False
        self.objects = []
        pygame.init()
        pygame.font.init()
        self.surface = pygame.display.set_mode((width, height))
        pygame.display.set_caption(caption)
        self.clock = pygame.time.Clock()
        self.keydown_handlers = defaultdict(list)
        self.keyup_handlers = defaultdict(list)

    def update(self):
        for o in self.objects:
            o.update()

    def draw(self):
        for o in self.objects:
            o.draw(self.surface)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                for handler in self.keydown_handlers[event.key]:
                    handler(event.key)
            elif event.type == pygame.KEYUP:
                for handler in self.keyup_handlers[event.key]:
                    handler(event.key)

    def run(self):
        while not self.game_over:
            self.surface.blit(self.background_image, (0, 0))

            self.handle_events()
            self.update()
            self.draw()

            pygame.display.update()
            self.clock.tick(self.frame_rate)


class Dots(Game):
    def __init__(self):
        Game.__init__(self, "Physics", 600, 600, con.FULL_PATH, 60)
        self.create_objects()

    def create_objects(self):
        for _ in range(3):
            self.create_circle(randint(100, 400), randint(50, 450), [randint(0, 255), randint(0, 255), randint(0, 255)], randint(1, 10), randint(1, 10))

    def create_circle(self, x, y, color, speed_x, speed_y):
        circle = Circle(x, y, color, speed_x, speed_y)
        self.objects.append(circle)

    def update(self):
        def crushing(object_1, object_2):
            vector_first_x = object_2.center[0] - object_1.center[0]
            vector_first_y = object_2.center[1] - object_1.center[0]
            vector_second_x = object_1.center[0] - object_2.center[0]
            vector_second_y = object_1.center[1] - object_2.center[1]

            average_x = (abs(object_1.speed[0]) + abs(object_2.speed[0])) / 2
            average_y = (abs(object_1.speed[1]) + abs(object_1.speed[1])) / 2

            if vector_first_x != 0:
                object_1.speed[0] = -vector_first_x / abs(vector_first_x) * abs(average_x)

            if vector_second_x != 0:
                object_2.speed[0] = -vector_second_x / abs(vector_second_x) * abs(average_x)

            if vector_first_y != 0:
                object_1.speed[1] = -vector_first_y / abs(vector_first_y) * abs(average_y)

            if vector_second_y != 0:
                object_2.speed[1] = -vector_second_y / abs(vector_second_y) * abs(average_y)

        def intersection(self, object_1, object_2):
            if ((object_1.center[0] - object_2.center[0]) ** 2 + (object_1.center[1] - object_2.center[1]) ** 2) <= (con.RADIUS * 2 + 1) ** 2:
                return True
            return False

        def handle_collision(self):
            for object_1 in self.objects:
                for object_2 in self.objects:
                    if intersection(self, object_1, object_2) and object_1 != object_2:
                        crushing(object_1, object_2)

        for object in self.objects:
            if object.center[0] > con.SCREEN_WIDTH:
                object.speed[0] = -object.speed[0]

            if object.center[1] > con.SCREEN_HEIGHT:
                object.speed[1] = -object.speed[1]

            if object.center[0] < 0:
                object.speed[0] = -object.speed[0]

            if object.center[1] < 0:
                object.speed[1] = -object.speed[1]

        handle_collision(self)
        super().update()
