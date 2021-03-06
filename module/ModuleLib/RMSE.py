from module import Module,ModuleDesc,InputDesc,OutputDesc
import numpy as np
from module.GraphLib import get_graph

graph = get_graph('RMSE_graph')
from session import Session
sess = Session(ModuleLibPath='D:\pycharm_proj\modulespack2\module\ModuleLib')
ModuleTable, toposort = sess.build_graph(graph)


class RMSE(Module):

    def __init__(self):
        pass

    @staticmethod
    def make_module_description():
        inputdesc = {'x1':InputDesc(datatype=np.float32, datashape=(None,)),
                     'x2':InputDesc(datatype=np.float32, datashape=(None,))}
        outputdesc = {'y':OutputDesc(datatype=np.float32, datashape=(None,))}
        MD = ModuleDesc(inputdesc, outputdesc)
        return MD

    @staticmethod
    def run(inputs):
        x1 = inputs['x1']
        x2 = inputs['x2']

        # graph = ModuleGraph(JsonFile='D:\pycharm_proj\modulespack2\module\ModuleLib\RMSE_graph.json')
        # graph = get_graph('RMSE_graph')
        # from session import Session
        # sess = Session(ModuleLibPath='D:\pycharm_proj\modulespack2\module\ModuleLib')
        # ModuleTable, toposort = sess.build_graph(graph)

        feed_dic = {'firstadd': {'x1': x1, 'x2': x2}}
        result = sess.run(fetches=toposort, ModuleTable=ModuleTable
                          , graph=graph, feed_dict=feed_dic)

        return result