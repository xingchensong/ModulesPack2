# -*- coding: utf-8 -*-
# File: base.py

from abc import ABCMeta
import six

__all__ = ['Module', 'ProxyModule', 'ModuleFactory']

# TODO : write help_doc in  http://xx.html
@six.add_metaclass(ABCMeta)
class Module(object):
    """ Base class for all Modules. See
    `Write a Module
    <http://xx.html>`_
    for more detailed explanation of the module methods.
    """

    @staticmethod
    def make_module_description():
        """
        Override this method to setup the descriptions of the Module.

        Note : The return value must be a instance of ModuleDesc.

        Examples:
            def make_module_description(self):
                inputdesc = InputDesc(datatype=np.float32,datashape=(None,),name='x')
                outputdesc = OutputDesc(datatype=np.float32,datashape=(None,),name='y')
                desc = ModuleDesc(inputdesc,outputdesc)
                return desc
        """
        raise NotImplementedError('you must override function _make_module_description() in your subclass and return instance of ModuleDesc')


    @staticmethod
    def run(inputs):
        """
        Override this method to implement the functionality that this module should have.

        Note :
            Inputs is something like a dict, the keys and values in inputs must be the same as they are defined in inputdesc.
            The return value must be something like a dict too. k&v of outputs should also meet the definition(in outputdesc)!

        Args:
            inputs : A dict-like object

        Returns:
            outputs : A dict-like object

        Examples:
            class new_module(Module):

                def _make_module_description(self):
                    inputdesc = {'x1':InputDesc(datatype=np.float32,datashape=(None,),name='x1'),
                                'x2':InputDesc(datatype=np.float32,datashape=(None,),name='x2')}
                    outputdesc = {'y1':OutputDesc(datatype=np.float32,datashape=(None,),name='y1'),
                                'y2':OutputDesc(datatype=np.float32,datashape=(None,),name='y2')}
                    desc = ModuleDesc(inputdesc,outputdesc)
                    return desc

                def _run(inputs):
                    x1 = inputs['x1']
                    x2 = inputs['x2']
                    y1 = x2
                    y2 = x1
                    outputs = {'y1':y1,'y2',y2}
                    return outputs
                    # Error example: return y2,y1  . you should integrate them(y1,y2) into a dictionary!#
        """
        raise NotImplementedError('you must override function run() in your subclass')


    def __str__(self):
        return type(self).__name__

    @property
    def name(self):
        return self.__class__.__name__


class ProxyModule(Module):
    """ A Module which proxy all methods to another Module.
        It's useful as a base class of Modules which decorate other Modules.
    """
    def __init__(self, cb,*args,**kwargs):
        """
        Args:
            cb(Module): the underlying Module
        """
        assert isinstance(cb, Module), type(cb)
        self.cb = cb
        #TODO 对多余参数的处理

    def __str__(self):
        return "Proxy-" + str(self.cb)


class ModuleFactory(Module):
    """
    Create a Module with some lambdas.
    """
    def __init__(self, make_module_description=None, run=None):
        """
        Each lambda takes ``self`` as the only argument.
        """

        self._cb_make_module_description = make_module_description
        self._cb_run = run

    def make_module_description(self):
        if self._cb_make_module_description:
            return self._cb_make_module_description(self)

    def run(self,inputs):
        if self._cb_run:
            return self._cb_run(inputs)

