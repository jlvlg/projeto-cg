import numpy as np
from .camera import Camera
from itertools import chain
from .mesh import Mesh
from .entity import Entity

class Scene:
    def __init__(self, maze, cameraPos, on_end) -> None:
        self.maze = maze
        self._gen_mesh()
        self.on_end = on_end
        self.camera = Camera(cameraPos)
        self.can_move = True
        print(self.maze.end)

    def _gen_mesh(self):
        faces, vertices, self.bounding_boxes = self.maze.to_face_vertex()
        v = []
        for face in faces:
            v.append([*vertices[face[0]], 0, 1])
            v.append([*vertices[face[1]], 0, 0])
            v.append([*vertices[face[2]], 1, 1])
            v.append([*vertices[face[3]], 0, 0])
            v.append([*vertices[face[4]], 1, 0])
            v.append([*vertices[face[5]], 1, 1])
        self.entities = [
            Entity([0,0,0], [0,0,0], Mesh(np.array(list(chain.from_iterable(v)), dtype=np.float32)), './renderer/gfx/wall.png'),
            Entity([0,0,0], [0,0,0], Mesh(np.array([0, 0, 0, 0, 0, 
                    self.maze.width, 0, 0, self.maze.width, 0, 
                    0, 0, self.maze.height, 0, self.maze.height,
                    0, 0, self.maze.height, 0, self.maze.height,
                    self.maze.width, 0, 0, self.maze.width, 0,
                    self.maze.width, 0, self.maze.height, self.maze.width, self.maze.height], 
                    dtype=np.float32)), './renderer/gfx/tiles.png'),
            Entity([self.maze.end[0] + 0.5, 0.5, self.maze.end[1] + 0.5], [0, 0, 0], Mesh(
                    np.array([
                        -0.125, 0.125, 0, 0, 0,
                        0.125, 0.125, 0, 1, 0,
                        -0.125, -0.125, 0, 0, 1,         
                        0.125, 0.125, 0, 1, 0,
                        0.125, -0.125, 0, 1, 1,
                        -0.125, -0.125, 0, 0, 1
                    ], dtype=np.float32)), './renderer/gfx/kali.png', True)
        ]
    
    def move_camera(self, dPos):
        if not self.can_move:
            return
        dPos = np.array(dPos, dtype=np.float32)
        cell_pos = (int(self.camera.position[0]), int(self.camera.position[2]))
        starbb = [[self.maze.end[0] + 0.25, 0.25, self.maze.end[1] + 0.25], [self.maze.end[0] + 0.75, 0.75, self.maze.end[1] + 0.75]]
        print(cell_pos)
        for x in range(-1, 2):
            for z in range (-1, 2):
                for boundary in self.bounding_boxes.get((cell_pos[0] + x, cell_pos[1] + z), []):
                    if self.check_colision(self.camera.position + [dPos[0], 0, 0], boundary):
                        dPos[0] = 0
                    if self.check_colision(self.camera.position + [0, 0, dPos[2]], boundary):
                        dPos[2] = 0
        if (cell_pos[0], cell_pos[1]) == self.maze.end and self.check_colision(self.camera.position + dPos, starbb):
                self.can_move = False
                self.on_end()
        self.camera.position += dPos

    def check_colision(self, camerabb, checkingbb):
        return (camerabb[0] - 0.1 <= checkingbb[1][0] and
                camerabb[0] + 0.1 >= checkingbb[0][0] and 
                camerabb[1] - 0.1 <= checkingbb[1][1] and 
                camerabb[1] + 0.1 >= checkingbb[0][1] and 
                camerabb[2] - 0.1 <= checkingbb[1][2] and 
                camerabb[2] + 0.1 >= checkingbb[0][2])
                

    def spin_camera(self, dTheta, dPhi):
        self.camera.theta = (self.camera.theta + dTheta) % 360
        self.camera.phi = min(89, max(-89, self.camera.phi + dPhi))
        self.camera.update_vectors()

    def destroy(self):
        for entity in self.entities:
            entity.destroy()