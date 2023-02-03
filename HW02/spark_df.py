#!/usr/bin/python
# coding:utf-8
import sys,os
from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.types import *
from datetime import datetime, timedelta
from pyspark.sql.functions import to_timestamp
from pyspark.sql.functions import *
from pyspark.sql.functions import avg, round
import pyspark.sql.functions as f
from pyspark.sql import Window

sc = SparkContext.getOrCreate()
spark = SQLContext(sc)
df = spark.read.format("csv").option("encoding","BIG5").option("header", "true").option("inferSchema", "true")\
.load("s3://storearea/bank.csv")
df.printSchema()
df.show()
df.select("age").groupBy("age").count().sort("age").show()