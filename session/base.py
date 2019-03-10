# -*- coding: utf-8 -*-
# File: base.py

import sys,os
from abc import abstractmethod, ABCMeta

from module import (Module, Modules)
from utils import mylogger as logger
import networkx as nx

from module.ModuleLib import *

__all__ = ['Stop','Session']

class Stop(Exception):
    """
    An exception thrown to stop running graph.
    """
    pass

class SessionInterface(object):
  """Base class for implementations of client sessions."""

  @staticmethod
  def sess_id():
    """The process in which this session will run."""
    raise NotImplementedError('sess_str')

  @staticmethod
  def run(fetches,ModuleTable,graph,feed_dict=None):
    """Run modules in the session. See `BaseSession.run()` for details."""
    raise NotImplementedError('run')

class BaseSession(SessionInterface):
    """A class for ModulesGraph to interact with a background computation.

      The BaseSession enables execution of Modules and
      manages imperative information when running the graph.
    """

    def __init__(self, ModuleLibPath=None):
        """Constructs a new TensorFlow session.

        Args:
          ModuleLibPath: (Optional) used to find defined modules.

        Raises:
          Stop: Or one of its subclasses if an error occurs while
            creating the session.
        """

        if ModuleLibPath is not None:
            #TODO : 是否需要将ModuleLibPath封装成Config？
            sys.path.append(ModuleLibPath)
        else:
            raise Stop('ModuleLibPath must be specified')
        super().__init__()


    @staticmethod
    def build_graph(graph):
        """
        Instantiate Modules used in graph and fill the ModuleTable.

        Args:
          graph: A instance of class:ModuleGraph.

        Returns:
          ModuleTable: it holds all information of modules(nodes) and relations(edges) between them.
          toposort: Topological sorting of the graph, it's a list-like object

        Raises:
          Stop: Or one of its subclasses if an error occurs while building the graph.
          TypeError: If modules are of an inappropriate type.
        """

        # instantiation
        nodes = graph.nodes
        modules = []
        for node_name in nodes:
            module_name = graph.node[node_name]['attr']['module']
            # Dynamic import
            p = __import__(module_name, globals(), locals(), level=0)
            globals()[module_name] = p.__dict__[module_name]
            modules.append(eval(module_name+'()'))

        # check type
        def _Check_Module( md):
            """
            Check Modules which will be registered to ModuleTable.

            Args:
                md (Module or [Module]): a Module or a list of Modules

            Returns:
                succeed or not
            """
            if isinstance(md, (list, tuple)):
                for x in md:
                    _Check_Module(x)
                return
            assert isinstance(md, Module), md
            assert not isinstance(modules, Modules), \
                "Cannot append more Modules after BaseSession was setup!"
            return True

        Check_Module = _Check_Module

        for md in modules:
            Check_Module(md)

        # register to ModuleTable
        logger.logger.info("Build graph ...")

        ModuleTable = {'node_name':
                           {'module_name':None,'module_instance':None,'module_desc':None,'output':None}
                       }
        for index,node_name in enumerate(nodes):
            logger.logger.info('Register ' + node_name + ' to session')
            ModuleTable[node_name] = {'module_name':graph.node[node_name]['attr']['module'],
                                      'module_instance':modules[index],
                                      'module_desc':modules[index].make_module_description(),
                                      'output':None}

        toposort = list(nx.topological_sort(graph))

        return ModuleTable,toposort

    @staticmethod
    def run(fetches,ModuleTable,graph,feed_dict=None):
        """
        Runs operations and evaluates modules in `fetches`.

        This method runs full "step" of graph computation, by
        running the necessary graph fragment to execute every `Node`
        in `fetches`, substituting the values in
        `feed_dict` for the corresponding start-nodes in Topology graph.

        The `fetches` must be a single graph's topological sorted list ,
        and this method will sequentially execute the nodes in the list.

        Args:
          fetches: A single graph's topological sorted list
          feed_dict: A dictionary that maps node-input to values (only for start-node).
          ModuleTable: A multilevel dictionary that holds all information for running the graph

        Returns:
          final_output: outputs of the end-node in the graph

        Raises:
          Stop: If this `Session` is in an invalid state (e.g. has been
            closed).
          TypeError: If `fetches` or `feed_dict` keys are of an inappropriate type.
        """

        def CheckDesc(current_node_name,current_input_name,pre_node_name,pre_output_name):
            """
            Check the module description of the edge's two ends.

            Args:
              current_node_name: right node of the edge.
              current_input_name: input name of right node.
              pre_node_name: left node of the edge.
              pre_output_name: output name of left node.

            Raises:
              Stop: If there is a desc-mismatch.
            """

            current_input_desc = ModuleTable[current_node_name]['module_desc'].get_inputs_desc()[current_input_name]
            pre_output_desc = ModuleTable[pre_node_name]['module_desc'].get_outputs_desc()[pre_output_name]
            if not current_input_desc == pre_output_desc :
                raise Stop('there is a desc-mismatch when data flow from '
                           '%s to %s, go to check their definitions in modules' % (str(current_node_name),str(pre_node_name)))

        toposort = fetches
        final_output = None

        logger.logger.info("Begin Running Modules Graph ...")

        for node_name in toposort:
            logger.logger.info('Run ' + node_name)
            # Generate inputs for current node
            if  'startNode' in graph.node[node_name]['attr']:
                if not isinstance(feed_dict[node_name], dict):
                    raise Stop('feed_dict must be a dict-like object')
                inputs = feed_dict[node_name]
            else:
                inputs = graph.node[node_name]['attr']['input']
                for key,value in inputs.items():
                    # The initial value that can be specified in graph.json
                    if type(value).__name__ == 'dict':
                        for inner_key,inner_value in value.items():
                            inputs[inner_key] = inner_value
                    # The initial value that must be obtained by running the previous node
                    else:
                        pre_node_name = value.split('/',1)[0]
                        pre_output_name = value.split('/')[-1]
                        CheckDesc(current_node_name=node_name, current_input_name=key,
                                  pre_node_name=pre_node_name, pre_output_name=pre_output_name)
                        inputs[key] = ModuleTable[pre_node_name]['output'][pre_output_name]

            # run node
            output = ModuleTable[node_name]['module_instance'].run(inputs)
            if not isinstance(output,dict):
                raise Stop('output of node %s must be a dict-like object' % str(node_name))
            final_output = output
            print(final_output)

            # Fill in 'output' item of the current node in ModuleTable
            ModuleTable[node_name]['output'] = output

        return final_output


    # def __new__(cls, *args, **kwargs):
    #     if (len(args) > 0 and isinstance(args[0], Config)) \
    #             or 'config' in kwargs:
    #         logger.logger.error("Use interface API to launch controller ,do not pass Config directly to a controller!")
    #         import sys
    #         sys.exit(1)
    #     else:
    #         return super(BaseSession, cls).__new__(cls)

class Session(BaseSession):

    def __init__(self,ModuleLibPath=None):
        super().__init__(ModuleLibPath)

    @staticmethod
    def sess_id():
        """Return current-process id and father-process id"""
        return os.getpid(), os.getppid()




