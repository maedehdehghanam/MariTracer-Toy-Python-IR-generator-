class IR_Node: 
    def __init__(self, op, inputs, variable):
        self.op = op
        self.inputs = inputs
        self.variable = variable
        
    #define the string representation 
    def __repr__(self):
        #we may have a lsit of inputs
        return f"%{self.variable}: {self.op}:({','.join(map(str, self.inputs))})"