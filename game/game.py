from .maze import Maze
from renderer.renderer import Renderer
import random
import glfw
import glfw.GLFW as GLFW
from renderer.scene import Scene
import numpy as np

RETURN_ACTION_CONTINUE = 0
RETURN_ACTION_END = 1

WALK_DIRECTION_OFFSET = {
    1: 0,
    2: 90,
    3: 45,
    4: 180,
    6: 135,
    7: 90,
    8: 270,
    9: 315,
    11: 0,
    12: 225,
    13: 270,
    14: 180,
}

class Game:
    def __init__(self, screen_width, screen_height, maze_width, maze_height) -> None:
        self.maze_width = maze_width
        self.maze_height = maze_height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.renderer = Renderer(screen_width, screen_height)
        self.scene = None

        glfw.init()
        glfw.window_hint(GLFW.GLFW_CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(GLFW.GLFW_CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(GLFW.GLFW_OPENGL_PROFILE, GLFW.GLFW_OPENGL_CORE_PROFILE)
        glfw.window_hint(GLFW.GLFW_OPENGL_FORWARD_COMPAT, GLFW.GLFW_TRUE)
        glfw.window_hint(GLFW.GLFW_DOUBLEBUFFER, GLFW.GLFW_FALSE)

        self.window = glfw.create_window(screen_width, screen_height, 'Encontre a estrela', None, None)
        glfw.make_context_current(self.window)
        glfw.set_input_mode(self.window, GLFW.GLFW_CURSOR, GLFW.GLFW_CURSOR_HIDDEN)

    def _start_new_game(self):
        self.maze = Maze(self.maze_width, self.maze_height)
        if self.scene:
            self.scene.destroy()
        self.scene = Scene(self.maze, (random.randint(0, self.maze_width - 1) + 0.5, 0.5, random.randint(0, self.maze_height - 1) + 0.5), on_end=self._start_new_game)

    def mainloop(self):
        self._start_new_game()
        self.renderer.setup()
        self.last_time = glfw.get_time()
        self.delta = 0
        
        while not glfw.window_should_close(self.window):
            self._handle_events()
            self.renderer.render(self.scene)
            self.scene.entities[2].update([0, 0, self.delta * 1])
            self._calculate_frame_rate()
        self._quit()

    def _quit(self):
        self.renderer.quit()
        self.scene.destroy()
        glfw.destroy_window(self.window)

    def _calculate_frame_rate(self):
        current_time = glfw.get_time()
        self.delta = current_time - self.last_time
        self.last_time = current_time


    def _handle_events(self):
        if glfw.get_key(self.window, GLFW.GLFW_KEY_ESCAPE) == GLFW.GLFW_PRESS:
            glfw.set_window_should_close(self.window, True)
        self._handle_movement()
        self._handle_mouse()
        glfw.poll_events()

    def _handle_movement(self):
        combo = 0
        if glfw.get_key(self.window, GLFW.GLFW_KEY_W) == GLFW.GLFW_PRESS:
            combo += 1
        if glfw.get_key(self.window, GLFW.GLFW_KEY_A) == GLFW.GLFW_PRESS:
            combo += 2
        if glfw.get_key(self.window, GLFW.GLFW_KEY_S) == GLFW.GLFW_PRESS:
            combo += 4
        if glfw.get_key(self.window, GLFW.GLFW_KEY_D) == GLFW.GLFW_PRESS:
            combo += 8
        
        if combo in WALK_DIRECTION_OFFSET:
            direction = WALK_DIRECTION_OFFSET[combo]
            dPos = [
                self.delta * 2 * np.sin(np.deg2rad(self.scene.camera.theta + direction)),
                0,
                self.delta * 2 * np.cos(np.deg2rad(self.scene.camera.theta + direction)),
            ] 
            self.scene.move_camera(dPos)

    def _handle_mouse(self):
        (x, y) = glfw.get_cursor_pos(self.window)
        rate = self.delta * 100
        theta_increment = rate * (self.screen_width / 2 - x)
        phi_increment = rate * (self.screen_height / 2 - y)
        self.scene.spin_camera(theta_increment, phi_increment)
        glfw.set_cursor_pos(self.window, self.screen_width / 2, self.screen_height / 2)