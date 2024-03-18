# Automated-Data-Pipeline (MSDS697 Final Project)

## Project Overview
Our project aimed to develop an automated data pipeline utilizing Airflow, MongoDB, and Spark to streamline the movement and processing of job market data. With a focus on roles relevant to our Master's curriculum, we collected data from leading job portals like LinkedIn, Glassdoor, and ZipRecruiter. The core objective was to provide actionable insights into the job market, enabling students and professionals to make informed decisions regarding their career paths.

## Learning Objectives
This project was designed to achieve several key learning objectives:
- **Airflow Utilization**: Master the use of Airflow to orchestrate complex data workflows, ensuring efficient data transfer and processing.
- **Database Management**: Gain hands-on experience with MongoDB, both in local environments and cloud deployments (MongoDB Atlas), to manage large datasets effectively.
- **Data Processing and Analysis**: Leverage Spark's powerful data processing capabilities to analyze job market trends and extract meaningful insights.
- **Cloud Deployment**: Understand the intricacies of deploying data pipelines in the cloud using Google Cloud Services, enhancing scalability and accessibility.

## Dataset and Goals
Our project utilized a rich dataset collected from three prominent job search portals: LinkedIn, Glassdoor, and ZipRecruiter. The data encompassed a wide range of fields, including job titles, company names, locations, and salary ranges, focusing specifically on positions like Data Analyst, Data Scientist, and Software Engineer.

The primary goal was to dissect the current job market landscape, identifying key trends and factors influencing job availability and compensation. By analyzing variables such as role, location, and remote work opportunities, we aimed to equip job seekers with the knowledge needed to navigate the market effectively and align their career aspirations with market realities.

