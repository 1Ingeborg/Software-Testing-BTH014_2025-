import random
import string
import json
import os

def random_string(length=10):
    return ''.join(random.choices(string.printable, k=length))

def random_nested_list(depth=2):
    if depth <= 0:
        return [random.randint(0, 100)]
    return [random.choice([
        random.randint(-1000, 1000),
        random_string(),
        random_nested_list(depth - 1),
        random_nested_dict(depth - 1),
        None,
        True,
        False,
        float('nan')
    ]) for _ in range(random.randint(2, 5))]

def random_nested_dict(depth=2):
    d = {}
    for _ in range(random.randint(2, 4)):
        key = random_string(5)
        if depth <= 0:
            d[key] = random.choice([
                random_string(),
                random.randint(0, 999),
                None
            ])
        else:
            d[key] = random.choice([
                random_string(),
                random_nested_list(depth - 1),
                random_nested_dict(depth - 1),
                random.uniform(-1e6, 1e6),
                None,
                float('nan')
            ])
    return d

def generate_fuzz_data(n=10):
    samples = {}
    for i in range(n):
        samples["fuzz_%d" % i] = random.choice([
            random_string(random.randint(5, 30)),
            random_nested_list(depth=2),
            random_nested_dict(depth=2),
            {"user": random_string(6), "active": random.choice([True, False]), "data": random_nested_list(1)},
            set(random_string(5)),
            frozenset(random_string(5)),
            [{"id": i, "value": random.random(), "meta": None} for i in range(3)]
        ])
    return samples

def get_fuzz_samples(n=10):
    seed_file = os.path.join(os.path.dirname(__file__), 'fuzz_seed.json')

    # 如果 seed 文件存在，就加载
    if os.path.exists(seed_file):
        with open(seed_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    # 否则生成新样本并保存
    samples = generate_fuzz_data(n)

    # 将不支持的对象（如 set/frozenset/float nan）转换为 JSON 兼容结构
    def convert(obj):
        if isinstance(obj, (set, frozenset)):
            return list(obj)
        if isinstance(obj, float) and (obj != obj):  # nan
            return "NaN"
        if isinstance(obj, dict):
            return {k: convert(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [convert(v) for v in obj]
        return obj

    json_compatible = {k: convert(v) for k, v in samples.items()}
    with open(seed_file, 'w', encoding='utf-8') as f:
        json.dump(json_compatible, f, ensure_ascii=False, indent=2)
    return json_compatible
