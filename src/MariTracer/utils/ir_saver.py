import json

def maripr(tracer, outputs):
    data = {
        "inputs": [repr(a) for a in tracer.inputs],
        "body": [repr(node) for node in tracer.nodes],
        "outputs": None if outputs is None else [repr(o) for o in outputs],
    }
    return data

def print_IR(ir, indent=2):
    print(json.dumps(ir, indent= indent))