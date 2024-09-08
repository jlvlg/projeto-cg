import random
import networkx as nx
import matplotlib.pyplot as plt


class Maze:
    def __init__(self, height, width) -> None:
        self.height = height
        self.width = width
        self._graph = nx.Graph()
        self._graph.add_nodes_from(
            [(x, y) for x in range(width) for y in range(height)]
        )
        self._generate_maze()

    def forward(self, coord, direction):
        forward = (
            coord[0] + (-1 if direction == 3 else 1 if direction == 1 else 0),
            coord[1] + (-1 if direction == 0 else 1 if direction == 2 else 0),
        )
        return forward if forward in self._graph[coord] else None

    def to_face_vertex(self):
        vertices = [
            (x, y, z)
            for z in range(self.height + 1)
            for x in range(self.width + 1)
            for y in range(2)
        ]
        faces = []
        for x, z in self._graph:
            adj = self._graph[(x, z)]
            if (x, z - 1) not in adj:
                wall_vertices = [
                    vertices.index((x, 0, z)),
                    vertices.index((x, 1, z)),
                    vertices.index((x + 1, 1, z)),
                    vertices.index((x + 1, 0, z)),
                ]
                faces.append(wall_vertices)
            if (x + 1, z) not in adj:
                wall_vertices = [
                    vertices.index((x + 1, 0, z)),
                    vertices.index((x + 1, 1, z)),
                    vertices.index((x + 1, 1, z + 1)),
                    vertices.index((x + 1, 0, z + 1)),
                ]
                faces.append(wall_vertices)
            if (x, z + 1) not in adj:
                wall_vertices = [
                    vertices.index((x + 1, 0, z + 1)),
                    vertices.index((x + 1, 1, z + 1)),
                    vertices.index((x, 1, z + 1)),
                    vertices.index((x, 0, z + 1)),
                ]
                faces.append(wall_vertices)
            if (x - 1, z) not in adj:
                wall_vertices = [
                    vertices.index((x, 0, z + 1)),
                    vertices.index((x, 1, z + 1)),
                    vertices.index((x, 1, z)),
                    vertices.index((x, 0, z)),
                ]
                faces.append(wall_vertices)
        return faces, vertices

    def _generate_maze(self):
        random_point = (
            random.randint(0, self.width - 1),
            random.randint(0, self.height - 1),
        )
        self._dfs(random_point, set())

    def _neighbors(self, coords):
        neighbors = []
        x, y = coords
        if x > 0:
            neighbors.append((x - 1, y))
        if x < self.width - 1:
            neighbors.append((x + 1, y))
        if y > 0:
            neighbors.append((x, y - 1))
        if y < self.height - 1:
            neighbors.append((x, y + 1))
        return neighbors

    def _dfs(self, node, visited):
        visited.add(node)
        neighbors = self._neighbors(node)
        random.shuffle(neighbors)
        for neighbor in neighbors:
            if neighbor not in visited:
                self._graph.add_edge(node, neighbor)
                self._dfs(neighbor, visited)
