import inspect


def strict(func):
    """
    Декоратор @strict проверяет соответствие типов переданных аргументов типам,
    указанным в аннотациях параметров функции. Если аннотация для параметра не
    задана, то проверка аргумента пропускается.
    """

    def wrapper(*args, **kwargs):
        bound = inspect.signature(func).bind(*args, **kwargs)
        for arg, arg_type in bound.arguments.items():
            expected_type = func.__annotations__.get(arg)
            if expected_type and not isinstance(arg_type, expected_type):
                raise TypeError(
                    f'Argument "{arg}" must be {expected_type.__name__}, '
                    f'got {type(arg_type).__name__}'
                )
        return func(*args, **kwargs)

    return wrapper
