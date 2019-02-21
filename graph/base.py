import networkx as nx
import matplotlib.pyplot as plt
import json

__all__ = ['ModuleGraph']

class ModuleGraph(nx.DiGraph):
    """
    Read Json file and transform it to graph.
    """
    def __init__(self,JsonFile=None,**attr):
        assert JsonFile is not None
        graphdata = json.load(fp = open(JsonFile,'r'))
        tempGraph = nx.DiGraph()

        for i in range(graphdata['version']['nodeNum']):
            currentNodeName = graphdata['node'][i]['name']
            # print(graphdata['node'][i])
            tempGraph.add_node(currentNodeName, attr=graphdata['node'][i])

        for i in range(graphdata['version']['nodeNum']):
            if 'startNode' in  graphdata['node'][i]:
                continue
            currentNodeName = graphdata['node'][i]['name']
            outerNodes = graphdata['node'][i]['input'].values()
            for node in outerNodes:
                tempGraph.add_edge( node.split('/',1)[0] , currentNodeName
                                    , data=graphdata['node'][i]['input'] )

        super().__init__(incoming_graph_data=tempGraph)

    def ShowGraph(self):
        nx.draw_spring(self, with_labels=True)
        plt.title('moduleGraph')
        plt.axis('on')
        plt.xticks([])
        plt.yticks([])
        plt.show()
