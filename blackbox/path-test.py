import pickle
import hashlib
import os

obj = os.getcwd()
print(obj)

# 使用 pickle 序列化对象
serialized = pickle.dumps(obj, protocol=4)
hex_str = serialized.hex()

# 计算 SHA256 哈希
hash_val = hashlib.sha256(serialized).hexdigest()

# 输出结果
print(f"Original Object : {repr(obj)}")
print(f"Pickled (hex)   : {hex_str}")
print(f"SHA256 Hash     : {hash_val}")
