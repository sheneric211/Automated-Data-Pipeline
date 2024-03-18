from mongodb import mongodb

@mongodb
def save_spark_dataframe(collection, **kwargs):
    import os
    from pyspark.sql.types import StructType, StructField, StringType, FloatType
    from pyspark.sql import SparkSession
    from pyspark.sql.functions import col, when, lower

    output_path = kwargs['output_path']

    hours_per_year = 40 * 52
    salary_threshold = 1000

    spark = SparkSession.builder \
        .appName("MongoDBIntegration") \
        .config("spark.driver.memory", "2g") \
        .config("spark.executor.memory", "8g") \
        .getOrCreate()

    schema = StructType(
        [
            StructField("job_url", StringType(), True),
            StructField("site", StringType(), True),
            StructField("title", StringType(), True),
            StructField("company", StringType(), True),
            StructField("company_url", StringType(), True),
            StructField("location", StringType(), True),
            StructField("job_type", StringType(), True),
            StructField("date_posted", StringType(), True),
            StructField("interval", StringType(), True),
            StructField("min_amount", FloatType(), True),
            StructField("max_amount", FloatType(), True),
            StructField("currency", StringType(), True),
            StructField("is_remote", StringType(), True),
            StructField("num_urgent_words", StringType(), True),
            StructField("benefits", StringType(), True),
            StructField("emails", StringType(), True),
            StructField("description", StringType(), True)
        ]
    )
    cursor = collection.find({}, {'_id' : 0})
    data = [doc for doc in cursor]

    df = spark.createDataFrame(data=data, schema=schema)

    df = df.withColumn("min_amount_float", col("min_amount").cast("float"))
    df = df.withColumn("max_amount_float", col("max_amount").cast("float"))
    
    # Determine if the salary is hourly based on the threshold
    df = df.withColumn("is_hourly",
                       when(col("min_amount_float") < salary_threshold, True)
                       .when(col("max_amount_float") < salary_threshold, True)
                       .when(col("interval") == "hourly", True)
                       .otherwise(False))

    df = df.withColumn("min_amount_yearly", 
                       when(col("is_hourly"), col("min_amount_float") * hours_per_year)
                       .otherwise(col("min_amount_float")))
    
    df = df.withColumn("max_amount_yearly", 
                       when(col("is_hourly"), col("max_amount_float") * hours_per_year)
                       .otherwise(col("max_amount_float")))
    
    df = df.drop("min_amount", "max_amount", "interval", "min_amount_float", "max_amount_float", "is_hourly")

    df = df.drop("emails", "job_url", "site", "company_url", "currency")

    df = df.withColumn("avg_salary_yearly", (col("min_amount_yearly") + col("max_amount_yearly")) / 2)

    df = df.dropna(subset=["avg_salary_yearly"])
    # creating a new column indicating senior or not
    df = df.drop("min_amount_yearly", "max_amount_yearly")
    df = df.withColumn(
        "is_senior",
        when(lower(col("title")).contains("senior"), 1).otherwise(0)
    )

    # creating a new column for more general title
    df = df.withColumn(
        "title_category",
        when(lower(col("title")).contains("scientist"), "Scientist")
        .when(lower(col("title")).contains("engineer"), "Engineer")
        .when(lower(col("title")).contains("developer"), "Developer")
        .when(lower(col("title")).contains("analyst"), "Analyst")
        .otherwise("Other")
    )

    # dealing with null values (probably some better way)
    df = df.na.drop(subset=["description"])
    df = df.na.fill({"is_remote": False})
    df = df.na.fill({"date_posted": '2024-02-10'})
    df = df.na.fill({"job_type": 'fulltime'})
    df = df.na.fill({"location": 'San Francisco, CA'})
    df = df.na.fill({"num_urgent_words": 0})

    # remove outliers for the plots
    companies_to_remove = ["Prophecy Games", "Exhibit Experience", "Trucadence LLC"]

    df = df.filter(~df.company.isin(companies_to_remove))

    df.write.parquet(output_path, mode='overwrite')



