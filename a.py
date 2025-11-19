from ai.chest_xray1 import predict_chest_xray  # import hàm

from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

spark = SparkSession.builder.getOrCreate()

data = [("hdfs://namenode:9000/xray/images/batch_004/00000011_004.png",)]
df_test = spark.createDataFrame(data, ["image_path"])

predict_udf = udf(lambda path: predict_chest_xray(path), StringType())
df_test = df_test.withColumn("prediction", predict_udf("image_path"))
df_test.show(truncate=False)
