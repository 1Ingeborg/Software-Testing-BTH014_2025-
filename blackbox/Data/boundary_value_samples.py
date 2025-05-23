import sys
import datetime
import decimal

def get_boundary_value_samples():
    max_int = sys.maxsize
    min_int = -sys.maxsize - 1
    long_str = "a" * 10000  # 超长字符串
    empty_list = []
    large_list = list(range(10000))
    empty_dict = {}
    deep_nested_list = [1]
    for _ in range(50):  # 构造深度为 50 的嵌套结构
        deep_nested_list = [deep_nested_list]

    return {
        "max_int": max_int,
        "min_int": min_int,
        "zero": 0,
        "long_str": long_str,
        "empty_str": "",
        "empty_list": empty_list,
        "large_list": large_list,
        "empty_dict": empty_dict,
        "max_float": float('inf'),
        "min_float": float('-inf'),
        "nan_float": float('nan'),
        "decimal_max": decimal.Decimal('1E+1000'),
        "decimal_min": decimal.Decimal('-1E+1000'),
        "deep_nested_list": deep_nested_list,
        "long_tuple": tuple(range(1000)),
        "long_bytes": b'\x00' * 4096,
        "oldest_date": datetime.datetime.min,
        "future_date": datetime.datetime.max,
    }
