
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import compileShader, compileProgram
import numpy as np
from .material import Material
import pyrr

class Renderer:
    def __init__(self, screen_width, screen_height) -> None:
        self.screen_width = screen_width
        self.screen_height = screen_height
        
    def setup(self):
        self._setup_opengl()
        self._setup_shaders()
        
        glUniformMatrix4fv(
            glGetUniformLocation(self.shader, "projection"),
            1,
            GL_FALSE,
            pyrr.matrix44.create_perspective_projection(fovy = 45, aspect = self.screen_width/self.screen_height, near = 0.1, far = 10, dtype=np.float32)
        )
        glUniform1i(glGetUniformLocation(self.shader, "imageTexture"), 0)
        self.modelMatrixLocation = glGetUniformLocation(self.shader, "model")
        self.cameraMatrixLocation = glGetUniformLocation(self.shader, "camera")
    
    def _setup_opengl(self):
        glClearColor(0.1, 0.2, 0.2, 1)
        glEnable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def _setup_shaders(self):
        with open('./renderer/shaders/vertex.vs') as f:
            vs_src = f.readlines()
        with open('./renderer/shaders/fragment.fs') as f:
            fs_src = f.readlines()
        self.shader = compileProgram(
            compileShader(vs_src, GL_VERTEX_SHADER),
            compileShader(fs_src, GL_FRAGMENT_SHADER)
        )
        glUseProgram(self.shader)

    def render(self, scene):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(self.shader)

        camera_transform = pyrr.matrix44.create_look_at(
            eye = scene.camera.position, 
            target = scene.camera.position + scene.camera.forwards, 
            up = scene.camera.up,
            dtype = np.float32)
        glUniformMatrix4fv(self.cameraMatrixLocation, 1, GL_FALSE, camera_transform)

        for entity in scene.entities:
            glUniformMatrix4fv(
                    self.modelMatrixLocation, 1, GL_FALSE, 
                    entity.get_model_transform())
            entity.texture.use()
            glBindVertexArray(entity.mesh.vao)
            glDrawArrays(GL_TRIANGLES, 0, entity.mesh.vertex_count)

        glFlush()

    def quit(self):
        glDeleteProgram(self.shader)