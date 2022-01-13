import pygame as pg
import numpy as np
import numpy
import math
import pygame
from numba import njit





@njit(fastmath=True)
def ray_casting(screen_array, player_pos, player_angle, player_height, player_pitch,
                     screen_width, screen_height, delta_angle, ray_distance, h_fov, scale_height):

    screen_array[:] = np.array([80, 136, 191])
    y_buffer = np.full(screen_width, screen_height)

    ray_angle = player_angle - h_fov
    for num_ray in range(screen_width):
        first_contact = False
        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)

        for depth in range(1, ray_distance):
            x = int(player_pos[0] + depth * cos_a)
            if 0 < x < map_width:
                y = int(player_pos[1] + depth * sin_a)
                if 0 < y < map_height:

                    # remove fish eye and get height on screen
                    depth *= math.cos(player_angle - ray_angle)
                    height_on_screen = int((player_height - height_map[x, y][0]) /
                                           depth * scale_height + player_pitch)

                    # remove unnecessary drawing
                    if not first_contact:
                        y_buffer[num_ray] = min(height_on_screen, screen_height)
                        first_contact = True

                    # remove mirror bug
                    if height_on_screen < 0:
                        height_on_screen = 0

                    # draw vert line
                    if height_on_screen < y_buffer[num_ray]:
                        for screen_y in range(height_on_screen, y_buffer[num_ray]):
                            screen_array[num_ray, screen_y] = color_map[x, y]
                        y_buffer[num_ray] = height_on_screen

        ray_angle += delta_angle
    return screen_array


class VoxelRender:
    def __init__(self, screen, width, height, player):
        #self.app = app
        self.screen = screen
        self.player = player
        self.width = width
        self.height = height
        self.fov = math.pi / 5
        self.h_fov = self.fov / 3
        self.num_rays = width
        self.delta_angle = self.fov / self.num_rays
        self.ray_distance = 4000
        self.scale_height = 900
        self.screen_array = np.full((width, height, 3), (0, 0, 0))

    def update(self):
        self.screen_array = ray_casting(self.screen_array, self.player.pos, self.player.angle,
                                        self.player.height, self.player.pitch, self.width,
                                        self.height, self.delta_angle, self.ray_distance,
                                        self.h_fov, self.scale_height)

    def draw(self):
        kompas = pygame.font.SysFont(None, 48)
        kompasname = kompas.render("N", True, (0, 0, 0))
        #self.screen.blit(kompasname, (800, 30))
        pg.surfarray.blit_array(self.screen, self.screen_array)


class Player:
    def __init__(self):
        self.pos = np.array([0, 0], dtype=float)
        self.angle = math.pi / 4
        self.height = 270
        self.pitch = 30
        self.angle_vel = 0.01
        self.vel = 1
        self.speedK = 2
        pygame.mouse.set_visible(False)

    def update(self):
        print(self.pos, self.pitch, self.angle)
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)

        self.pos[0] += self.vel * cos_a * self.speedK
        self.pos[1] += self.vel * sin_a * self.speedK
        self.height += self.vel * self.pitch / 200

        pressed_key = pg.key.get_pressed()
        if pressed_key[pg.K_UP]:
            self.speedK += 1
            if self.speedK > 10:
                self.speedK = 10
        if pressed_key[pg.K_DOWN]:
            self.speedK -= 1
            if self.speedK < 1:
                self.speedK = 1

        if pressed_key[pg.K_q]:
            self.angle -= self.angle_vel
        if pressed_key[pg.K_e]:
            self.angle += self.angle_vel
        
        if pressed_key[pg.K_w]:
            self.pitch -= self.vel
        if pressed_key[pg.K_s]:
            self.pitch += self.vel
        if pressed_key[pg.K_a]:
            self.angle -= self.angle_vel
        if pressed_key[pg.K_d]:
            self.angle += self.angle_vel


class App:
    def __init__(self):
        self.res = self.width, self.height = (800, 450)
        self.screen = pg.display.set_mode(self.res, pg.SCALED)
        self.clock = pg.time.Clock()
        self.player = Player()
        self.voxel_render = VoxelRender(self)

    def update(self):
        self.player.update()
        self.voxel_render.update()

    def draw(self):
        self.voxel_render.draw()
        pg.display.flip()

    def run(self):
        while True:
            self.update()
            self.draw()

            [exit() for i in pg.event.get() if i.type == pg.QUIT]
            self.clock.tick(60)
            pg.display.set_caption(f'FPS: {self.clock.get_fps()}')


if __name__ == '__main__':
    pygame.font.init()
    height_map = np.load(open("map/height", "rb"))
    color_map = np.load(open("map/map", "rb"))
    map_height = len(height_map[0])
    map_width = len(height_map)
    res = width, height = (800, 450)
    screen = pg.display.set_mode(res, pg.SCALED, pg.FULLSCREEN)
    clock = pg.time.Clock()
    player = Player()
    voxel_render = VoxelRender(screen, width, height, player)

    while True:
            player.update()
            voxel_render.update()
            
            voxel_render.draw()
            pg.display.flip()

            [exit() for i in pg.event.get() if i.type == pg.QUIT]
            clock.tick(60)
            pg.display.set_caption(f'FPS: {clock.get_fps()}')