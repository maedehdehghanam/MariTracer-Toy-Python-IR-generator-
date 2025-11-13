import sys

class IR_Node: 
    def __init__(self, op, inputs):
        self.op = op
        self.inputs = inputs
        
    #define the string representation 
    def __repr__(self):
        #we may have a lsit of inputs
        return f"{self.op}:({','.join(map(str, self.inputs))})"

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
    def __repr__(self):
        return f"{self.val}"
    
class Trace:
    def __init__(self):
        self.nodes = []
        
    def record_op(self, op, inputs):
        raw_inputs = [a.val if isinstance(a, Tracer) else a for a in inputs]
        node =  IR_Node(op, raw_inputs)
        self.nodes.append(node)
        return Tracer(f"{op}({','.join(map(str, raw_inputs))})", self)
         
    def tracing_args(self, val):
        return Tracer(val, self)


def trace_function(fn, *args):
    trace = Trace()
    traced_args =[trace.tracing_args(a) for a in args]
    output = fn(*traced_args)
    return output, trace.nodes    

def f(x, y):
    return x + (x * 5) + y 

out, trace = trace_function(f, 3.0, 5.0)

print("Output:", out)
print("IR:")
for node in trace:
    print(" ", node)
