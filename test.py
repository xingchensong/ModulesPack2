import time
beg = time.time()
from session import Session
from graph import ModuleGraph

graph = ModuleGraph(JsonFile='graph.json')
sess = Session(ModuleLibPath='D:\pycharm_proj\modulespack2\module\ModuleLib')
feed_dic = {'RMSE':{'x1':1,'x2':2}}

ModuleTable,toposort = sess.build_graph(graph)
result =               sess.run(fetches=toposort,ModuleTable=ModuleTable
                                ,graph=graph,feed_dict=feed_dic)
print(time.time()-beg)
# graph.ShowGraph()