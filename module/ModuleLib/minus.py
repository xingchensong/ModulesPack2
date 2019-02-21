from module import Module,ModuleDesc,InputDesc,OutputDesc
import numpy as np

class minus(Module):

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
        ret = {'y':x1-x2}
        return ret