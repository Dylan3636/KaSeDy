import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


class Map:
    def __init__(self, full_connections, colour_map,pos=None):
        split = [[list(l) for l in zip(*temp)] for temp in full_connections]
        connections= []
        directions= []
        for temp in split:
            connections.append(temp[0])
            directions.append(temp[1])
        self.connections = np.array(connections)
        self.direction_map = np.array(directions)
        self.colour_map = np.array(colour_map)
        self.pos = pos

    def find_connections(self, node):
        return self.connections[node]

    def is_connected(self, n1, n2):
        return n2 in self.connections[n1]

    def colour_of(self, node):
        return self.colour_map[node]

    def show(self):
        edges = []
        for i in range(0, np.size(self.connections, 0)):
            for j in range(0, np.size(self.connections[i], 0)):
                edges.append((i + 1, self.connections[i][j]))
        G = nx.Graph()
        G.add_edges_from(edges)
        if self.pos ==None:
            pos = self.get_pos()
            self.pos = pos
        else:
            pos = self.pos
        #print nx.random_layout(G)
        #print pos
        for i in range(0, len(self.colour_map)):
            nx.draw_networkx_nodes(G, pos, nodelist=[i + 1], node_color=[self.colour_map[i]])
            nx.draw_networkx_labels(G, pos, labels={i + 1: i + 1})
        nx.draw_networkx_edges(G, pos)
        # print edges
        # nx.draw(G)
        # nx.draw_networkx_labels(G,labels=range(1, len(self.colour_map)))
        plt.title('Graph')
        plt.show()

    def get_pos(self):
        pos = {1: np.array([5, 5])}
        for i in range(0, np.size(self.connections, 0)):
            for j in range(0, len(self.connections[i])):
                x = 0
                y = 0
                ind = self.connections[i][j]
                card = self.direction_map[i][j]
                if card == 'N':
                    x, y = 0, 1
                elif card == 'S':
                    x, y = 0, -1
                elif card == 'E':
                    x, y = 1, 0
                else:
                    x, y = -1, 0
                pos[ind] = np.array([pos[i + 1][0] + x, pos[i + 1][1] + y])
        return pos


def test():
    full_connections = [[(2, 'N'), (3, 'W')], [(1, 'S')], [(1, 'E')]]
    colour_map = ['B', 'R', 'R']
    map = Map(full_connections, colour_map)
    print map.connections
    print map.direction_map
    map.show()


if __name__ == '__main__':
    test()