## Technical Components & Workflow
![Airflow Pipeline](https://github.com/sheneric211/Automated-Data-Pipeline/assets/103718326/41cea7e1-ffb9-46ac-bb78-288553078d76)

### MongoDB Atlas
For our project, we leveraged MongoDB Atlas for its fully managed cloud database capabilities, providing us with scalability, security, and operational efficiency. Key features of our MongoDB Atlas setup include:
- **Cluster Creation**: We created a dedicated cluster in MongoDB Atlas, allowing us to manage our job market dataset effectively.
- **Data Management**: MongoDB's intuitive interface and robust features facilitated seamless data import, querying, and aggregation, enhancing our analysis process.
- **Security**: MongoDB Atlas provided comprehensive security features, including network isolation, encryption, and fine-grained access control, ensuring our data's integrity and safety.

### Google Cloud Storage (GCS)
Google Cloud Storage (GCS) played a pivotal role in our project for storing and managing our datasets securely in the cloud. Our GCS integration involved:
- **Bucket Configuration**: We set up a GCS bucket for efficient data storage, with carefully configured access permissions to ensure project security.
- **Airflow Integration**: Our Airflow pipeline was designed to interact seamlessly with GCS, facilitating smooth data transfers between GCS and our processing environments.
- **Scalability and Security**: GCS offered a scalable infrastructure and robust security measures, including data encryption and identity and access management, crucial for handling sensitive job market data.

## Analysis & Insights

By employing PySpark queries, we have extracted a wealth of valuable data to aid in the job search process. Recognizing that salary is a significant motivator for many individuals, our initial step involved identifying job titles that typically offer the highest pay. Our analysis revealed that data engineers command the highest salaries, closely followed by data scientists, with analysts generally earning the least, as illustrated in the figure below. Further analysis on salary distribution by job modality showed that, on average, remote positions offer salaries that are less than half those of at least hybrid roles. This discrepancy is partly due to the data being derived from 301 remote and 1,486 non-remote job postings, highlighting a noteworthy trend: the current market offers fewer opportunities for fully remote positions. This scarcity of remote job listings is an intriguing insight in itself suggesting that if desired, finding fully remote roles may present additional challenges in today's job market.

<img width="863" alt="Figure 1" src="https://github.com/sheneric211/Automated-Data-Pipeline/assets/103718326/17a57ff5-ca6c-46a1-a208-99270eae823c">

## Visualizations & Artifacts

<img width="992" alt="Screenshot 2024-03-17 at 5 47 07 PM" src="https://github.com/sheneric211/Automated-Data-Pipeline/assets/103718326/4fc2d173-08b4-4ee5-a7f9-7926f5aaa6f4">


<img width="918" alt="Screenshot 2024-03-17 at 5 47 14 PM" src="https://github.com/sheneric211/Automated-Data-Pipeline/assets/103718326/b016d59f-2397-4b6f-b0ab-ef1c099a8dda">


<img width="919" alt="Screenshot 2024-03-17 at 5 47 22 PM" src="https://github.com/sheneric211/Automated-Data-Pipeline/assets/103718326/b442f753-c0c1-42c8-8801-c6cb98a77f15">


<img width="787" alt="Screenshot 2024-03-17 at 5 47 26 PM" src="https://github.com/sheneric211/Automated-Data-Pipeline/assets/103718326/32f96cc2-d6b9-493b-b382-a6018270eb2c">

## Machine Learning Models
For this project we tried various different models, including random forests, simple linear regression, neural networks, and gradient-boosting trees. We found the “simpler” models actually performed better in terms of prediction accuracy compared to models like the neural network or random forests. The simplest linear regression model proved to be the best, which was definitely surprising, since we expected the more complex models to be able to capture more patterns from the data.

We utilized random forests for its ability to handle non-linear data and efficiency in training, however, its performance was suboptimal. Potentially due to overfitting or the high dimensionality of our feature space after encoding. We had a similar issue with the neural networks, however we did not extensively tune any of the hyperparameters or attempt to simplify the model, which is definitely something we can do next time.

The gradient boosting trees were only slightly worse than the simple linear regression in terms of predictive power. Looking back, it makes sense since some of our features would seem to have a linear relationship with the target variable (average_salary).

These results remind us of the importance of trying the simpler models first before moving on to the more complex ones. We should also explore the data more in the EDA section, this might have given us more hints about the potential relationship between our features and target variable.

## Conclusion
In conclusion, our exploration of the job market through the use of mongoDB, sparkSQL, and machine learning has provided us with some useful information about the relationships between job roles, job titles, and salaries.

Our machine learning models for salary prediction revealed surprising results. Contrary to the usual belief that more complex models yield better results, in this case we found that simpler models were actually more effective. This emphasizes the importance of carefully choosing a model based on actual data analysis on results, and that we should always try the simple models even as just a baseline.

While our approach was thorough, we understand that our limited data size might limit our findings. We also missed the opportunity to build some more interesting models and applications. We initially had the idea of using a model that takes in your resume and returns similar job postings, using embeddings of the descriptions and some sort of similarity measure. Though we were not able to accomplish that this time around, we would love to give this another try in the next module!

## Installation & Usage
### Required Libraries
```
pip install airflow[google] pymongo pyspark matplotlib seaborn joblib
```

### Airflow Setup
```
# Set up the environmental variable
# You would put those exports under .bash_profile or .zshrc
export AIRFLOW_HOME={path/to/github/repo}/airflow
export AIRFLOW_CONFIG={path/to/github/repo}/config/airflow.cfg

export AIRFLOW_CONN_GOOGLE_CLOUD_DEFAULT='{
    "conn_type": "google_cloud_platform",
    "extra": {"key_path": "{path/to/project}/credentials.json",
    "scope": "https://www.googleapis.com/auth/cloud-platform",
    "project": "airflow",
    "num_retries": 5}}'

# run in a terminal
### initialize airflow db
airflow db migrate
# or
# airflow db init

### create user
### id: admin, password: admin
airflow users create --role Admin --username admin --email admin --firstname admin --lastname admin --password admin

### start webserver
### endpoint defined in config/airflow.cfg
### default: http://localhost:8080
airflow webserver

# run in another terminal
### run scheduler
airflow scheduler
```

### Parameter Setup
```
params={
        'gcs_bucket_name' : 'msds697-jobs', # bucket name where your input data is located
        'gcs_input_dir_path' : 'jobs', # path to the file from your bucket
        'output_dir_path' : '/tmp', # directory path for your artifacts (location for outputs)
        'mongodb_host' : 'localhost',
        'mongodb_port' : '27017',
        'mongodb_database' : 'msds697',
        'mongodb_collection' : 'jobs'
    }
```

# Contributers
- [Eric Shen](https://github.com/sheneric211) - Machine Learning Models & Data Analysis & MongoDB Atlas
- [Inseong Han](https://github.com/EthanHistory) - Airflow
- [Evan Turkon](https://github.com/eJturkon) - GCS
- [Aditya Nair](https://github.com/adityanair98) - Data analysis
- [Jeffrey Chen](https://github.com/chenjiefei) - Data analysis
