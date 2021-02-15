from time import time

def time_decorator(func):
    def wrapper(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print('Время выполнения', t2 - t1)
        with open('log.txt', 'a') as f:
            f.write(f'{func.__name__} | время выполнения - {t2-t1} секунд\n')
        return result
    return wrapper