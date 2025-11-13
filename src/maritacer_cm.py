import sys
import numpy as np
import json
from utils.common import * 
import contextvars
current_trace =  contextvars.ContextVar('current_trace')

class Tracer:
    def __init__(self, val):
        self.val = val
    
    def __add__(self, operand2):
        return current_trace.get().record_op("add", [self.val, operand2])
    def __mul__(self, operand2):
        return current_trace.get().record_op("mul", [self.val, operand2])
    def __sub__(self, operand2):
        return current_trace.get().record_op("sub", [self.val, operand2])
    def __truediv__(self, operand2):
        return current_trace.get().record_op("div", [self.val, operand2])
    def __floordiv__(self, operand2):
        return current_trace.get().record_op("floor_div", [self.val, operand2])
    def __pow__(self, operand2):
        return current_trace.get().record_op("pow", [self.val, operand2])
    def __neg__(self, operand2):
        return current_trace.get().record_op("neg", [self.val, operand2])
    def __abs__(self, operand2):
        return current_trace.get().record_op("abs", [self.val, operand2])
    def __eq__(self, operand2):
        return current_trace.get().record_op("equal_check", [self.val, operand2])
    def __lt__(self, operand2):
        return current_trace.get().record_op("less_than_check", [self.val, operand2])
    
    #universal functions operate on ndarrays in an elemnetwise fashion 
    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        return self.trace.record_op(ufunc.__name__,[self.val, *inputs])
    
    
    def __repr__(self):
        return f"{self.val}"
    
class Trace:
    def __init__(self):
        self.inputs = []
        self.nodes = []
        self.counter = 0
    
    def __enter__(self):
        self.token = current_trace.set(self)
        return self
    def __exit__(self, exec_type, exec_value, traceback):
        current_trace.reset(self.token)
            
    def record_op(self, op, inputs):
        raw_inputs = [a.val if isinstance(a, Tracer) else a for a in inputs]
        
        node =  IR_Node(op, raw_inputs, str(self.counter))
        self.counter += 1
        self.nodes.append(node)
        return Tracer(f"%{node.variable}")
         
    def tracing_args(self, val):
        self.inputs.append(f"%{self.counter}: {type(val).__name__}({val})")
        self.counter += 1
        return Tracer(f"%{self.counter-1}")
        

def maripr(tracer, outputs):
    data = {
        "inputs": [repr(a) for a in tracer.inputs],
        "body": [repr(node) for node in tracer.nodes],
        "outputs": None if outputs is None else [repr(o) for o in outputs],
    }

    print(json.dumps(data, indent=2))
    return data

def trace_function(fn, *args):
    with Trace() as trace:
        traced_args =[trace.tracing_args(a) for a in args]
        output = fn(*traced_args)
        print("IR:")
        maripr(trace, output)
    return output, trace.nodes    

def f(x, y):
    sum_man = 0
    for i in range(3):
        z = x**bar(x,y)
    x =x*2
    return z + y, x**2
def bar(a, b):
    return a - b

out, trace = trace_function(f, 3.0, 5.0)
print(trace)

