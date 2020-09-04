import unittest
from operator import and_
from unittest.mock import patch

from main.dijk import Graph, apply_dijkstra, find_shortest_path


class TestGraph(unittest.TestCase):
    def setUp(self):
        self.graph = Graph(input_file_path='tests/samples/samples.csv')

    def test_add_node(self):
        assert self.graph.add_node('foo') is None
    
    def test_add_node_fails(self):
        self.assertRaises(AssertionError, self.graph.add_node, '')
    
    def test_add_edge(self):
        assert self.graph.add_edge(
            from_node='foo', 
            to_node='bar', 
            weight=42
        ) is None
    
    def test_add_edge_fails(self):
        self.assertRaises(
            AssertionError,
            self.graph.add_edge,
            'foo', 
            'foo', 
            42
        )

class TestHelpersFunctions(unittest.TestCase):
    def setUp(self):
        self.graph = Graph(input_file_path='tests/samples/samples.csv')

    def test_apply_dijkstra(self):
        visited, paths = apply_dijkstra(self.graph, 'GRU')

        conditions = [
            and_(
                visited == {
                    'GRU': 0, 
                    'BRC': 10, 
                    'CDG': 40, 
                    'SCL': 15, 
                    'ORL': 35
                },
                paths == {
                    'BRC': 'GRU', 
                    'CDG': 'ORL', 
                    'SCL': 'BRC', 
                    'ORL': 'SCL'
                }
            )
        ]

        assert all(conditions)

    @patch('main.dijk.apply_dijkstra')
    def test_find_shortest_path(self, fn):
        visited = {
            'GRU': 0, 
            'BRC': 10, 
            'CDG': 40, 
            'SCL': 15, 
            'ORL': 35
        }

        paths = {
            'BRC': 'GRU', 
            'CDG': 'ORL', 
            'SCL': 'BRC', 
            'ORL': 'SCL'
        }

        fn.return_value = (visited, paths)

        assert find_shortest_path(self.graph, 'GRU', 'SCL')[1] == ['GRU', 'BRC', 'SCL']


if __name__ == '__main__':
    unittest.main()