
import sys

from awsglue.transforms import *

from awsglue.utils import getResolvedOptions

from awsglue.context import GlueContext

from awsglue.dynamicframe import DynamicFrame

from awsglue.job import Job

from pyspark.context import SparkContext

from pyspark.sql.functions import col

from pyspark.sql import SparkSession

# Create a GlueContext
glueContext = GlueContext(SparkContext.getOrCreate())

# Get arguments passed from the AWS Glue job
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

# Start a new AWS Glue job
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Load data from S3 bucket
input_dynamic_frame = glueContext.create_dynamic_frame_from_options(
    's3', {'paths': ['<your_s3_bucket_path_here>/raw_data.csv']},
    format='csv'
)

# Drop unused columns
clean_dynamic_frame =\
    input_dynamic_frame.drop_fields(['<unused_column_name_1>', '<unused_column_name_2>'])

# Filter data by specific criteria
filtered_dynamic_frame = clean_dynamic_frame.filter(frame=
    clean_dynamic_frame.toDF()
        .where(col('<column_name>').isin('<list_of_values>'))
)

# Convert dynamic frame to data frame
data_frame = filtered_dynamic_frame.toDF()

# Write data to Athena
glueContext.write_dynamic_frame.from_options(
    frame = DynamicFrame.fromDF(data_frame, glueContext, "<table_name>"),
    connection_type = "s3",
    connection_options = {
        "path": "<your_s3_bucket_path_here>/output/",
        "partitionKeys": ["<partition_column_name>"]
    },
    format = "parquet"
)

# Commit job and terminate
job.commit()
spark.quit()
