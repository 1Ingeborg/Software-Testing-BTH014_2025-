import decimal
import random

random.seed(2024)  # 固定种子
digits = ''.join(str(random.randint(0,9)) for _ in range(100))
long_str = '0.' + digits
long_float = float(long_str)
print('长浮点:', long_str)
print('float:', long_float)
