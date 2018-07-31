import threading
from time import sleep
from typing import Callable
from config.Constants import *


def _p(s, end='\n'):
    if DEBUG:
        print(s, end=end)


def mult_thread_execute(target: Callable, execute_number: int, args: list = None,
                        kwargs: list = None,
                        thread_number: int = 5):
    '''
    Execute specific function with multi threads.
    :param target: the function to execute.
    :param execute_number: number of execution.
    :param args: positional arguments.
    :param kwargs: keyword arguments.
    :param thread_number: number of maximum execution threads as the same time.
    :return: the return value of each execution in a list.
    '''
    if args is None:
        args = [[]] * execute_number
    if kwargs is None:
        kwargs = [{}] * execute_number

    lock = threading.Lock()
    result = []

    # Decorate the target function to collect its return value.
    def decorated(*args, **kwargs):
        _p('Starting thread: ' + threading.current_thread().getName())
        r = target(*args, **kwargs)
        # acquire thread lock before append the result.
        lock.acquire()
        result.append(r)
        lock.release()
        _p('Ending thread: ' + threading.current_thread().getName())

    while execute_number > 0:
        threads = []
        for i in range(0, thread_number):
            if execute_number == 0:
                break
            # start new thread with name "[target function] #i"
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
