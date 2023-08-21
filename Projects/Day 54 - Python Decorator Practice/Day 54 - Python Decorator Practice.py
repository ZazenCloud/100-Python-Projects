import time


# Decorator function to calculate the execution speed of a function
def speed_calc_decorator(function):
    # Record the current time before running the function
    first_run = time.time()
    # Call the function
    function()
    # Record the current time after running the function
    second_run = time.time()
    # Calculate the time difference as the execution speed
    speed = second_run - first_run
    # Print the execution speed
    print(f"{function.__name__} run speed: {speed}")


@speed_calc_decorator
def fast_function():
    for i in range(10000000):
        i * i


@speed_calc_decorator
def slow_function():
    for i in range(100000000):
        i * i
