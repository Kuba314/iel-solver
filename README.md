IEL solver
===

A wrapper around all your task solving functions.

Example usage
---
```bash
python3 iel_solver.py -p me         # (define your preset inside the script first)
python3 iel_solver.py -p me -t 1-3  # solve for your preset, but only first 3 tasks
python3 iel_solver.py FCDGA         # solve the tasks for those letters
python3 iel_solver.py C -t 3        # solve third task of group C
```

How to write code in python
---
Python is a dynamically typed language, meaning there is not `int` when declaring a variable
```python
x = 5       # store int 5 in x
y = 4       # store int 4 in y
z = x * y   # store x * y in z
a = 'asd'   # string, you can use `'` or `"`, it doesn't matter
x = 'asd'   # you can even change a variable type, you can really do anything

b = 5 ** 2  # exponentiation (5 to the power of 2)
```
This is how you print stuff
```python
a = 5
print(a)        # prints "5"
print('asd')    # prints "asd"
print('number a is:', a)    # prints "number a is: 5"

# format string example
# documentation can be found if you search for "python f string"
print(f'This is a format string, value of a is {a}, number one lower is {a-1}')
```
This is how you define and call a function
```python
def my_function(arg1, arg2):
    arg3 = arg1 + arg2 ** 3
    return arg3 + 2 * arg1

# this is how you might call a function
my_function(1, 2)
```

Now for some useful stuff that you might need in this project.

Working with the math library
```python
import math     # imports the math package

math.pi         # 3.14159265...
math.atan()     # arc tan function
```

Working with complex numbers
```python
a = complex(1, 2)   # 1 + 2j
b = complex(3, 1)   # 3 + j
c = a + b           # 4 + 3j, yes, it's that easy
d = a * b
size = abs(c)       # (4 ** 2 + 3 ** 2) ** 0.5 = 5 (gets the size of the vector)
```

I left you a few useful functions inside. Namely `par`, which calculates parallel resistors and `solve_cramer_3`, which solves a 3*3 array for you.
```python
# this is how you use the cramer function
def get_3(u, i1, i2, r1, r2, r3, r4, r5):
    matrix = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 8]
    ]
    final_vector = [4, 4, 2]
    
    # btw the return value is a tuple of the three values that you want. tuple is basically a C array
    solution = solve_cramer_3(matrix, final_vector)
```
