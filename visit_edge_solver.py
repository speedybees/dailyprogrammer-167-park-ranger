import copy

class VisitEdgeSolver(object):
    @staticmethod
    def solve(graph):
        odd_vertices = set([vertex for vertex in graph.vertices 
                           if len(vertex.edges) % 2 == 1])
        if len(odd_vertices) == 0:
            return "Any"
        elif len(odd_vertices) != 2:
            # We'd have to backtrack across any odd nodes

            # It will be necessary to backtrack.  We'll want to backtrack on 
            # whichever vertices have the shortest connecting path, so keep 
            # stapling onto graph until we're down to two odd vertices
            graph_copy = copy.deepcopy(graph)
            # Since the references will have all been duplicated, have to 
            # create a new one of these
            odd_vertices = set([vertex for vertex in graph_copy.vertices 
                                if len(vertex.edges) % 2 == 1])
            while (len(odd_vertices) > 2):
                edges = [edge for sublist in 
                              [vertex.edges for vertex in odd_vertices]
                              for edge in sublist]
                # Edges where both vertices in odd sets are effectively
                # twice as valuable because they change the valence
                # favorably for two sets, whereas edges with one vertex
                # not in odd_vertices means that now we have a new odd
                # vertex.  However, if a path is long enough, we don't
                # get a break by backtracking it, even though using it
                # would only change the valence by 1
                shortest_edge = min(edges, 
                                    key=lambda edge: edge.length
                                                     /len([vertex 
                                                           for vertex 
                                                           in odd_vertices]))
                # We don't want to use this edge again, pretend like it 
                # doesn't exist any more
                for vertex in shortest_edge.vertices:
                    vertex.remove_edge(shortest_edge)
                    if ((len(vertex.edges) % 2) == 0):
                        odd_vertices.discard(vertex)
                    else:
                        odd_vertices.add(vertex)
        return list(odd_vertices)
