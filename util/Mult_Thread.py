import threading
from time import sleep
from typing import Callable
from model.Constants import *


def _p(s, end='\n'):
    if DEBUG:
        print(s, end=end)


def mult_thread_execute(target: Callable, execute_number: int, args: list = None,
                        kwargs: list = None,
                        thread_number: int = 5):
    if args is None:
        args = [[]] * execute_number
    if kwargs is None:
        kwargs = [{}] * execute_number

    lock = threading.Lock()
    result = []

    def decorated(*args, **kwargs):
        _p('Starting thread: ' + threading.current_thread().getName())
        r = target(*args, **kwargs)
        lock.acquire()
        result.append(r)
        lock.release()
        _p('Ending thread: ' + threading.current_thread().getName())

    while execute_number > 0:
        threads = []
        for i in range(0, thread_number):
            if execute_number == 0:
                break
            t = threading.Thread(target=decorated, name=target.__name__ + ' #' + str(i),
                                 args=args.pop(0), kwargs=kwargs.pop(0))
            threads.append(t)
            execute_number -= 1
        for t in threads:
            t.start()
        for t in threads:
            t.join()
    return result


if __name__ == '__main__':
    def foo(a='666'):
        for i in range(5):
            print(str(a))
            sleep(1)
        return 'OJBK'


    r = mult_thread_execute(foo, 10)
    print(r)
