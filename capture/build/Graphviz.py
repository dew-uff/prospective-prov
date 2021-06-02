from graphviz import Digraph


class Graphviz:
    def __init__(self, trial):
        """
        :param trial: experiment id
        """
        self.trial = trial
        self._shape = 'box'
        self._size = '15'
        self._nodesep = '0.4'
        self._color = 'black'
        self._background = '#85CBC0'
        self._filename = 'trial{}'.format(self.trial)
        self._graph = Digraph(filename=self._filename, strict=True)

    def initialize(self):
        try:
            self._graph.attr(size=self._size, nodesep=self._nodesep)
            self._graph.node_attr.update(color=self._color,
                                         fillcolor=self._background,
                                         style='filled',
                                         shape=self._shape,
                                        )
            return self._graph
        except SystemError:
            print('Error creating the graph! '
                  'You may not have the GraphViz library!')
            return None
        finally:
            print('Starting ProspectiveProv!')
