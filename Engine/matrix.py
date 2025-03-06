# repo: https://github.com/ADRIKPANJA/py-3d
# matrix.py

'''The module for 3D transformations and perspective.'''

import numpy as np

class matrix:
    '''The class for matrices.'''
    @staticmethod
    def translation_matrix(tx, ty, tz) -> np.array:
        '''Translation matrix.'''
        return np.array([
            [1, 0, 0, tx],
            [0, 1, 0, ty],
            [0, 0, 1, tz],
            [0, 0, 0,  1]
        ])
    @staticmethod
    def scaling_matrix(sx, sy, sz) -> np.array:
        '''Scaling matrix'''
        return np.array([
            [sx,  0,  0, 0],
            [ 0, sy,  0, 0],
            [ 0,  0, sz, 0],
            [ 0,  0,  0, 1]
        ])
    @staticmethod
    def rotation_x_matrix(pitch) -> np.array:
        '''Rotation x'''
        pitch = np.radians(pitch)
        return np.array([
            [1,             0,              0, 0],
            [0, np.cos(pitch), -np.sin(pitch), 0],
            [0, np.sin(pitch),  np.cos(pitch), 0],
            [0,             0,              0, 1]
        ])
    @staticmethod
    def rotation_y_matrix(yaw) -> np.array:
        '''Rotation y'''
        yaw = np.radians(yaw)
        return np.array([
            [ np.cos(yaw), 0, np.sin(yaw), 0],
            [          0,  1,           0, 0],
            [-np.sin(yaw), 0, np.cos(yaw), 0],
            [           0, 0,           0, 1]
        ])
    @staticmethod
    def perspective_projection_matrix(fov, near_clipping_plane, far_clipping_plane, aspect) -> np.array:
        '''The perspective projection matrix'''
        fov = np.radians(fov)
        return np.array([
            [1/(aspect*np.tan(fov/2)),                        0,                                                                                     0,                                                                                     0],
            [                       0,        1/(np.tan(fov/2)),                                                                                     0,                                                                                     0],
            [                       0,                        0, (far_clipping_plane + near_clipping_plane)/(near_clipping_plane - far_clipping_plane), (2*far_clipping_plane*near_clipping_plane)/(near_clipping_plane - far_clipping_plane)],
            [                       0,                        0,                                                                                    -1,                                                                                     0]
        ])
    
def get_center(obj):
    obj = np.array(obj)
    return np.mean(obj, axis=0)

def translate_object(object, tx, ty, tz) -> list[float, float, float]:
    '''Translates an object based on {tx}, {ty} and {tz}'''
    object = np.array(object)
    obj = []
    for x, y, z in object:
        matrix_ = matrix.translation_matrix(tx, ty, tz)
        point_h = np.array([x, y, z, 1])
        translated_point = np.dot(matrix_, point_h)
        obj.append(translated_point[:3])
    return obj

def scale_object(object, sx, sy, sz) -> list[list[float, float, float]]:
    '''Scales an object based on {sx}, {sy} and {sz}'''
    cx, cy, cz = get_center(object)
    object = [[x - cx, y - cy, z - cz] for x, y, z in object]
    matrix_ = matrix.scaling_matrix(sx, sy, sz)
    obj = []
    for x, y, z in object:
        point_h = np.array([x, y, z, 1])
        obj.append(np.dot(matrix_, point_h)[:3])
    final_obj = [[x + cx, y + cy, z + cz] for x, y, z in obj]
    return final_obj

def rotate_object_x(object, pitch):
    '''Rotates an object based on {pitch}'''
    cx, cy, cz = get_center(object)
    object = [[x - cx, y - cy, z - cz] for x, y, z in object]
    matrix_ = matrix.rotation_x_matrix(pitch)
    obj = []
    for x, y, z in object:
        point_h = np.array([x, y, z, 1])
        obj.append(np.dot(matrix_, point_h)[:3])
    final_obj = [[x + cx, y + cy, z + cz] for x, y, z in obj]
    return final_obj

def rotate_object_y(object, yaw):
    '''Rotates an object based on {pitch}'''
    cx, cy, cz = get_center(object)
    object = [[x - cx, y - cy, z - cz] for x, y, z in object]
    matrix_ = matrix.rotation_y_matrix(yaw)
    obj = []
    for x, y, z in object:
        point_h = np.array([x, y, z, 1])
        obj.append(np.dot(matrix_, point_h)[:3])
    final_obj = [[x + cx, y + cy, z + cz] for x, y, z in obj]
    return final_obj

def rotate_object(object, pitch, yaw):
    '''Rotates an object.'''
    cx, cy, cz = get_center(object)
    object = [[x - cx, y - cy, z - cz] for x, y, z in object]
    matrix_ = matrix.rotation_y_matrix(yaw) @ matrix.rotation_x_matrix(pitch)
    obj = []
    for x, y, z in object:
        point_h = np.array([x, y, z, 1])
        obj.append(np.dot(matrix_, point_h)[:3])
    final_obj = [[x + cx, y + cy, z + cz] for x, y, z in obj]
    return final_obj


def project_obj(obj, fov, aspect_ratio, near, far, screen_width, screen_height):
    object = []
    matrix_ = matrix.perspective_projection_matrix(fov, near, far, aspect_ratio)
    for x, y, z in obj:
        if z < near:
            z = near
        temp = np.dot(matrix_, np.array([x, y, z, 1]))
        if not (abs(temp[3]) < 1e-6):
            temp /= temp[3]
        else:
            continue
        screen_x = ((temp[0] + 1)/2) * screen_width
        screen_y = ((1 - temp[1])/2) * screen_height
        object.append(np.array([screen_x, screen_y]))
    return object

class camera():
    '''Transformations for the camera.'''
    @staticmethod
    def rotate_object_relative_to_camera_x(object, pitch):
        '''Rotates an object.'''
        matrix_ = matrix.rotation_x_matrix(pitch)
        obj = []
        for x, y, z in object:
            point_h = np.array([x, y, z, 1])
            obj.append(np.dot(matrix_, point_h)[:3])
        return obj
    @staticmethod
    def rotate_object_relative_to_camera_y(object, yaw):
        '''Rotates an object.'''
        matrix_ = matrix.rotation_y_matrix(yaw)
        obj = []
        for x, y, z in object:
            point_h = np.array([x, y, z, 1])
            obj.append(np.dot(matrix_, point_h)[:3])
        return obj

# Demo obj
# object = np.array([
#     [-50, -50, 0],
#     [50, -50, 0],
#     [50, 50, 0],
#     [50, -50, 0],
#     [-50, -50, 100],
#     [50, -50, 100],
#     [50, 50, 100],
#     [50, -50, 100],
#     [-50, -50, 0],
#     [-50, -50, 100],
#     [50, -50, 0],
#     [50, -50, 100],
#     [50, 50, 0],
#     [50, 50, 100],
#     [-50, 50, 0],
#     [-50, 50, 100],
# ])
