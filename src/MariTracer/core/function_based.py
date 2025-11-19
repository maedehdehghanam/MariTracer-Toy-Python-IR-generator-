import sys
import numpy as np
import json
from common import *
from MariTracer.utils.ir_saver import *

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
        self.inputs = []
        self.nodes = []
        self.counter = 0
        
    def record_op(self, op, inputs):
        raw_inputs = [a.val if isinstance(a, Tracer) else a for a in inputs]
        
        node =  IR_Node(op, raw_inputs, str(self.counter))
        self.counter += 1
        self.nodes.append(node)
        return Tracer(f"%{node.variable}", self)
         
    def tracing_args(self, val):
        self.inputs.append(f"%{self.counter}: {type(val).__name__}({val})")
        self.counter += 1
        return Tracer(f"%{self.counter-1}", self)
        
def trace_function(fn, *args):
    trace = Trace()
    traced_args =[trace.tracing_args(a) for a in args]
    output = fn(*traced_args)
    #maripr works with tuples
    if not isinstance(output, tuple):
        output = (output,)

    print("IR:")
    ir = maripr(trace, output)
    print_IR(ir)
    return output, ir   

def ch(b):
    mari_for(body,b, a=2)
def body(a, i):
    a = a + i
    return a

o, i = trace_function(ch, 4)
print(i)


