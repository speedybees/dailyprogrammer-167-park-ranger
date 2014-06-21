import re

def next_letter(letter):
    return chr(ord(letter) + 1)

class UndirectedEdge(object):
    def __init__(self, length, v1, v2):
        self.length = length
        self.vertices = set([v1, v2])

    def __repr__(self):
        return "{0}: {1}".format([vertex.name for vertex in self.vertices], self.length)

class Vertex(object):
    def __init__(self, name):
        self.name = name
        self.edges = set()

    def __getitem__(self, location):
        return self.edges[location]

    def __repr__(self):
        return "'" + self.name + "': {" \
               + ', '.join(["{0}: {1}".format(
                                [vertex.name for vertex in edge.vertices if vertex != self][0], 
                                edge.length) 
                            for edge in sorted(self.edges)]) + "}"

    def add_edge(self, edge):
        self.edges.add(edge)

    def remove_edge(self, edge):
        self.edges.remove(edge)

class Graph(object):
    def __init__(self):
        self._vertices = {}

    def __getitem__(self, location):
        return self._vertices[location]

    def __iter__(self):
        return self._vertices.__iter__()

    def __repr__(self):
        to_return = ''
        for vertex in sorted(self._vertices.items()):
            to_return += "{0}\n".format(str(vertex))
        return to_return

    @property
    def vertices(self):
        return self._vertices.values()

    def add_vertex(self, vertex):
        self._vertices[vertex.name] = vertex

    def parse(self, file):
        lines = file.readlines()
        if len(lines) < 2:
            raise IOException("Insufficient lines")
        number_of_vertices = int(lines[0])
        self._vertices = {}
        letter = 'A'
        line_number = 1
        for line in lines[1:]:
            try:
                self.parse_line(letter, line)
                # This is going to get weird if there are more than 26 vertices,
                # but the problem statement specifies that won't happen
                letter = next_letter(letter)
            except ValueError:
                print >> sys.stderr, "Improperly formatted line", line
            line_number += 1            # We can't use len(self._vertices) since new Vertices can get 
            # added and we risk underflow if we do that
            if (line_number > number_of_vertices):
                break


    def parse_line(self, name, line):
        lengths = [int(length) for length in line.split(',')]
        if not self._vertices.has_key(name):
            self.add_vertex(Vertex(name))
        letter = 'A'
        for length in lengths:
            if length != -1:
                if self._vertices.has_key(letter):
                # This vertex has already been added, create an edge between them
                # We'll just assume the length matrix is well-formed
                    edge = UndirectedEdge(length,
                                          self._vertices[name], 
                                          self._vertices[letter])
                    self._vertices[name].add_edge(edge)
                    self._vertices[letter].add_edge(edge)
            letter = next_letter(letter)

