from pymongo import MongoClient

# Thay <db_password> bằng mật khẩu thật
mongo_uri = "mongodb+srv://Bigdata:<db_password>@clusterxray.ahgkigy.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(mongo_uri)

# Chọn database
db = client["xray_db"]

# Chọn collection để lưu metadata
collection = db["predictions"]
