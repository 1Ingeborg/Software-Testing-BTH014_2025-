import collections
import datetime
import decimal
import hashlib
import io
import locale
import os
import pickle
import pickletools
import uuid
import sys
import struct
import math
import platform
import threading


LONG_FLOAT_STR = '0.3695054310985410369453981036945398103694539810369453981036945398103694539810369453981036945398103694452412345612045231204156414657452194521761529768546132196572561527965421675219467251496745216379514964725196735521967512769521796524146375296165726914527962015'
LONG_FLOAT = float(LONG_FLOAT_STR)
# 命名元组
Point = collections.namedtuple("Point", "x y")

def zero_func():
    return 0

# 常规自定义类
class CustomClass:
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def __eq__(self, other):
        return isinstance(other, CustomClass) and self.a == other.a and self.b == other.b
    def __repr__(self):
        return f"CustomClass(a={self.a}, b={self.b})"

# 带 __slots__ 的自定义类
class WithSlots:
    __slots__ = ['x', 'y']
    def __init__(self, x, y):
        self.x = x
        self.y = y

# 平台相关的自定义 __reduce__ 用例
class ReducePlatform:
    def __reduce__(self):
        return (str, (platform.system(),))

# 动态属性类，覆盖def-use链
class DynamicAttr:
    def __init__(self):
        self.x = 10
        self.y = 20
    def set_new(self):
        self.z = 99

# 覆盖 __getstate__/__setstate__
class GetSetState:
    def __init__(self):
        self.data = [1,2,3]
    def __getstate__(self):
        return {"data": self.data, "extra": 42}
    def __setstate__(self, state):
        self.data = state["data"]
        self.extra = state["extra"]

# 递归自引用
def get_recursive_list():
    l = []
    l.append(l)
    return l

def get_recursive_dict():
    d = {}
    d['self'] = d
    return d

def get_deep_nested_list():
    l = [[[[]]]]
    l[0][0][0].append(l)
    return l

def get_cross_reference():
    a = []
    b = [a]
    a.append(b)
    return a

# 不同bit pattern的NaN
def get_special_nans():
    nan1 = struct.unpack('d', b'\x00\x00\x00\x00\x00\x00\xf8\x7f')[0]
    nan2 = struct.unpack('d', b'\x01\x00\x00\x00\x00\x00\xf8\x7f')[0]
    nan3 = struct.unpack('d', b'\xff\xff\xff\xff\xff\xff\xff\x7f')[0]
    return [nan1, nan2, nan3]

# 常见不可pickle类型
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

