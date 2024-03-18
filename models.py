def simple_linear_regression(**kwargs):
    import os
    # import joblib

    from pyspark.sql import SparkSession
    from pyspark.ml.regression import LinearRegression
    from pyspark.ml.evaluation import RegressionEvaluator
    from pyspark.ml.feature \
        import CountVectorizer, IDF, Tokenizer
    
    input_path = kwargs['input_path']
    output_path = kwargs['output_path']

    spark = SparkSession.builder \
        .appName("random_forest") \
        .config("spark.executor.memory", "3g") \
        .config("spark.executor.memoryOverhead", "512m") \
        .config("spark.driver.memory", "4g") \
        .config("spark.default.parallelism", "100") \
        .getOrCreate()

    df = spark.read.parquet(input_path)

    tokenizer = Tokenizer(inputCol="description", outputCol="words")
    df_words = tokenizer.transform(df)
    cv = CountVectorizer(inputCol="words", outputCol="features", binary=True)
    cv_model = cv.fit(df_words)
    df_features = cv_model.transform(df_words)

    train_data, test_data = df_features.randomSplit([0.8, 0.2], seed=0)

    lr = LinearRegression(featuresCol='features', labelCol='avg_salary_yearly')
    lr_model = lr.fit(train_data)

    # Make predictions on the test data
    lr_predictions = lr_model.transform(test_data)

    lr_predictions.select("avg_salary_yearly", "prediction").show(5)

    # Initialize evaluator with RMSE metric
    rmse_evaluator = RegressionEvaluator(labelCol='avg_salary_yearly', predictionCol='prediction', metricName='rmse')

    # Compute RMSE on test data
    lr_rmse = rmse_evaluator.evaluate(lr_predictions)
    print('Linear Regression RMSE:', lr_rmse)

    with open(os.path.join(output_path, "slr_model_evaluation.txt"), "w") as file:
        print("Root Mean Squared Error (RMSE) on test data = %g" % lr_rmse, file=file)

def random_forest(**kwargs):
    import os
    # import joblib

    from pyspark.sql import SparkSession

    from pyspark.ml.regression import RandomForestRegressor
    from pyspark.ml.evaluation import RegressionEvaluator
    from pyspark.ml.feature \
        import CountVectorizer, IDF, Tokenizer

    input_path = kwargs['input_path']
    output_path = kwargs['output_path']

    spark = SparkSession.builder \
        .appName("random_forest") \
        .config("spark.executor.memory", "3g") \
        .config("spark.executor.memoryOverhead", "512m") \
        .config("spark.driver.memory", "4g") \
        .config("spark.default.parallelism", "100") \
        .getOrCreate()

    df = spark.read.parquet(input_path)

    tokenizer = Tokenizer(inputCol="description", outputCol="words")
    df_words = tokenizer.transform(df)
    cv = CountVectorizer(inputCol="words", outputCol="features", binary=True)
    cv_model = cv.fit(df_words)
    df_features = cv_model.transform(df_words)

    train_data, test_data = df_features.randomSplit([0.8, 0.2], seed=0)

    rf = RandomForestRegressor(featuresCol="features", labelCol="avg_salary_yearly")
    rf_model = rf.fit(train_data)

    predictions = rf_model.transform(test_data)

    # Evaluate the model using RMSE
    evaluator = RegressionEvaluator(
        labelCol="avg_salary_yearly",
        predictionCol="prediction",
        metricName="rmse"
    )

    # Calculate RMSE
    rmse = evaluator.evaluate(predictions)
    
    with open(os.path.join(output_path, "rf_model_evaluation.txt"), "w") as file:
        print("Root Mean Squared Error (RMSE) on test data = %g" % rmse, file=file)

    # joblib.dump(rf_model, os.path.join(output_path, 'random_forest_model.joblib'))
