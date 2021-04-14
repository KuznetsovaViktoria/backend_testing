import functools


user = {
    'name': 'Ivan',
    'access_level': 'admin'
}


def secure(access_level):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if access_level == 'admin':
                return func(*args, **kwargs)
            return 'access denied'

        return wrapper
    return decorator

@secure('guest') #аналог строки get_secure_information = secure(get_secure_information()), только лучше, потому что изначально указано
def get_secure_information(role):
    if role == 'admin':
        return 'My password is 123'
    return 'else info'


print(get_secure_information('guest'))