def get_test_data():
    # 动态属性和def-use链对象
    obj = DynamicAttr()
    obj.set_new()  # 新增z属性
    dynamic_obj1 = obj
    dynamic_obj2 = obj
    dynamic_obj_copy = DynamicAttr()
    dynamic_obj_copy.x = 123

    getset_obj = GetSetState()
    getset_obj.data.append(4)  # 属性变更再pickle

    # def-use链：dict的key和value
    du_dict = {}
    for i in range(3):
        du_dict[f"key{i}"] = i*10
    du_dict["nested"] = {"inner": du_dict}

    # def-use链：list中被覆盖的元素
    du_list = [0]
    du_list[0] = 999

    # memo链：递归后再插入数据
    cross_a = []
    cross_b = [cross_a]
    cross_a.append(cross_b)
    cross_a.append(42)

    data = collections.OrderedDict([
        # 基本类型与边界
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

        # 字符串与字节
        ("empty_str", ""),
        ("short_ascii", "abc123"),
        ("long_str", "A" * 50000),
        ("unicode_str", "你好，🌟！\n\r\t☃"),
        ("bytes", b"bytes data"),
        ("bytearray", bytearray([1, 2, 3, 255])),
        ("empty_bytes", b""),
        ("empty_bytearray", bytearray()),

        # 容器类型
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

        # 顺序敏感（dict/set不同顺序）
        ("dict_keys_order1", {"a": 1, "b": 2}),
        ("dict_keys_order2", {"b": 2, "a": 1}),
        ("set_order1", set([1, 2, 3])),
        ("set_order2", set([3, 2, 1])),

        ("seg", {'c', 'a', 'b'}),  # 这种数据在不同环境/实现下遍历顺序不同，输出结果如37、38、311等可能不同

        ("path_win", "C:\\Users\\abc\\Desktop\\test.txt"),  # Windows下的路径分隔符
        ("path_unix", "/home/abc/test.txt"),  # Unix/Linux下的路径分隔符

        # 嵌套/递归结构
        ("list_of_dicts", [{"a": 1}, {"b": 2}]),
        ("dict_of_lists", {"l1": [1, 2, 3], "l2": [4, 5, 6]}),
        ("nested", [{"x": [1, 2, {"y": 3}]}]),
        ("recursive_list", get_recursive_list()),
        ("recursive_dict", get_recursive_dict()),

        # 标准库容器
        ("ordered_dict", collections.OrderedDict([('a', 1), ('b', 2)])),
        ("default_dict", collections.defaultdict(zero_func, x=1)),
        ("counter", collections.Counter("hello world")),
        ("namedtuple", Point(3, 4)),

        # 自定义类型
        ("custom_class", CustomClass(5, 10)),
        ("with_slots", WithSlots(7, 8)),

        # 标准库对象
        ("datetime", datetime.datetime(2024, 5, 22, 18, 30, 59, 123456)),
        ("date", datetime.date(2024, 5, 22)),
        ("time", datetime.time(23, 59, 59, 999999)),
        ("timedelta", datetime.timedelta(days=5, seconds=12345)),
        ("decimal", decimal.Decimal("3.1415926535897932384626")),
        ("uuid", uuid.UUID('12345678123456781234567812345678')),

        # 边界与极限
        ("big_set", set(range(1000))),
        ("large_list", list(range(10000))),
        ("large_dict", {str(i): i for i in range(1000)}),
        ("long_key_dict", {"A" * 1000: 123}),

        # 深度递归
        ("deep_nested_list", get_deep_nested_list()),

        # 不可变对象
        ("tuple_of_frozenset", (frozenset([1, 2]), frozenset([3, 4]))),

        # 特殊类型
        ("complex_number", complex(1, 2)),
        ("ellipsis", ...),
        ("notimplemented", NotImplemented),
        ("slice_obj", slice(1, 10, 2)),

        # python内置
        ("range_full", range(-100, 101)),
        ("bool_list", [True, False, True]),

        # 白盒切口类型
        ("cross_ref", get_cross_reference()),
        ("special_nans", get_special_nans()),
        ("frozenset1", frozenset([3, 2, 1, 0])),
        ("frozenset2", frozenset([0, 1, 2, 3])),
        ("tricky_platform", ReducePlatform()),
        ("equal_content_list_1", [1, 2, 3]),
        ("equal_content_list_2", [1, 2, 3]),

        # all-def all-use相关对象
        ("dynamic_obj1", dynamic_obj1),
        ("dynamic_obj2", dynamic_obj2),
        ("dynamic_obj_copy", dynamic_obj_copy),
        ("getset_obj", getset_obj),
        ("du_dict", du_dict),
        ("du_list", du_list),
        ("cross_a", cross_a),
    ])

    # 常见不可pickle类型（try/except可跳过）
    data.update(get_unpicklable())
    return data

def get_opnames(data):
    return [op[0].name for op in pickletools.genops(data)]

def get_opnames(data):
    return [op[0].name for op in pickletools.genops(data)]

def test_recursive_list():
    a = []
    a.append(a)
    d = pickle.dumps(a)
    b = pickle.loads(d)
    assert b[0] is b

def test_recursive_dict():
    d = {}
    d["self"] = d
    p = pickle.dumps(d)
    d2 = pickle.loads(p)
    assert d2["self"] is d2

def test_non_picklable_type():
    try:
        pickle.dumps(lambda x: x+1)
        assert False, "pickle.dumps(lambda) 应该抛出异常"
    except Exception:
        pass


class Custom:
    def __init__(self, value):
        self.value = value
    def __eq__(self, other):
        return type(other) == type(self) and self.value == other.value

def test_custom_object():
    o = Custom(123)
    d = pickle.dumps(o)
    o2 = pickle.loads(d)
    assert o == o2 and o is not o2

def test_custom_getstate_setstate():
    class X:
        def __init__(self): self.data = 1
        def __getstate__(self): return {"x":42}
        def __setstate__(self, st): self.data = st["x"]
    x = X()
    d = pickle.dumps(x)
    y = pickle.loads(d)
    assert y.data == 42

