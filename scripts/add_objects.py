## Blender Plotting Spiral Practice

import bpy
import numpy as np
from math import sin, cos, pi

cursor_location = bpy.context.scene.cursor_location
Cube = bpy.ops.mesh.primitive_cube_add


def play():
    theta = 0
    r = 3
    two_pi = 4.5*pi

    while theta < two_pi:
        x = r*cos(theta)
        y = r*sin(theta)
        z = 1.5*theta
        Cube(location = (x, y ,z), radius = 0.1)
        x = r*cos(pi + theta)
        y = r*sin(pi + theta)
        z = 1.5*theta
        Cube(location = (x, y, z), radius = 0.1)
        theta += 0.3
        r /= 1.1

    theta = 0
    two_pi = 4.5*pi
    r = 3

    while theta < two_pi:
        y = r*cos(theta)
        x = r*sin(theta)
        z = 1.5*theta
        Cube(location = (x, y ,z), radius = 0.1)
        y = r*cos(pi + theta)
        x = r*sin(pi + theta)
        z = 1.5*theta
        Cube(location = (x, y, z), radius = 0.1)
        theta += 0.3
        r /= 1.1

class Spiral:

    def __init__(self, init_pos, direction, radius = 1):
        self.init_pos = np.array(init_pos)
        d = np.array(direction)
        d = d/np.sqrt(np.sum(d**2))
        self.direction = d
        self.radius = radius

    def _get_outer_matrix(self):
        X = np.zeros((3, 3), dtype = np.float32)
        X[2, 1] = self.direction[0]
        X[1, 2] = -self.direction[0]
        X[2, 0] = -self.direction[1]
        X[0, 2] = self.direction[1]
        X[1, 0] = self.direction[2]
        X[0, 1] = -self.direction[2]
        return X

    def _get_rotation_matrix(self, theta):
        ux = self._get_outer_matrix()
        I = np.diag(np.ones(3))
        R = I + sin(theta) * ux + (1 - cos(theta))*ux.dot(ux)
        return R

    def _get_orthogonal_vec(self):
        e = np.array([0.1, 0.1, 0.1])
        v = np.cross(self.direction, self.direction + e)
        return v

    def plot(self, num_iter = 50, dt = 0.5):
        p = self._get_orthogonal_vec()
        current_pos = self.init_pos
        theta = 0
        for _ in range(num_iter):
            R = self._get_rotation_matrix(theta)
            dx = self.radius * R.dot(p)
            location = current_pos + dx
            Cube(location = location, radius = 0.1)
            theta = theta + pi/12
            current_pos = current_pos + dt * self.direction

class DNA(Spiral):

    def plot(self, num_iter = 50, dt = 0.5):
        p = self._get_orthogonal_vec()
        current_pos = self.init_pos
        theta = 0
        for _ in range(num_iter):
            R = self._get_rotation_matrix(theta)
            dx1 = self.radius * R.dot(p)
            dx2 = self.radius * R.dot(-p)
            location1 = current_pos + dx1
            location2 = current_pos + dx2
            Cube(location = location1, radius = 0.1)
            Cube(location = location2, radius = 0.1)
            theta = theta + pi/12
            current_pos = current_pos + dt * self.direction

def play2():
    theta = 0
    start_pos = np.array([1, 0, 0])
    for _ in range(20):
        R = np.array([[cos(theta), -sin(theta), 0],
                      [sin(theta), cos(theta),  0],
                      [0         , 0         ,  1]])
        location = R.dot(np.array(start_pos)) + np.array([0, 0, 1])
        DNA(location, [1, 1, 1], 10).plot(10, dt = 0.3)
        theta = theta + pi/20
