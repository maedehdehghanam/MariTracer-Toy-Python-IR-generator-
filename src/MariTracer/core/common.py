class IR_Node: 
    def __init__(self, op, inputs, variable):
        self.op = op
        self.inputs = inputs
        self.variable = variable
        
    def __repr__(self):
        return f"%{self.variable}: {self.op}:({','.join(map(str, self.inputs))})"
    
def mari_for(body, *args, a, b=None):
    if b is not None:
        for i in range(a, b):
            result = body(*args, i)
            if not isinstance(result,tuple):
                result = (result, )
            args = result
    else:
        for i in range(a):
            result = body(*args, i)
            if not isinstance(result,tuple):
                result = (result, )
            args = result
    return args