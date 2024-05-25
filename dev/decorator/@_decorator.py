def add_prefix_suffix(func):
    def wrapper(*args, **kwargs):
        print("Prefix: Starting the function")
        result = func(*args, **kwargs)
        print("Suffix: Ending the function")
        return result

    return wrapper


@add_prefix_suffix
def greet(name):
    print(f"Hello, {name}!")


greet("Alice")
