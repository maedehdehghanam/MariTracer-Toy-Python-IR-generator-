from MariTracer.core.threadsafe import *
from MariTracer.core.mari_lang import *

def simple_add(a, b):
    return a + b; 

def static_loop_self_multiplication(a):
    for _ in range(3):
        a = a*a
    return a

def two_functions(a, b):
    d = simple_add(a, b)
    result = static_loop_self_multiplication(d) 
    return result

def dynamic_for(num, s):
    result = mari_for(body, num, start=s, end = 6)
    return result

def body(num, index):
    return num*index

def test_dynamic_for():
    output, ir = trace_function(dynamic_for, 10, 3)
    """
    # num * 3 * 4 * 5 
    for i in range(start,6)
        num = num * i 
    """
    
    expected_ir = {
        "inputs": [
            "'%0: int(10)'", #num
            "'%1: int(3)'"  #start_range 
        ],
        "body": [
            "%2: mul:(%0,3)",
            "%3: mul:(%2,4)",
            "%4: mul:(%3,5)"
        ],
        "outputs": [
            "%4"
        ]
    }
    assert ir == expected_ir
   
    
def test_simple_add():
    output, ir = trace_function(simple_add, 0.3, 4)
    
    expected_ir = {
        "inputs": [
            "'%0: float(0.3)'",
            "'%1: int(4)'"
        ],
        "body": [
            "%2: add:(%0,%1)"
        ],
        "outputs": [
            "%2"
        ]
    }
    
    assert expected_ir == ir
def test_static_loop_self_multiplication():
    output, ir = trace_function(static_loop_self_multiplication, 2)
    
    #the expected IR isL 
    expected_ir = {
            "inputs": [
                "'%0: int(2)'"
            ],
            "body": [
                "%1: mul:(%0,%0)",
                "%2: mul:(%1,%1)",
                "%3: mul:(%2,%2)"
            ],
            "outputs": [
                "%3"
            ]
        }
    assert expected_ir  == ir

def test_two_functions():
    output, ir = trace_function(two_functions, 3, 5)
    
    expected_ir ={
        "inputs": [
            "'%0: int(3)'",
            "'%1: int(5)'"
        ],
        "body": [
            "%2: add:(%0,%1)",
            "%3: mul:(%2,%2)",
            "%4: mul:(%3,%3)",
            "%5: mul:(%4,%4)"
        ],
        "outputs": [
            "%5"
        ]
    }
    
    assert (ir) == expected_ir