def test_custom_reduce():
    class Y:
        def __reduce__(self):
            return (str, ("reduce!",))
    y = Y()
    d = pickle.dumps(y)
    assert pickle.loads(d) == "reduce!"

def test_global_class():
    import datetime
    obj = datetime.datetime(2024, 5, 20, 12, 30)
    d = pickle.dumps(obj)
    assert pickle.loads(d) == obj

def test_unpickled_identity():
    obj = [1,2]
    b = pickle.loads(pickle.dumps(obj))
    assert obj == b and obj is not b

def test_dispatch_table():
    # 白盒: Pickler.dispatch应含常用类型
    disp = pickle.Pickler.dispatch
    for typ in [list, dict, tuple, set, frozenset, str, int, float]:
        assert typ in disp

def test_memoization_opcodes():
    a = [1]
    obj = [a, a]
    d = pickle.dumps(obj)
    ops = get_opnames(d)
    assert ("BINPUT" in ops or "LONG_BINPUT" in ops) and ("BINGET" in ops or "LONG_BINGET" in ops)



# --------- 自定义分支、内部路径 ---------


def test_unicode_binlong_opcode():
    val = 2**120
    d = pickle.dumps(val, protocol=3)
    ops = get_opnames(d)
    assert "LONG1" in ops or "LONG4" in ops

def test_empty_set_opcode():
    d = pickle.dumps(set(), protocol=4)
    assert "EMPTY_SET" in get_opnames(d)

def test_frozenset_opcode():
    d = pickle.dumps(frozenset([1,2]), protocol=4)
    assert "FROZENSET" in get_opnames(d)

def test_additems_opcode():
    d = pickle.dumps({1,2,3}, protocol=4)
    assert "ADDITEMS" in get_opnames(d)

def test_binunicode_opcode():
    s = "a" * 300
    d = pickle.dumps(s, protocol=4)
    assert "BINUNICODE" in get_opnames(d)

def test_short_binbytes_opcode():
    d = pickle.dumps(b"123", protocol=4)
    assert "SHORT_BINBYTES" in get_opnames(d)

def test_appends_opcode():
    d = pickle.dumps([1,2,3], protocol=4)
    assert "APPENDS" in get_opnames(d)

def test_recursive_tuple():
    t = ([],)
    t[0].append(t)
    d = pickle.dumps(t)
    t2 = pickle.loads(d)
    assert t2[0][0] is t2



def test_slots_object():
    class SlotObj:
        __slots__ = ('a',)
        def __init__(self): self.a = 5
    d = pickle.dumps(SlotObj())
    s = pickle.loads(d)
    assert s.a == 5

def test_tuple_subclass():
    class MyTuple(tuple): pass
    x = MyTuple((1,2))
    d = pickle.dumps(x)
    y = pickle.loads(d)
    assert isinstance(y, MyTuple) and y == (1,2)



def test_set_order_differs():
    s = set(range(50))
    pkl = pickle.dumps(s, protocol=4)
    h = hashlib.sha256(pkl).hexdigest()
    print("set order hash:", h)
    assert pickle.loads(pkl) == s

def test_dict_order_differs():
    d = {i: chr(65 + i) for i in range(50)}
    pkl = pickle.dumps(d, protocol=4)
    h = hashlib.sha256(pkl).hexdigest()
    print("dict order hash:", h)
    assert pickle.loads(pkl) == d

class PathObj:
    def __init__(self):
        self.path = os.path.abspath(".")
    def __eq__(self, other):
        return self.path == other.path

def test_os_path_platform_diff():
    obj = PathObj()
    pkl = pickle.dumps(obj)
    obj2 = pickle.loads(pkl)
    print("platform path:", obj2.path)

def test_locale_affect_unicode():
    s = "中文"
    pkl = pickle.dumps(s)
    print("current locale:", locale.getpreferredencoding())
    print("pickle bytes:", pkl)
    assert pickle.loads(pkl) == s



def run_whitebox_tests():
    tests = [
        test_recursive_list,
        test_recursive_dict,
        test_non_picklable_type,
    ]
    failed = 0
    for test in tests:
        try:
            test()
        except Exception as e:
            print(f"[白盒测试 FAILED] {test.__name__}: {e}")
            failed += 1
    if failed == 0:
        print("通过！")
    else:
        print(f"[白盒测试] 未通过: {failed} 个")