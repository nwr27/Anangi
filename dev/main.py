def add_prefix_suffix(func):
    def wrapper(*args, **kwargs):
        print("Prefix: Starting the function")
        result = func(*args, **kwargs)
        print("Suffix: Ending the function")
        return result

    return wrapper


def greet(name):
    print(f"Hello, {name}!")


# Manual way of decorating
greet_with_prefix_suffix = add_prefix_suffix(greet)
greet_with_prefix_suffix("Alice")
