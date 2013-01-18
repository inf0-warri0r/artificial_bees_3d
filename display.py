"""
Author : tharindra galahena (inf0_warri0r)
Project: artificial bees simulation using neural networks - part 2
Blog   : http://www.inf0warri0r.blogspot.com
Date   : 18/01/2013
License:

     Copyright 2013 Tharindra Galahena

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version. This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
details.

* You should have received a copy of the GNU General Public License along with
This program. If not, see http://www.gnu.org/licenses/.

"""

import math

from OpenGL.GL import *
from OpenGL.GLU import *

import pygame
from pygame.locals import *


class display:
    def __init__(self, width, height):
        self.width = 600
        self.height = 600
        pygame.init()
        pygame.display.set_mode((self.width, self.height),
            pygame.OPENGL | pygame.DOUBLEBUF)

        self.clock = pygame.time.Clock()

        self.rx = 0
        self.ry = 0
        self.rz = 0

        self.xx = 0
        self.yy = 0
        self.zz = 20

        self.sl = list()

    def key_bord(self):

        for event in pygame.event.get():
            if event.type == KEYUP:
                if event.key == K_a:
                    self.ry = (self.ry + 10) % 360
                if event.key == K_s:
                    self.ry = (self.ry - 10) % 360
                if event.key == K_d:
                    self.yy = self.yy + 1
                if event.key == K_f:
                    self.yy = self.yy - 1
                if event.key == K_g:
                    self.zz = self.zz + 1
                if event.key == K_h:
                    self.zz = self.zz - 1
                if event.key == K_q:
                    exit()

    def set_cod(self, h):
        self.sl = list()
        for j in range(0, 8):
            m = list()
            r = h * math.cos(j * math.pi / 4)
            zz = h * math.sin(j * math.pi / 4)
            for i in range(0, 8):
                a = r * math.cos(i * math.pi / 4)
                b = r * math.sin(i * math.pi / 4)
                m.append((a, zz, b))
            self.sl.append(m)

    def cube(self, x, y, z, color, l):

        x1 = x - l
        x2 = x + l

        y1 = y - l
        y2 = y + l

        z1 = z + l
        z2 = z - l

        glColor3f(color[0], color[1], color[2])

        glBegin(GL_QUADS)

        glVertex3f(x1, y1, z1)
        glVertex3f(x2, y1, z1)
        glVertex3f(x2, y2, z1)
        glVertex3f(x1, y2, z1)

        glVertex3f(x1, y1, z2)
        glVertex3f(x2, y1, z2)
        glVertex3f(x2, y2, z2)
        glVertex3f(x1, y2, z2)

        glVertex3f(x1, y2, z1)
        glVertex3f(x2, y2, z1)
        glVertex3f(x2, y2, z2)
        glVertex3f(x1, y2, z2)

        glVertex3f(x1, y1, z1)
        glVertex3f(x1, y2, z1)
        glVertex3f(x1, y2, z2)
        glVertex3f(x1, y1, z2)

        glVertex3f(x2, y1, z1)
        glVertex3f(x2, y2, z1)
        glVertex3f(x2, y2, z2)
        glVertex3f(x2, y1, z2)

        glEnd()

    def spear(self, x, y, z, color):

        a = x
        b = y
        c = z
        glBegin(GL_QUADS)
        for j in range(0, 8):
            for i in range(0, 8):
                p1 = self.sl[j][i]
                p2 = self.sl[j][(i + 1) % 8]
                p3 = self.sl[(j + 1) % 8][(i + 1) % 8]
                p4 = self.sl[(j + 1) % 8][i]
                glColor3f(1, 0, 0)
                glVertex3f(p1[0] + a, p1[1] + b, p1[2] + c)
                glVertex3f(p2[0] + a, p2[1] + b, p2[2] + c)
                glColor3f(1, 1, 0)
                glVertex3f(p3[0] + a, p3[1] + b, p3[2] + c)
                glVertex3f(p4[0] + a, p4[1] + b, p4[2] + c)
        glEnd()

    def set_display(self):
        glMatrixMode(GL_TEXTURE)
        glLoadIdentity()

        glLightfv(GL_LIGHT0, GL_POSITION, [0, 4, 0])

        glClearColor(0.0, 0.0, 0.0, 0.0)
        glMatrixMode(GL_PROJECTION)

        glLoadIdentity()
        gluPerspective(90, 1, 0.01, 1000)
        gluLookAt(0, self.yy, self.zz, 0, 0, 0, 0, 1, 0)
        glRotate(self.ry, 0, 1, 0)
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def flip(self):
        pygame.display.flip()
