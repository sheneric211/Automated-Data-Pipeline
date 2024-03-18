from mongodb import mongodb

@mongodb
def types_of_job_postings(collection, **kwargs):
    import os
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    matplotlib.pyplot.ioff()

    output_path = kwargs['output_path']

    remote_count = collection.count_documents({ "is_remote": True })
    non_remote_count = collection.count_documents({ "is_remote": { "$ne": True } })
    labels = 'Remote Jobs', 'Non-Remote Jobs'
    sizes = [remote_count, non_remote_count]
    colors = ['gold', 'yellowgreen']
    explode = (0.1, 0) 

    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
    autopct='%1.1f%%', shadow=True, startangle=140)
    plt.title('Types of Job Postings')
    plt.axis('equal')
    plt.savefig(os.path.join(output_path, 'types_of_job_postings.png'))

@mongodb
def ds_job_postings_in_ffang(collection, **kwargs):
    import os
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    matplotlib.pyplot.ioff()

    output_path = kwargs['output_path']

    companies = ["Facebook/Meta", "Apple", "Amazon", "Netflix", "Google"]
    counts = []
    for _, company in enumerate(companies):
        if company == "Facebook/Meta":
            count = collection.count_documents({ "$or": [{ "company": { "$regex": "facebook", "$options": "i" } }, { "company": { "$regex": "meta", "$options": "i" } }] })
        else:
            count = collection.count_documents({ "company": { "$regex": company.lower(), "$options": "i" } })
        counts.append(count)

    plt.bar(companies, counts, color=['blue', 'red', 'green', 'purple', 'orange'])
    plt.xlabel('Company')
    plt.ylabel('Number of Postings')
    plt.title('Number of Data Science Related Job Postings at FAANG')
    plt.savefig(os.path.join(output_path, 'ds_job_postings_in_ffang.png'))

@mongodb
def proportion_of_relevant_postings(collection, **kwargs):
    import os
    import json
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    matplotlib.pyplot.ioff()

    output_path = kwargs['output_path']

    all_jobs_count = collection.count_documents({})
    pipeline = [
        {
            "$match": {
                "job_type": "fulltime",
                "$or": [
                    {
                        "interval": "yearly",
                        "min_amount": { "$gte": 100000 }
                    },
                    {
                        "interval": "hourly",
                        "min_amount": { "$gte": 50 }
                    }
                ]
            }
        }
    ]
    relevant_jobs = collection.aggregate(pipeline)
    relevant_jobs_count = len(list(relevant_jobs))
    labels = 'Relevant Jobs', 'Other Jobs'
    sizes = [relevant_jobs_count, all_jobs_count - relevant_jobs_count]
    colors = ['gold', 'yellowgreen']
    explode = (0.1, 0) 

    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
    autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')
    plt.title('Proportion of Relevant Postings ($100k/yr+, fulltime)')
    plt.savefig(os.path.join(output_path, 'proportion_of_relevant_postings.png'))


def average_salary(**kwargs):
    import os
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    matplotlib.pyplot.ioff()

    import seaborn as sns
    from pyspark.sql import SparkSession
    from pyspark.sql import functions as F

    input_path = kwargs['input_path']
    output_path = kwargs['output_path']

    spark = SparkSession.builder \
        .appName("visualization") \
        .getOrCreate()

    df = spark.read.parquet(input_path)

    avg_salary_by_title = df.groupBy("title_category").agg(
        F.avg("avg_salary_yearly").alias("average_salary")
    ).orderBy(F.col("average_salary").desc())

    avg_salary_by_title_pd = avg_salary_by_title.toPandas()

    sns.set(style="whitegrid")

    plt.figure(figsize=(10, 6))
    sns.barplot(x="average_salary", y="title_category", data=avg_salary_by_title_pd, palette="viridis")

    plt.title('Average Salary by Title Category')
    plt.xlabel('Average Salary')
    plt.ylabel('Title Category')

    plt.tight_layout()
    plt.savefig(os.path.join(output_path, 'average_salary.png'))

    top_20_companies = df.groupBy("company").agg(
        F.avg("avg_salary_yearly").alias("average_salary")
    ).orderBy(F.col("average_salary").desc()).limit(20)

    top_20_companies_pd = top_20_companies.toPandas()

    sns.set_theme(style="whitegrid")

    plt.figure(figsize=(10, 8))
    sns.barplot(x="average_salary", y="company", data=top_20_companies_pd, palette="coolwarm")

    plt.title('Top 20 Companies by Average Salary')
    plt.xlabel('Average Salary')
    plt.ylabel('Company')

    plt.tight_layout()
    plt.savefig(os.path.join(output_path, 'top_companies_by_salary.png'))