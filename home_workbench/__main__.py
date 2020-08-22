import sys

from home_workbench.home_workbench import fib

if __name__ == "__main__":
    n = int(sys.argv[1])
    print(fib(n))
