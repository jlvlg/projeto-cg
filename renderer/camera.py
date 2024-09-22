import numpy as np

class Camera:
    def __init__(self, position) -> None:
        self.position = np.array(position, dtype=np.float32)
        self.theta = 0
        self.phi = 0
        self.update_vectors()
    
    def update_vectors(self):
        self.forwards = np.array([
            np.cos(np.deg2rad(self.phi)) * np.sin(np.deg2rad(self.theta)), 
            np.sin(np.deg2rad(self.phi)),
            np.cos(np.deg2rad(self.phi)) * np.cos(np.deg2rad(self.theta)), 
            ], 
            dtype=np.float32)
        self.right = np.cross(self.forwards, np.array([0,1,0], dtype=np.float32))
        self.up = np.cross(self.right, self.forwards)