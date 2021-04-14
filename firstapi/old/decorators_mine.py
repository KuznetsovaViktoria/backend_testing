from time import *
import functools

# 1 problem

def upper_print(func):
    def wrapper(*args, **kwargs):
        func(*[i.upper() if type(i) == str else i for i in args], **kwargs)
    return wrapper


print = upper_print(print)
print('fdjgfdGSAHFDX')

# 2 problem


def decorator_time(func):
    global count
    count = 0
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        global count
        t1 = time()
        if count == 0:
            count += 1
            a = func(*args, **kwargs)
        t2 = time()
        print(t2 - t1)
        return a
    return wrapper

@decorator_time
def some_func():
    sleep(2)
    print("some_func is done, now you'll see its time")
    return 0

some_func()

# 3, 4 problem

def check_password():
    global c
    c = 0
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            global c
            if c == 0:
                c += 1
                print('type password:')
                p = input()
                if p == correct_password:
                    return func(*args, **kwargs)
                print('access denied')
                return None
            return func(*args, **kwargs)
        return wrapper
    return decorator

@check_password()
def fibonachi(n):
    if n > 2:
        return fibonachi(n-1) + fibonachi(n-2)
    return 1

print('set password for function fibonachi:')
correct_password = input()
print(fibonachi(30))


# 5 problem

def cached(func):
    cache = {}
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = tuple(args) + tuple(kwargs)
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    return wrapper

@cached
def fibonachi1(n):
    if n > 2:
        return fibonachi1(n-1) + fibonachi1(n-2)
    return 1

print(fibonachi1(35))