from MariTracer.core.threadsafe import *
def mari_for(body, *args, start, end=None):
    if isinstance(start, Tracer):
        start = int(start.value)

    if isinstance(end, Tracer):
        end = int(end.value)
        
    if end is not None:
        for i in range(start, end):
            result = body(*args, i)
            if not isinstance(result,tuple):
                result = (result, )
            args = result
    else:
        for i in range(start):
            result = body(*args, i)
            if not isinstance(result,tuple):
                result = (result, )
            args = result
    return args

def dynamic_for(num, s):
    result = mari_for(body, num, start=s, end = 6)
    return result

def body(num, index):
    return num*index
o, i = trace_function(dynamic_for,5,3)
print(i)
