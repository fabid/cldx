import io

import networkx as nx
import pygraphviz as pgv
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import FancyArrow, Arc


class CausalLoopDiagram:
    def __init__(self):
        """
        Initializes an empty Causal Loop Diagram
        """
        self.graph = nx.DiGraph()

    def add_causal_links(self, links):
        """
        Add causal links from a list of links

        Parameters
        ----------
        links : list of (souce, target, gain) tuples, default None
            Sources and targets of the causal links.
            Sign of the gain defines if source and target move together or in opposite direction.
        """
        self.graph.add_edges_from(
            [(l[0], l[1], {'gain': l[2]}) for l in links])

    def to_graphviz(self):
        g = self.graph.copy()
        for e in g.edges:
            self._prepare_edge(g, e)
        gv = nx.nx_agraph.to_agraph(g)
        return gv

    def _prepare_edge(self, g, edge):
        edge_data = g.get_edge_data(edge[0], edge[1])
        if edge_data['gain'] > 0:
            edge_data['label'] = '+'
        else:
            edge_data['label'] = '-'
            edge_data['arrowhead'] = 'empty'

    def draw(self, filename=None, loops=[]):
        """
        Draw causal loop diagram.

        Parameters
        ----------
        filename : string, default None
            If specified, will output an image file. Recommended extension: png
        loops : list of loops, default []
            If specified, will draw markers for reinforcing and stabilizing loops.
            Note: this is beta and layout is not really good.
        """
        gv = self.to_graphviz()
        gv.layout(prog='dot')

        asdot = str(gv.draw(format='dot'))
        start = asdot.find('bb="')
        end = asdot.find('"];')
        size = [float(x) for x in asdot[start+4: end].split(',')[2:]]

        png = gv.draw(format='png')
        if filename:
            gv.draw(filename)

        tempBuff = io.BytesIO()
        tempBuff.write(png)
        tempBuff.seek(0)
        img = mpimg.imread(tempBuff)
        plt.figure(figsize=(12, 12))
        plt.imshow(img, interpolation="bicubic")
        imsize = [img.shape[1], img.shape[0]]
        for loop in loops:
            self._draw_loop(gv, loop, size, imsize)

    def _draw_loop(self, gv, loop, size, imsize):
        coords = [gv.get_node(n).attr['pos'].split(',') for n in loop['nodes']]
        x = np.mean([float(c[0]) for c in coords])
        y = np.mean([float(c[1]) for c in coords])
        x = x * imsize[0] / size[0]
        y = imsize[1] - y * imsize[1] / size[1]
        head = FancyArrow(x + 15, y, 0, -1, head_width=10, color="k")
        arrow = Arc((x, y), 30, 30, theta1=0, theta2=270)
        plt.gca().add_patch(arrow)
        plt.gca().add_patch(head)
        plt.text(x - 5, y + 4, loop['type'], fontsize=8)

    def _get_loop_type(self, loop):
        sign = np.product(
            [self.graph.get_edge_data(l, loop[(i + 1) % len(loop)])['gain']
             for i, l in enumerate(loop)])
        return 'R' if sign > 0 else 'S'

    def find_loops(self):
        """
        Find loops (cycles) in the causal loop diagram.
        It returns a list of loops described by a list of nodes and type.
        `R` for reinforcing or `S` for stabilizing
        """
        loops = nx.simple_cycles(self.graph)
        return [{'nodes': l, 'type': self._get_loop_type(l)} for l in loops]
