from collections import OrderedDict
import datetime, decimal, uuid

class MyClass:
    __slots__ = ['x', 'y']
    def __init__(self):
        self.x = 1
        self.y = [1, 2, 3]

def get_equivalence_class_samples():
    recursive_list = []
    recursive_list.append(recursive_list)

    return {
        "int": 42,
        "float": 3.14159,
        "str": "hello world",
        "unicode_str": "你好，世界 🌏",
        "list": [1, 2, 3],
        "dict": {"key": "value", "num": 10},
        "tuple": (1, "a", 3.14),
        "seg": {'c', 'a', 'b'},
        "set": {1, 2, 3},
        "bool": True,
        "none": None,
        "nested": {"a": [1, {"b": 2}], "c": (3, 4)},
        "ordered_dict": OrderedDict([("a", 1), ("b", 2)]),
        "recursive_list": recursive_list,
        "custom_class": MyClass(),
        "datetime": datetime.datetime(2025, 5, 20, 10, 30),
        "decimal": decimal.Decimal("3.14159"),
        "uuid": uuid.UUID("12345678123456781234567812345678")
    }
