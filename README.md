# MariTracer 

A minimal Python-based IR (Intermediate Representation) tracer that captures arithmetic operations, control flow (e.g., `for` loops), and function compositions in a simplified SSA-like format.

Inspired by projects like [JAX](https://github.com/google/jax) and `torch.fx`, MariTracer helps you visualize and reason about the structure of Python programs through operator tracing.

---

## Features

- 📌 **Operator Overloading:** Traces arithmetic expressions like `a + b`, `a * b`, etc.
- 🧩 **Function Composition:** Traces nested function calls.
- 🧠 **IR Generation:** Emits a simple human-readable IR as a Python dictionary with `inputs`, `body`, and `outputs`.
- 🌐 **Thread-safe:** support for parallel contexts using `contextvars`.
- 🔁 **Loop Tracing:** Supports dynamic/static `for` loops with custom `mari_for` control flow.
- to be continued :)! 

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/maedehdehghanam/MariTracer-Toy-Python-IR-generator-
cd MariTracer
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
