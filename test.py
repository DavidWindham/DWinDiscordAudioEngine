from functools import wraps

def wrapper(func_to_wrap):
    @wraps(func_to_wrap)
    def wrapper_inner(*args):
        third_var = "this is a test"
        fourth_var = "fourth"
        func_to_wrap(*args, third_var, fourth_var)

    return wrapper_inner

@wrapper
def test_func(first_var, second_var, third_var, fourth_var):
    print("Inside test_func: ", first_var)
    print("The second var is: ", second_var)
    print("The third var is: ", third_var)
    print("The fourthsecond var is: ", fourth_var)

test_func("test", "second")
