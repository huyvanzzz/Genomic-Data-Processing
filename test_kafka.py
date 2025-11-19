import pandas as pd
import glob
from IPython.display import display

# -----------------------------
# Cấu hình pandas hiển thị tất cả cột
pd.set_option('display.max_columns', None)  # hiển thị tất cả cột
pd.set_option('display.width', 300)         # chiều rộng màn hình
pd.set_option('display.max_rows', 100)     # hiển thị tối đa 100 hàng
# -----------------------------

# Nếu chỉ 1 file Parquet
parquet_file = r"part-00000-f5c80eb3-fa05-4b07-a494-8ca82e78d450-c000.snappy.parquet"

# Đọc file Parquet
df = pd.read_parquet(parquet_file)

# Hiển thị 10 dòng đầu tiên với tất cả cột
display(df.head(10))
