import sys
import numpy as np
import json
from  MariTracer.core.common import * 
from MariTracer.utils.ir_saver import *
import contextvars

current_trace =  contextvars.ContextVar('current_trace')

class Tracer:
    def __init__(self, val, value):
        self.val = val
        self.value = value
    
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
        return Tracer(f"%{node.variable}", None)
         
    def tracing_args(self, value):
        self.inputs.append(f"%{self.counter}: {type(value).__name__}({value})")
        self.counter += 1
        return Tracer(f"%{self.counter-1}", value)
        
        
def trace_function(fn, *args):
    with Trace() as trace:
        traced_args =[trace.tracing_args(a) for a in args]
        output = fn(*traced_args)
        ir = maripr(trace, output)
        print_IR(ir)
    return output, ir    


