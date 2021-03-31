from dataclasses import dataclass
from operator import attrgetter

from Timer import timed

try:
    import pandas as pd

    pd.set_option('precision', 0)
except ImportError:
    pass

INF = float('inf')


@dataclass
class Edge:
    self: int = 0
    other: int = 0
    weight: int = INF

    def __gt__(self, other):
        return max(self.self, self.other) > max(other.self, other.other)

    def __lt__(self, other):
        return max(self.self, self.other) < max(other.self, other.other)

    def __repr__(self):
        return f"Edge({self.self + 1}, {self.other + 1}, {self.weight})"

    def __str__(self):
        return f"{self.self + 1:2} -> {self.other + 1:2} = {self.weight:2}"


class MST:
    def __init__(self):
        self.cost = 0
        self.nodes: list[Edge] = []
        self.basic_ops = 0

    def append(self, node: Edge):
        self.cost += node.weight
        self.nodes.append(node)

    def __repr__(self):
        return repr(self.nodes)

    def __str__(self):
        return "\n".join(edge.__str__() for edge in self.nodes)

    def __iter__(self):
        return iter(self.nodes)

    def __len__(self):
        return len(self.nodes)


class Matrix:
    def __init__(self, adj_list):
        self.len = max(max(adj_list))

        self.adj_matrix = [[INF if r != c else 0 for r in range(self.len)] for c in
                           range(self.len)]

        for (s, o), weight in adj_list.items():
            self.adj_matrix[s - 1][o - 1] = weight
            self.adj_matrix[o - 1][s - 1] = weight

    def __str__(self):
        try:
            return str(pd.DataFrame(self.adj_matrix, columns=range(1, self.len + 1),
                                    index=range(1, self.len + 1)))
        except NameError:
            return '\n'.join(str(row) for row in self.adj_matrix)

    def __len__(self):
        return self.len

    @timed
    def prims(self, v=1, *, show_steps=False):
        vertex = v - 1
        mst = MST()
        edges = []
        visited = []

        while len(mst) < self.len - 1:
            if show_steps:
                print(f"Vertex: {vertex + 1}")

            visited.append(vertex)

            if show_steps:
                print("\tAppending Edges")

            # Append each connected edge to list which  hasn't already been visited and exists
            for other, weight in enumerate(self.adj_matrix[vertex]):
                if other not in visited and weight > 0 and weight != INF:
                    edges.append(Edge(vertex, other, weight))

                    if show_steps:
                        print(f"\t{edges[-1]}")

            mst.basic_ops += len(self.adj_matrix[vertex])

            if edges:
                # Select smallest weighted edge
                min_edge = min(edges, key=attrgetter('weight'))
                mst.basic_ops += len(edges)

                if show_steps:
                    print(f"\tMinimum Edge: {min_edge}")

                vertex = min_edge.other
                mst.append(min_edge)
                edges.remove(min_edge)
            else:
                # No valid Edges Left
                break

        return mst
