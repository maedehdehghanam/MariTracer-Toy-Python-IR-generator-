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
            body(*args, i)
    else:
        for i in range(a):
            body(*args, i)
