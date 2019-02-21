from module import Module,ModuleDesc,InputDesc,OutputDesc
import numpy as np

class add(Module):

    def __init__(self):
        pass

    @staticmethod
    def make_module_description():
        inputdesc = {'x1':InputDesc(datatype=np.float32,datashape=(None,)),
                     'x2':InputDesc(datatype=np.float32,datashape=(None,))}

        outputdesc = {'y':OutputDesc(datatype=np.float32,datashape=(None,))}

        MD = ModuleDesc(inputdesc,outputdesc)
        return MD

    @staticmethod
    def run(inputs):
        num1 = inputs['x1']
        num2 = inputs['x2']
        ret = {'y':num1+num2}
        return ret