from maze import Maze
import random
import enum
import networkx as nx
import matplotlib.pyplot as plt


class Game:
    def __init__(self, maze) -> None:
        self.maze = maze
        self.direction = 0  # NORTH -> EAST -> SOUTH -> WEST
        self.player = (
            random.randint(0, maze.width - 1),
            random.randint(0, maze.height - 1),
        )
        self.end = (
            random.randint(0, maze.width - 1),
            random.randint(0, maze.height - 1),
        )
        self.maze.to_face_vertex()

    def turn_right(self):
        self.direction = (self.direction + 1) % 4

    def turn_left(self):
        self.direction = (self.direction - 1) % 4

    def foward(self):
        print(self.player)
        forward = self.maze.forward(self.player, self.direction)
        if forward:
            self.player = forward
        print(self.player)


if __name__ == "__main__":
    game = Game(Maze(10, 10))
    pos = {(x, y): (x, -y) for x, y in game.maze._graph}
    nx.draw(
        game.maze._graph,
        pos,
        node_color=[
            ("green" if x == game.player else ("red" if x == game.end else "skyblue"))
            for x in game.maze._graph
        ],
    )
    plt.show()
