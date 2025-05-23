import os
import sys
import pickle
import hashlib
import platform
from datetime import datetime
from testdata import get_test_data

def is_pickleable(obj, protocol=3):
    try:
        pickle.dumps(obj, protocol=protocol)
        return True
    except Exception:
        return False

def record_pickle_hash(data, protocol=3):
    pickled = pickle.dumps(data, protocol=protocol)
    hash_val = hashlib.sha256(pickled).hexdigest()
    return hash_val, pickled

def main():
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)

    raw_data = get_test_data()
    protocol = 3

    # 先单独测试每个字段是否可pickle
    field_hashes = {}
    unpicklable = {}
    pickleable_data = {}
    for k, v in raw_data.items():
        try:
            h = hashlib.sha256(pickle.dumps(v, protocol=protocol)).hexdigest()
            field_hashes[k] = h
            pickleable_data[k] = v
        except Exception as e:
            field_hashes[k] = f"UNPICKLABLE: {e}"
            unpicklable[k] = str(e)

    # 用可pickle的子集整体序列化
    all_hash, all_pickled = record_pickle_hash(pickleable_data, protocol)
    pickle_len = len(all_pickled)

    meta = {
        "os": platform.platform(),
        "python_version": sys.version.replace('\n', ' '),
        "protocol": protocol,
        "datetime": datetime.now().isoformat(),
        "pickle_len": pickle_len,
        "fields_total": len(raw_data),
        "fields_pickleable": len(pickleable_data),
        "fields_unpickleable": len(unpicklable)
    }

    version_tag = f"py{sys.version_info.major}{sys.version_info.minor}"
    system_tag = platform.system().lower()  # 如 'windows', 'linux', 'darwin'
    txt_path = os.path.join(output_dir, f"hash_{version_tag}_{system_tag}.txt")
    bin_path = os.path.join(output_dir, f"hash_{version_tag}_{system_tag}.bin")

    # 写出文本
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(f"META: {meta}\n")
        f.write(f"ALL_HASH: {all_hash}\n")
        for k, h in field_hashes.items():
            f.write(f"FIELD_HASH[{k}]: {h}\n")
        if unpicklable:
            f.write("\nUNPICKLABLE_FIELDS:\n")
            for k, reason in unpicklable.items():
                f.write(f"  {k}: {reason}\n")

    # 一定会写出bin文件（只包含可pickle对象）
    with open(bin_path, "wb") as f:
        f.write(all_pickled)

    print(f"主hash: {all_hash}")
    print(f"字段级hash: {field_hashes}")
    if unpicklable:
        print("\n[WARNING] 以下字段不可pickle：")
        for k, reason in unpicklable.items():
            print(f"  {k}: {reason}")

if __name__ == "__main__":
    main()
    from testdata import run_whitebox_tests
    run_whitebox_tests()
