from main.dijk import Graph, find_shortest_path

import re

if __name__ == '__main__':
    print('----- Press 0 + Enter to end ----- \n')

    while True:
        user_input = input("please enter the route: ")

        if user_input == '0':
            exit(0)

        match = re.search(
            r"^(?P<from>[A-Z]+)\s*\-\s*(?P<to>[A-Z]+)$",
            user_input
        )

        if match:
            from_node = match.groupdict()['from']
            to_node = match.groupdict()['to']

            graph = Graph()

            result = find_shortest_path(
                graph=graph,
                origin_node=from_node,
                destination_node=to_node
            )

            path = ' - '.join(result[1])
            price = f'${result[0]}'

            print(f'best route: {path} > {price}')
