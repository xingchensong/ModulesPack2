# -*- coding: utf-8 -*-
# File: module_desc.py

# namedtuple让tuple可以字典化
# 既可以通过tuple原有的下标访问数据也可以根据key访问数据（每个数据都有自己的key，数据本身作为value）
from collections import namedtuple
from utils import mylogger as logger
from utils.argtools import memoized_method

__all__ = ['InputDesc', 'OutputDesc', 'ModuleDesc']

def get_sublist_by_names(lst, names):
    """
    Args:
        lst (list): list of objects with "name" property.

    Returns:
        list: a sublist of objects, matching names
    """
    orig_names = [p.name for p in lst]
    ret = []
    for name in names:
        try:
            idx = orig_names.index(name)
        except ValueError:
            logger.logger.info("Name {} doesn't appear in lst {}!".format(
                name, str(orig_names)))
            raise
        ret.append(lst[idx])
    return ret


class InputDesc(namedtuple('InputDescTuple', ['datatype', 'datashape'])):
    """
    Metadata about an input entry point to the Module.
    It's a part of the Module Description.
    It can be later used to check whether the modules-pipeline can work properly.
    """

    def __new__(cls, datatype, datashape):
        """
        Args:
            datatype (): type of input data
            datashape (tuple): shape of input data , can be (None,) if you don't know concrete shape of your data

        Examples:
            inputdesc = {'x': InputDesc(datatype=np.float32,datashape=(None,)) }

            # if you have multi-inputs, then :
            inputdesc = {'x1': InputDesc(datatype=np.float32,datashape=(None,),name='x1'),
                        'x2': InputDesc(datatype=np.float32,datashape=(None,),name='x2') }
        """
        datashape = tuple(datashape)    # has to be tuple for "self" to be hashable
        # #TODO : check datatype here
        # if any(k in name for k in [':', '/', ' ']):
        #     raise ValueError("Invalid InputDesc name: '{}'".format(name))
        self = super(InputDesc, cls).__new__(cls, datatype, datashape)
        return self


class OutputDesc(namedtuple('OutputDescTuple', ['datatype', 'datashape'])):
    """
    Metadata about an output exit point to the Module.
    It's a part of the Module Description.
    It can be later used to check whether the modules-pipeline can work properly.
    """

    def __new__(cls, datatype, datashape):
        """
        Args:
            datatype (): type of output data
            datashape (tuple): shape of output data , can be (None,) if you don't know concrete shape of your data

        Examples:
            outputdesc = {'y': OutputDesc(datatype=np.float32,datashape=(None,),name='y') }

            # if you have multi-outputs, then :
            outputdesc = {'y1': OutputDesc(datatype=np.float32,datashape=(None,),name='y1'),
                          'y2': OutputDesc(datatype=np.float32,datashape=(None,),name='y2') }
        """
        datashape = tuple(datashape)    # has to be tuple for "self" to be hashable
        # # TODO : check datatype here
        # if any(k in name for k in [':', '/', ' ']):
        #     raise ValueError("Invalid OnputDesc name: '{}'".format(name))
        self = super(OutputDesc, cls).__new__(cls, datatype, datashape)
        return self


class ModuleDesc(object):
    """
    Base class for a module description.
    """

    def __init__(self,InputDesc,OutputDesc):
        assert InputDesc is not None,'InputDesc can\'t be None'
        assert OutputDesc is not None,'OutputDesc can\'t be None'

        self.inputDesc = InputDesc
        self.outputDesc = OutputDesc
        super().__init__()


    @memoized_method
    def get_inputs_desc(self):
        """
        Returns:
            A list of :class:`InputDesc`, which describes the inputs of this module.
            The result is cached for each instance of :class:`ModuleDescBase`.
        """
        try:
            ret = self.inputDesc
            return ret
        except AttributeError:
            logger.logger.info('Can\'t find InputDesc' )

    @memoized_method
    def get_outputs_desc(self):
        """
        Returns:
            A list of :class:`OutputDesc`, which describes the outputs of this module.
            The result is cached for each instance of :class:`ModuleDescBase`.
        """
        try:
            ret = self.outputDesc
            return ret
        except AttributeError:
            logger.logger.info('Can\'t find OutputDesc')

    @property
    def input_names(self):
        """
        Returns:
            [str]: the names of all the inputs.
        """
        return self.inputDesc.keys()

    @property
    def output_names(self):
        """
        Returns:
            [str]: the names of all the outputs.
        """
        return self.outputDesc.keys()

