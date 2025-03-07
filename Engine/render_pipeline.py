# repo: https://github.com/ADRIKPANJA/py-3d
# render_pipeline.py

'''The rendering pipeline required for rendering, DO NOT MODIFY.'''

import pygame as pg
import numpy as np
import sys
import matrix
import time

class Renderer():
    '''The rendering pipeline.'''
    def __init__(self):
        super().__init__()
        self.screen = self.init(800, 600)
        self.pt = time.time()
        self.rotation = 0
        self.clock = pg.time.Clock()
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)
        self.dt = 1/240
        self.yaw = 0
        self.pitch = 0
        self.camX = 0
        self.camY = 0
        self.camZ = -100
        self.camXvel = 0
        self.camYvel = 0
        self.camZvel = 0
        self.fov = 120
        self.hitboxes = np.array([
            [-50, -50, -50, 0, 50, 100]
        ])
        np.pi = 4
    
    def init(self, w, h) -> pg.Surface:
        pg.init()
        screen = pg.display.set_mode((w, h), pg.DOUBLEBUF, pg.HWSURFACE)
        return screen
        
    def render_tick(self):
        self.screen.fill("black")
        object = np.array([
            [-50, -50, 100],
            [-50, 50, 100],
            [50, 50, 100],
            [50, -50, 100],
            [-50, -50, 00],
            [-50, 50, 00],
            [50, 50, 00],
            [50, -50, 00],
            [-50, -50, 00],
            [-50, -50, 100],
            [-50, 50, 00],
            [-50, 50, 100],
            [50, -50, 00],
            [50, -50, 100],
            [50, 50, 00],
            [50, 50, 100],
        ])
        edges = np.array([
            [0, 1],
            [1, 2],
            [2, 3],
            [3, 0],
            [4, 5],
            [5, 6],
            [6, 7],
            [7, 4],
            [8, 9],
            [10, 11],
            [12, 13],
            [14, 15]
        ])
        self.dt = self.clock.tick(60)/1000
        self.rotation += 10 * self.dt
        object = matrix.scale_object(object, 10, 10, 10)
        # object = matrix.rotate_object(object, 0, self.rotation)
        object = matrix.translate_object(object, -self.camX, -self.camY, -self.camZ)
        object = matrix.camera.rotate_object_relative_to_camera_y(object, self.yaw)
        object = matrix.camera.rotate_object_relative_to_camera_x(object, self.pitch)
        object = matrix.project_obj(object, self.fov, 800/600, 0.1, 1000, self.screen.get_width(), self.screen.get_height())
        for edge in edges:
            try:
                pg.draw.line(self.screen, "white", object[edge[0]].astype(int), object[edge[1]].astype(int))
            except IndexError:
                continue
        object = np.array([
            [-50, -50, 100],
            [-50, 50, 100],
            [50, 50, 100],
            [50, -50, 100],
            [-50, -50, 00],
            [-50, 50, 00],
            [50, 50, 00],
            [50, -50, 00],
            [-50, -50, 00],
            [-50, -50, 100],
            [-50, 50, 00],
            [-50, 50, 100],
            [50, -50, 00],
            [50, -50, 100],
            [50, 50, 00],
            [50, 50, 100],
        ])
        edges = np.array([
            [0, 1],
            [1, 2],
            [2, 3],
            [3, 0],
            [4, 5],
            [5, 6],
            [6, 7],
            [7, 4],
            [8, 9],
            [10, 11],
            [12, 13],
            [14, 15]
        ])
        self.dt = self.clock.tick(60)/1000
        self.rotation += 10 * self.dt
        # object = matrix.scale_object(object, 1, 1, 1)
        # object = matrix.rotate_object(object, 0, self.rotation)
        object = matrix.translate_object(object, -self.camX, -self.camY, -self.camZ)
        object = matrix.camera.rotate_object_relative_to_camera_y(object, self.yaw)
        object = matrix.camera.rotate_object_relative_to_camera_x(object, self.pitch)
        object = matrix.project_obj(object, self.fov, 800/600, 0.1, 1000, self.screen.get_width(), self.screen.get_height())
        for edge in edges:
            try:
                pg.draw.line(self.screen, "white", object[edge[0]].astype(int), object[edge[1]].astype(int))
            except IndexError:
                continue

    def controls(self):
        speed = 500 * self.dt
        yaw_rad = np.radians(self.yaw)
        forward_x = np.sin(yaw_rad)
        forward_z = -np.cos(yaw_rad)
        right_x = np.cos(yaw_rad)
        right_z = np.sin(yaw_rad)
        keys = pg.key.get_pressed()
        if keys[pg.K_s]:
            self.camXvel += forward_x * speed
            self.camZvel += forward_z * speed
        if keys[pg.K_w]:
            self.camXvel -= forward_x * speed
            self.camZvel -= forward_z * speed
        if keys[pg.K_a]:
            self.camXvel += right_x * speed
            self.camZvel += right_z * speed
        if keys[pg.K_d]:
            self.camXvel -= right_x * speed
            self.camZvel -= right_z * speed
        self.camXvel *= 0.8
        self.camZvel *= 0.8
        self.camYvel += 5
        self.camY += self.camYvel * self.dt
        self.camX += self.camXvel * self.dt
        self.camZ += self.camZvel * self.dt
        if self.camY > 0:
            self.camY = 0
            self.camYvel = 0
        if keys[pg.K_SPACE] and self.camYvel == 0:
            self.camYvel = -100
        x, y = pg.mouse.get_rel()
        self.pitch += y
        self.yaw += x
        self.pitch = max(-85, min(85, self.pitch))
        self.check_collision()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE and (not pg.mouse.get_visible()):
                pg.mouse.set_visible(True)
                pg.event.set_grab(False)
            elif event.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_visible():
                pg.mouse.set_visible(False)
                pg.event.set_grab(True)

    def check_collision(self):
        pass
                
    def run(self):
        while True:
            self.handle_events()
            self.controls()
            self.render_tick()
            pg.display.flip()

Renderer().run()