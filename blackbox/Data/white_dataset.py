# 修改后的 white_dataset.py 风格模块

import collections
import datetime
import decimal
import uuid
import sys
import struct
import math
import platform
import threading

def get_whitebox_samples():
    LONG_FLOAT_STR = '0.3695054310985410369453981036945398103694539810369453981036945398103694539810369453981036945398103694452412345612045231204156414657452194521761529768546132196572561527965421675219467251496745216379514964725196735521967512769521796524146375296165726914527962015'
    LONG_FLOAT = float(LONG_FLOAT_STR)

    Point = collections.namedtuple("Point", "x y")

    def zero_func():
        return 0

    class CustomClass:
        def __init__(self, a, b):
            self.a = a
            self.b = b
        def __eq__(self, other):
            return isinstance(other, CustomClass) and self.a == other.a and self.b == other.b
        def __repr__(self):
            return "CustomClass(a=%r, b=%r)" % (self.a, self.b)

    class WithSlots:
        __slots__ = ['x', 'y']
        def __init__(self, x, y):
            self.x = x
            self.y = y

    class ReducePlatform:
        def __reduce__(self):
            return (str, (platform.system(),))

    def get_cross_reference():
        a = []
        b = [a]
        a.append(b)
        return a

    def get_special_nans():
        nan1 = struct.unpack('d', b'\x00\x00\x00\x00\x00\x00\xf8\x7f')[0]
        nan2 = struct.unpack('d', b'\x01\x00\x00\x00\x00\x00\xf8\x7f')[0]
        nan3 = struct.unpack('d', b'\xff\xff\xff\xff\xff\xff\xff\x7f')[0]
        return [nan1, nan2, nan3]

    def get_recursive_list():
        l = []
        l.append(l)
        return l

    def get_recursive_dict():
        d = {}
        d['self'] = d
        return d

    def get_deep_nested_list():
        l = []
        tmp = l
        for _ in range(500):
            new = []
            tmp.append(new)
            tmp = new
        return l

    def get_unpicklable():
        try:
            f = open(__file__, 'rb')
        except Exception:
            f = None
        return {
            "unpicklable_file": f,
            "unpicklable_lambda": (lambda x: x + 1),
            "unpicklable_threadlock": threading.Lock(),
            "unpicklable_generator": (i for i in range(2)),
        }

    data = collections.OrderedDict([
        ("int_zero", 0),
        ("int_max", sys.maxsize),
        ("int_min", -sys.maxsize - 1),
        ("float_zero", 0.0),
        ("float_neg", -3.1415926),
        ("float_pos", LONG_FLOAT),
        ("float_nan", float('nan')),
        ("float_inf", float('inf')),
        ("float_ninf", float('-inf')),
        ("bool_true", True),
        ("bool_false", False),
        ("none", None),
        ("empty_str", ""),
        ("short_ascii", "abc123"),
        ("long_str", "A" * 50000),
        ("unicode_str", "你好，🌟！\n\r\t☃"),
        ("bytes", b"bytes data"),
        ("bytearray", bytearray([1, 2, 3, 255])),
        ("empty_bytes", b""),
        ("empty_bytearray", bytearray()),
        ("empty_list", []),
        ("single_item_list", [42]),
        ("empty_tuple", ()),
        ("single_item_tuple", (99,)),
        ("empty_dict", {}),
        ("single_item_dict", {"x": 123}),
        ("empty_set", set()),
        ("single_item_set", {7}),
        ("frozenset", frozenset([1, 2, 3])),
        ("empty_frozenset", frozenset()),
        ("range", range(10, 100, 3)),
        ("dict_keys_order1", {"a": 1, "b": 2}),
        ("dict_keys_order2", {"b": 2, "a": 1}),
        ("set_order1", set([1, 2, 3])),
        ("set_order2", set([3, 2, 1])),
        ("list_of_dicts", [{"a": 1}, {"b": 2}]),
        ("dict_of_lists", {"l1": [1, 2, 3], "l2": [4, 5, 6]}),
        ("nested", [{"x": [1, 2, {"y": 3}]}]),
        ("recursive_list", get_recursive_list()),
        ("recursive_dict", get_recursive_dict()),
        ("ordered_dict", collections.OrderedDict([('a', 1), ('b', 2)])),
        ("default_dict", collections.defaultdict(zero_func, x=1)),
        ("counter", collections.Counter("hello world")),
        ("namedtuple", Point(3, 4)),
        ("custom_class", CustomClass(5, 10)),
        ("with_slots", WithSlots(7, 8)),
        ("datetime", datetime.datetime(2024, 5, 22, 18, 30, 59, 123456)),
        ("date", datetime.date(2024, 5, 22)),
        ("time", datetime.time(23, 59, 59, 999999)),
        ("timedelta", datetime.timedelta(days=5, seconds=12345)),
        ("decimal", decimal.Decimal("3.1415926535897932384626")),
        ("uuid", uuid.UUID('12345678123456781234567812345678')),
        ("big_set", set(range(1000))),
        ("large_list", list(range(10000))),
        ("large_dict", {str(i): i for i in range(1000)}),
        ("long_key_dict", {"A" * 1000: 123}),
        ("deep_nested_list", get_deep_nested_list()),
        ("tuple_of_frozenset", (frozenset([1, 2]), frozenset([3, 4]))),
        ("complex_number", complex(1, 2)),
        ("ellipsis", ...),
        ("notimplemented", NotImplemented),
        ("slice_obj", slice(1, 10, 2)),
        ("range_full", range(-100, 101)),
        ("bool_list", [True, False, True]),
        ("cross_ref", get_cross_reference()),
        ("special_nans", get_special_nans()),
        ("frozenset1", frozenset([3, 2, 1, 0])),
        ("frozenset2", frozenset([0, 1, 2, 3])),
        ("tricky_platform", ReducePlatform()),
        ("equal_content_list_1", [1, 2, 3]),
        ("equal_content_list_2", [1, 2, 3]),
    ])

    data.update(get_unpicklable())
    return data
