from MariTracer.core.threadsafe import *

"""
MARI LOOP: A traceable custom loop for MariTracer

Arguments:
- `body`: a function of the form `body(*args, index)` that returns new args for the next iteration.
- `*args`: initial values passed to `body`.
- `start`: start of the loop (can be an int or a Tracer).
- `end`: optional end of the loop (if omitted, loop runs from 0 to `start`).

The `body` function should follow this pattern:

    def body(..., index):
        return updated_args

Where `updated_args` is either a single value or a tuple of values.
These values are fed into the next iteration of the loop.

The final `args` from the last iteration are returned.
"""

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

