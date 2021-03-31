from time import *
import functools

# 1 problem

p = print
p = lambda x: print(x.upper())
p('fdjgfdGSAHFDX')

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
            func(*args, **kwargs)
        t2 = time()
        print(t2 - t1)

    return wrapper

@decorator_time
def some_func():
    sleep(2)
    print("some_func is done, now you'll see its time")

some_func()

# 3, 4 problem

def check_password(password):
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
                if p == password:
                    return func(*args, **kwargs)
                print('access denied')
                return None
            return func(*args, **kwargs)
        return wrapper
    return decorator

@check_password(password="123")
def fibonachi(n):
    if n > 2:
        return fibonachi(n-1) + fibonachi(n-2)
    return 1

print(fibonachi(30))


# 5 problem

def cached(func):
    global cache
    cache = {}
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        global cache
        key = tuple(args) + tuple(kwargs)
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    return wrapper

@cached
@check_password(password="1234")
def fibonachi1(n):
    if n > 2:
        return fibonachi(n-1) + fibonachi(n-2)
    return 1

print(fibonachi1(30))