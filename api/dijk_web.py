from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse as urlparse
import csv
import json

from main.dijk import Graph, find_shortest_path


class ServiceHandler(BaseHTTPRequestHandler):
    def do_check(self, qs):
        if 'from' not in qs and 'to' not in qs:
            self.send_response(400)
        else:
            from_node = str(qs['from'][0]).upper()
            to_node = str(qs['to'][0]).upper()

            graph = Graph()

            try:
                result = find_shortest_path(
                    graph=graph,
                    origin_node=from_node,
                    destination_node=to_node
                )

                msg = json.dumps(
                    {
                        'path': ' - '.join(result[1]),
                        'price': f'${result[0]}',
                        'error': False
                    }
                )

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.wfile.write(bytes(msg, 'utf-8'))
                self.end_headers()

            except KeyError:
                msg = json.dumps(
                    {
                            'error': True,
                            'path': '',
                            'price': ''
                        },
                )

                self.wfile.write(
                    bytes(
                        msg,
                        'utf-8'
                    )
                )
                self.send_response(404, 'Not Found: record does not exist')
                self.send_header('Content-Type', 'application/json')
                self.end_headers()

    def do_insert(self, qs):
        if 'from' not in qs and 'to' not in qs and 'weight' not in qs:
            self.send_response(400, 'Bad Request: invalid keys')
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()

            return

        else:
            from_node = str(qs['from'][0]).upper()
            to_node = str(qs['to'][0]).upper()
            weight = int(qs['weight'][0])

            with open('input-routes.csv', 'a') as data_file:
                writer = csv.writer(
                    data_file,
                    delimiter=',',
                    lineterminator='\n'
                )

                writer.writerow([from_node, to_node, weight])

            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()

    def do_POST(self):
        parsed_route = urlparse.urlsplit(self.path)
        qs = {}

        if parsed_route.path == '/insert':
            if parsed_route.query:
                qs = urlparse.parse_qs(parsed_route.query)

            self.do_insert(qs)
        else:
            self.send_response(404)

    def do_GET(self):
        parsed_route = urlparse.urlsplit(self.path)
        qs = {}

        if parsed_route.path == '/check':
            if parsed_route.query:
                qs = urlparse.parse_qs(parsed_route.query)

            self.do_check(qs)
        else:
            self.send_response(404)


if __name__ == '__main__':
    server = HTTPServer(('127.0.0.1', 8080), ServiceHandler)
    server.serve_forever()
