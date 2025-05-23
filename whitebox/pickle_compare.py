import os
import itertools
import pickle
import hashlib

def deep_compare(obj1, obj2, path=""):
    diffs = []
    if type(obj1) != type(obj2):
        diffs.append((path, "type", type(obj1), type(obj2)))
        return diffs
    if isinstance(obj1, dict):
        for k in set(obj1.keys()).union(obj2.keys()):
            if k not in obj1:
                diffs.append((f"{path}.{k}", "missing_left", None, obj2[k]))
            elif k not in obj2:
                diffs.append((f"{path}.{k}", "missing_right", obj1[k], None))
            else:
                diffs += deep_compare(obj1[k], obj2[k], f"{path}.{k}")
    elif isinstance(obj1, (list, tuple, set, frozenset, range)):
        l1, l2 = list(obj1), list(obj2)
        if len(l1) != len(l2):
            diffs.append((path, "len", len(l1), len(l2)))
        else:
            for i, (a, b) in enumerate(zip(l1, l2)):
                diffs += deep_compare(a, b, f"{path}[{i}]")
    elif isinstance(obj1, float):
        if (obj1 != obj1 and obj2 != obj2):  # both NaN
            pass
        elif obj1 != obj2:
            diffs.append((path, "float", obj1, obj2))
    else:
        if obj1 != obj2:
            diffs.append((path, "value", obj1, obj2))
    return diffs

def guess_cause(diffs):
    # 简单原因分析，根据类型推断
    reasons = set()
    for path, dtype, v1, v2 in diffs:
        if dtype == "float":
            reasons.add("浮点数精度/NaN/Inf平台差异")
        elif dtype == "type":
            reasons.add("类型实现不兼容")
        elif dtype == "len":
            reasons.add("容器长度不同")
        elif dtype == "missing_left" or dtype == "missing_right":
            reasons.add("key/字段缺失")
        elif dtype == "value":
            if isinstance(v1, dict) or isinstance(v2, dict):
                reasons.add("dict顺序或实现不同")
            elif isinstance(v1, set) or isinstance(v2, set):
                reasons.add("set/frozenset顺序")
            elif isinstance(v1, str) or isinstance(v2, str):
                reasons.add("字符串编码差异")
            elif isinstance(v1, bytes) or isinstance(v2, bytes):
                reasons.add("字节内容不同")
            else:
                reasons.add("内容值不同")
    if not reasons:
        return "可能是引用顺序、对象ID、低层实现或平台相关的差异"
    return "，".join(reasons)

def compare_files(binfile1, binfile2):
    with open(binfile1, "rb") as f:
        data1 = f.read()
    with open(binfile2, "rb") as f:
        data2 = f.read()
    h1 = hashlib.sha256(data1).hexdigest()
    h2 = hashlib.sha256(data2).hexdigest()
    result = {
        "file1": binfile1,
        "file2": binfile2,
        "hash1": h1,
        "hash2": h2,
        "identical": h1 == h2,
        "diffs": [],
        "cause": ""
    }
    if h1 != h2:
        try:
            obj1 = pickle.loads(data1)
            obj2 = pickle.loads(data2)
            diffs = deep_compare(obj1, obj2)
            result["diffs"] = diffs
            result["cause"] = guess_cause(diffs)
        except Exception as e:
            result["cause"] = f"Pickle反序列化失败: {e}"
    return result

def main():
    directory = "outputs"
    files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".bin")]
    files.sort()
    results = []
    pairs = list(itertools.combinations(files, 2))
    for f1, f2 in pairs:
        print(f"比较: {os.path.basename(f1)} <-> {os.path.basename(f2)} ...")
        result = compare_files(f1, f2)
        results.append(result)
        if result["identical"]:
            print("  ✅ hash一致")
        else:
            print("  ❌ hash不一致")
            print(f"    hash1: {result['hash1']}")
            print(f"    hash2: {result['hash2']}")
            print(f"    主要原因: {result['cause']}")
            if result["diffs"]:
                print("    差异字段:")
                for d in result["diffs"][:5]:  # 只显示前5条
                    print(f"      {d}")
            else:
                print("    （结构和内容一致，差异可能在底层实现/引用顺序/浮点精度）")
    # 统计主要原因
    cause_counter = {}
    for r in results:
        if not r["identical"]:
            cause = r["cause"]
            cause_counter[cause] = cause_counter.get(cause, 0) + 1
    print("\n=== 差异原因统计 ===")
    for k, v in cause_counter.items():
        print(f"{k}: {v} 次")
    print("\n全部完成！")

if __name__ == "__main__":
    main()
