import numpy as np
import pyrr
from .material import Material

class Entity:
    def __init__(self, position, eulers, mesh, texture_path, spin = False) -> None:
        self.position = np.array(position, dtype=np.float32)
        self.eulers = np.array(eulers, dtype=np.float32)
        self.mesh = mesh
        self.spin = spin
        self.texture = Material(texture_path)
    
    def get_model_transform(self):
        return pyrr.matrix44.multiply(
            pyrr.matrix44.create_from_eulers(
                eulers = self.eulers,
                dtype = np.float32
            ),
            pyrr.matrix44.create_from_translation(
                vec=np.array(self.position),dtype=np.float32
            )
        )
    
    def update(self, dEulers) -> None:
        self.eulers = (self.eulers + dEulers) % 360

    def destroy(self):
        self.mesh.destroy()
        self.texture.destroy()