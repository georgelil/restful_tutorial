"""
Now we're getting to concepts i'm aware of, 
but haven't had much use with.

"""

import functools

def my_decorator(func):
    @functools.wraps(func)
    def function_that_runs_func():
        print("before decorator")
        func()
        print("after function")
    return function_that_runs_func


@my_decorator
def my_function():
    print("the function")


#my_function()

def decorator_with_arguments(number):
    def my_decorator(func):
        @functools.wraps(func)
        def function_that_runs_func(*args, **kwargs):
            print('{} before decorator'.format(number))
            func(*args, **kwargs)
            print('fin')
        return function_that_runs_func
    return my_decorator

@decorator_with_arguments(100)
def my_function_too(x, y):
    print("Hellow!")
    print('{0}, {1}'.format(x, y))

my_function_too(9, 8)