#! /usr/bin/python

import argparse, sys
from graph import Graph
from visit_edge_solver import VisitEdgeSolver

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculate the shortest path through a graph.')

    parser.add_argument('-i', '--input', action='store', default=None, dest='input', help='Input file to use.  If not provided, uses stdin.')
    parser.add_argument('-o', '--output', action='store', default=None, dest='output', help='Output file to use.  If not provided, uses stdin.')

    args = parser.parse_args()

    with (open(args.input) if args.input is not None else sys.stdin) as infile:
        with (open(args.output, 'w') if args.output is not None else sys.stdout) as outfile:
            graph = Graph()
            graph.parse(infile)
            solution = VisitEdgeSolver.solve(graph)
            if isinstance(solution, str):
                outfile.write("{0}\n".format(solution))
            else:
                outfile.write("{0} {1}\n".format(solution[0].name, solution[1].name))
