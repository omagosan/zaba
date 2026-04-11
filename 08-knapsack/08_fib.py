from utils import measure_time
import functools 

cache = {}

def fib(n: int) -> int:
    if n < 2:
        return n

    return fib(n - 1) + fib(n - 2)

def fib_mem(n: int) -> int: # memoizace
    if n < 2:
        return n

    if n in cache:
        return cache[n]

    result = fib_mem(n - 1) + fib_mem(n - 2)
    cache[n] = result

    return result

def fib_nonr(n: int) -> int: # nerekurzivní
    fibonacci = [0, 1]

    while len(fibonacci) < n + 1:
        fibonacci.append(fibonacci[-1] + fibonacci[-2])

    return fibonacci[n]


@functools.cache
def fib_cache(n: int) -> int: # python cache
    if n < 2:
        return n

    return fib(n - 1) + fib(n - 2)

if __name__ == "__main__":
    measure_time(lambda: fib_nonr(30), 100)
    measure_time(lambda: fib_mem(30), 100)

    # print(f"fib_mem(7) = {fib_mem(7)}")
    # print(f"fib_mem(20) = {fib_mem(20)}")
    # print(f"fib_mem(35) = {fib_mem(35)}")
    # print(f"fib_mem(50) = {fib_mem(50)}")

    # print(f"fib_nonr(7) = {fib_nonr(7)}")
    # print(f"fib_nonr(20) = {fib_nonr(20)}")
    # print(f"fib_nonr(35) = {fib_nonr(35)}")
    # print(f"fib_nonr(50) = {fib_nonr(50)}")


