import os
import weakref

from graph.base import ModuleGraph

BaseDir = os.path.dirname(__file__)
_graph_cache = weakref.WeakValueDictionary()
# 刚开始用成了WeakKeyDictionary 结果报错 TypeError: cannot create weak reference to 'str' object

# https://python3-cookbook.readthedocs.io/zh_CN/latest/c08/p25_creating_cached_instances.html
# https://www.jianshu.com/p/0cecea85ae3b
def get_graph(name):
    if name in _graph_cache.keys():
        g = _graph_cache[name]
    else:
        graph_path = os.path.join(BaseDir,name+'.json')
        g = ModuleGraph(JsonFile=graph_path)
        _graph_cache[name] = g
    return g

