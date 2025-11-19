

def simple_add(a, b):
    return a + b; 

def static_loop_self_multiplication(a):
    for _ in range(3):
        a = a*a
    return a

def two_functions(a, b):
    d = simple_add(a, b)
    result = loop_self_multiplication(d) 
    return result

def test_simple_add():
    output, ir = trace_function(simple_add, 0.3, 4)
    """
    the expected is: 
    {
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
    """
    assert str(ir["inputs"]) == str(["%0: float(0.3)", "%1: int(4)"])
    assert str(ir["body"]) == str(['%2: add:(%0,%1)'])
    assert str(ir["outputs"]) == str(['%2'])

def test_static_loop_self_multiplication():
    output, ir = trace_function(static_loop_self_multiplication, 2)
    """
    the expected IR isL 
        {
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
    """
    assert str(ir["inputs"]) == str(["'%0: int(2)'"])
    assert str(ir["body"]) == str(["%1: mul:(%0,%0)", "%2: mul:(%1,%1)", "%3: mul:(%2,%2)"])
    assert str(ir["outputs"]) == str(['%3'])

def test_two_functions():
    output, ir = trace_function(two_functions, 3, 5)
    """
    the expected IR is: 
    {
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
    """
    assert str(ir["inputs"]) == str(["'%0: int(3)'", "'%1: int(5)'"])
    assert str(ir["body"]) == str(["%2: add:(%0,%1)", "%3: mul:(%2,%2)", "%4: mul:(%3,%3)", "%5: mul:(%4,%4)"])
    assert str(ir["outputs"]) == str(['%5'])