from typing import Tuple
from collections import defaultdict, deque
import csv
import os


class Graph(object):
    def __init__(self, input_file_path: str=''):
        self.nodes = set()
        self.edges = defaultdict(list)
        self.distances = {}
        self.input_file_path = input_file_path

        unique_nodes = set()

        if os.path.exists(self.input_file_path):
            path = self.input_file_path
        else:
            path = 'data/input-routes.csv'

        with open(path, 'r+') as data_file:
            for item in csv.DictReader(
                data_file,
                skipinitialspace=True
            ):
                if item['from'] in unique_nodes:
                    self.add_node(item['from'])
                else:
                    unique_nodes.add(item['from'])

                if item['to'] in unique_nodes:
                    self.add_node(item['to'])
                else:
                    unique_nodes.add(item['to'])

                self.add_edge(item['from'], item['to'], int(item['weight']))

    def add_node(self, name: str):
        assert isinstance(name, str)
        assert name.strip()

        self.nodes.add(name)

    def add_edge(self, from_node: str, to_node: str, weight: int):
        assert isinstance(from_node, str)
        assert isinstance(to_node, str)
        assert isinstance(weight, int)
        assert from_node != to_node

        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.distances[(from_node, to_node)] = weight


def apply_dijkstra(graph: Graph, initial_node: str) -> Tuple[dict, dict]:
    assert isinstance(graph, Graph)
    assert isinstance(initial_node, str)

    visited = {initial_node: 0}
    path = {}

    nodes = set(graph.nodes)

    while nodes:
        min_node = None
        for node in nodes:
            if node in visited:
                if min_node is None:
                    min_node = node
                elif visited[node] < visited[min_node]:
                    min_node = node
        if min_node is None:
            break

        nodes.remove(min_node)
        current_weight = visited[min_node]

        for edge in graph.edges[min_node]:
            try:
                weight = current_weight + graph.distances[(min_node, edge)]
            except KeyError:
                continue

            if edge not in visited or weight < visited[edge]:
                visited[edge] = weight
                path[edge] = min_node

    return visited, path


def find_shortest_path(
    graph: Graph,
    origin_node: str,
    destination_node: str
) -> Tuple[str, list]:
    assert isinstance(graph, Graph)
    assert isinstance(origin_node, str)
    assert isinstance(destination_node, str)

    visited, paths = apply_dijkstra(graph, origin_node)
    full_path = deque()
    _destination_node = paths[destination_node]

    while _destination_node != origin_node:
        full_path.appendleft(_destination_node)
        _destination_node = paths[_destination_node]

    full_path.appendleft(origin_node)
    full_path.append(destination_node)

    return visited[destination_node], list(full_path)
