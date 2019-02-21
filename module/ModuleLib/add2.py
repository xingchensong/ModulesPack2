from module import Module,ModuleDesc,InputDesc,OutputDesc
import numpy as np

class add2(Module):

    def __init__(self):
        pass

    @staticmethod
    def make_module_description():
        inputdesc = {'x':InputDesc(datatype=np.float32,datashape=(None,))}

        outputdesc = {'y':OutputDesc(datatype=np.float32,datashape=(None,))}

        MD = ModuleDesc(inputdesc,outputdesc)
        return MD

    @staticmethod
    def _run(inputs):
        num = inputs['x']
        ret = {'y':num+2}
        # print('add_')
        return ret