import sys
import numpy as np

class IR_Node: 
    def __init__(self, op, inputs, variable):
        self.op = op
        self.inputs = inputs
        self.variable = variable
        
    #define the string representation 
    def __repr__(self):
        #we may have a lsit of inputs
        return f"%{self.variable}: {self.op}:({','.join(map(str, self.inputs))})"

class Tracer:
    def __init__(self, val, trace):
        self.trace = trace
        self.val = val
    
    def __add__(self, operand2):
        return self.trace.record_op("add", [self.val, operand2])
    def __mul__(self, operand2):
        return self.trace.record_op("mul", [self.val, operand2])
    def __sub__(self, operand2):
        return self.trace.record_op("sub", [self.val, operand2])
    def __truediv__(self, operand2):
        return self.trace.record_op("div", [self.val, operand2])
    def __floordiv__(self, operand2):
        return self.trace.record_op("floor_div", [self.val, operand2])
    def __pow__(self, operand2):
        return self.trace.record_op("pow", [self.val, operand2])
    def __neg__(self, operand2):
        return self.trace.record_op("neg", [self.val, operand2])
    def __abs__(self, operand2):
        return self.trace.record_op("abs", [self.val, operand2])
    def __eq__(self, operand2):
        return self.trace.record_op("equal_check", [self.val, operand2])
    def __lt__(self, operand2):
        return self.trace.record_op("less_than_check", [self.val, operand2])
    
    #universal functions operate on ndarrays in an elemnetwise fashion 
    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        return self.trace.record_op(ufunc.__name__,[self.val, *inputs])
    
    
    def __repr__(self):
        return f"{self.val}"
    
class Trace:
    def __init__(self):
        self.nodes = []
        self.counter = 0
        
    def record_op(self, op, inputs):
        raw_inputs = [a.val if isinstance(a, Tracer) else a for a in inputs]
        
        node =  IR_Node(op, raw_inputs, str(self.counter))
        self.counter += 1
        self.nodes.append(node)
        return Tracer(f"%{node.variable}", self)
         
    def tracing_args(self, val):
        node =  IR_Node("assign", [val], str(self.counter))
        self.counter += 1
        self.nodes.append(node)
        return Tracer(f"%{node.variable}", self)

# rewrite the code in a format that val as nodes 
def trace_function(fn, *args):
    trace = Trace()
    traced_args =[trace.tracing_args(a) for a in args]
    output = fn(*traced_args)
    return output, trace.nodes    

def f(x, y):
    sum_man = 0
    for i in range(3):
        z = x**bar(x,y)
    x =x*2
    return z + y
def bar(a, b):
    return a - b
out, trace = trace_function(f, 3.0, 5.0)

#TODO: handle loops
#TODO: assign each node a variable 
'''
each node has its variable
this changing variable should be implemented in the trace. 
val should be an object rather than a string cause then we can check if its been seen or not.
'''
print("Output:", out)
print("IR:")
for node in trace:
    print(" ", node)
