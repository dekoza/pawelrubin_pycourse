from inspect import getfullargspec
from typing import Callable, Dict, Tuple

TypeSignature = Tuple[Tuple[type, ...], Tuple[Tuple[str, type], ...]]


class Overload:
    functions: Dict[Tuple[str, TypeSignature], Callable] = {}

    def __init__(self, function: Callable):
        Overload.functions[
            (function.__name__, self.get_type_signature(function))
        ] = function
        self.function = function

    def __call__(self, *args, **kwargs):
        for (name, type_signature), function in self.functions.items():
            if name == self.function.__name__ and self.does_type_signature_match(
                *args, type_signature=type_signature, **kwargs
            ):
                return function(*args, **kwargs)
        return TypeError

    @staticmethod
    def get_type_signature(function: Callable) -> TypeSignature:
        fullargspec = getfullargspec(function)
        get_annotation = lambda arg: fullargspec.annotations.get(arg, object)
        return (
            tuple(map(get_annotation, fullargspec.args,)),
            tuple((kwarg, get_annotation(kwarg)) for kwarg in fullargspec.kwonlyargs),
        )

    @staticmethod
    def does_type_signature_match(
        *args, type_signature: TypeSignature, **kwargs
    ) -> bool:

        positionals = args + tuple(
            val
            for kwarg, val in kwargs.items()
            if kwarg not in list(map(lambda tup: tup[0], type_signature[1]))
        )

        kwonly = {
            kwarg: val
            for kwarg, val in kwargs.items()
            if kwarg in list(map(lambda tup: tup[0], type_signature[1]))
        }

        return (
            len(positionals) == len(type_signature[0])
            and all(
                isinstance(arg, typ) for arg, typ in zip(positionals, type_signature[0])
            )
            and len(kwonly) == len(type_signature[1])
            and all(
                kwarg == _kwarg and isinstance(val, typ)
                for (kwarg, val), (_kwarg, typ) in zip(
                    kwonly.items(), type_signature[1]
                )
            )
        )


def overload(function: Callable):
    return Overload(function)


if __name__ == "__main__":

    @overload
    def foo(x, *, y: int = 0):
        return 2

    @overload
    def foo(x, y):
        return 1


    @overload
    def foo(x):
        return 0

    print(f"foo(x=1, y=2.0) = {foo(x=1, y=2.0)}")
    print(f"foo(1, y=2)     = {foo(1, y=2)}")
    print(f"foo(1)          = {foo(1)}")
    print(f"foo(x=1, y=2)   = {foo(x=1, y=2)}")
