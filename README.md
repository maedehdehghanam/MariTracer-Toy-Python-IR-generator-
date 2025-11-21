# MariTracer 

A minimal Python-based IR (Intermediate Representation) tracer that captures arithmetic operations, control flow (e.g., `for` loops), and function compositions in a simplified SSA-like format.

Inspired by projects like [JAX](https://github.com/google/jax) and `torch.fx`, MariTracer helps you visualize and reason about the structure of Python programs through operator tracing.

---

## Features

- **Operator Overloading:** Traces arithmetic expressions like `a + b`, `a * b`, etc.
- **Function Composition:** Traces nested function calls.
- **IR Generation:** Emits a simple human-readable IR as a Python dictionary with `inputs`, `body`, and `outputs`.
- **Thread-safe:** support for parallel contexts using `contextvars`.
- **Loop Tracing:** Supports dynamic/static `for` loops with custom `mari_for` control flow.
- to be continued :)! 

---
## 1. Custom primitves
MariTracer has it's own primitive to trace input objects. 
# Example: 
## 🔁 Example: Tracing a Loop with `mari_for`:

`mari_for` is a loop primitive that allows MariTracer to trace repeated computations even when Python’s `for` loop cannot operate directly on `Tracer` objects.

Below is an example showing how a regular loop can be replaced with `mari_for` for proper tracing:

```python
"""
Original Python function (not traceable):

def my_func(num, s):
    # computes: num * s * (s+1) * ... * 5
    for i in range(s, 6):
        num = num * i
    return np.log(num)
"""
```
With mari_for, we rewrite the loop in a traceable form:
```
def my_func(num, s):
    # Performs: num * s * (s+1) * ... * 5
    for_result, = mari_for(body, num, start=s, end=6)
    return np.log(for_result)

def body(num, index):
    return num * index

output, mariPR =  trace_function(my_func, 10, 3)
```
This will produce an IR:
```
inputs:
  %0: int(10)
  %1: int(3)
body:
  %2: mul:(%0,3)
  %3: mul:(%2,4)
  %4: mul:(%3,5)
outputs:
  %4
```
## 2. Supports multithread tracing
each thread has its own independent trace without interfering with others.
```
import threading
from MariTracer import trace_function

"""
Spawns 5 threads.

Each thread runs trace_function(compute, a, b) with its own inputs.
"""
def compute(a, b):
    return a * b + 3

def thread_job(id, a, b):
    print(f"[Thread {id}] Starting")
    output, ir = trace_function(compute, a, b)
    print(f"[Thread {id}] Output: {output}")
    print(f"[Thread {id}] IR:")
    print(ir)
    print("-" * 40)

threads = []
for i in range(5):
    t = threading.Thread(target=thread_job, args=(i, i + 1, i + 2))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

```
---
## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/maedehdehghanam/MariTracer-Toy-Python-IR-generator-
cd MariTracer-Toy-Python-IR-generator-
```
### 2. Set up your enviorment
```
conda create -n maritracer python=3.10
conda activate maritracer
pip install -r requirements.txt
```
### 3. Install MariTracer
```
pip install -e .
```

### 4. Import MariTracer and use it:)

```
from MariTracer import trace_function

def add(a, b):
    return a + b

output, ir = trace_function(add, 1, 2)
print(output)

```
### (optional) run tests
```
pytest -v -s tests/test_simple.py
```
