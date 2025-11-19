class IR_Node: 
    def __init__(self, op, inputs, variable):
        self.op = op
        self.inputs = inputs
        self.variable = variable
        
    def __repr__(self):
        return f"%{self.variable}: {self.op}:({','.join(map(str, self.inputs))})"