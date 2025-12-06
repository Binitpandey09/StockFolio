#!/usr/bin/env python3

import os
import sys

# Test imports
try:
    from pyspark.sql import SparkSession
    print("✓ Successfully imported PySpark modules")
except ImportError as e:
    print(f"✗ Failed to import PySpark modules: {e}")
    sys.exit(1)

try:
    # Create Spark session
    spark = SparkSession.builder \
        .appName("Test Spark Setup") \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
        .getOrCreate()
    
    print(f"✓ Successfully created Spark session")
    print(f"✓ Spark version: {spark.version}")
    print(f"✓ Java version: {spark.sparkContext._gateway.jvm.System.getProperty('java.version')}")
    
    # Test basic operations
    data = [1, 2, 3, 4, 5]
    rdd = spark.sparkContext.parallelize(data)
    result = rdd.map(lambda x: x * 2).collect()
    print(f"✓ Basic RDD operations working: {result}")
    
    # Test DataFrame operations
    from pyspark.sql import Row
    df_data = [Row(name="Alice", age=25), Row(name="Bob", age=30)]
    df = spark.createDataFrame(df_data)
    df.show()
    print("✓ DataFrame operations working")
    
    # Stop Spark session
    spark.stop()
    print("✓ Spark session stopped successfully")
    print("\n🎉 All tests passed! Spark setup is complete and working properly.")
    
except Exception as e:
    print(f"✗ Error during Spark testing: {e}")
    sys.exit(1)
