from session import Session
from graph import ModuleGraph

graph = ModuleGraph(JsonFile='graph.json')
sess = Session()
feed_dic = {'firstadd':{'x1':1,'x2':2}}

ModuleTable,toposort = sess.build_graph(graph)
result =               sess.run(fetches=toposort,ModuleTable=ModuleTable
                                ,graph=graph,feed_dict=feed_dic)
graph.ShowGraph()