python
import streamlit as st
import pandas as pd
import boto3
import io

# Create an S3 client
s3_client = boto3.client("s3")

# Define S3 bucket details
bucket_name = "<your_bucket_name>"
raw_data_key = "data/raw_data.csv"
processed_data_key = "data/processed_data.csv"

# Define Athena client
athena_client = boto3.client("athena")

# Define the Athena database and table name
database_name = "<your_database_name>"
table_name = "<your_table_name>"

# Define Athena query
athena_query = "SELECT * FROM <your_table_name>"

# Get raw data from S3 and process
def process_data():
    # Get raw data from S3
    response = s3_client.get_object(Bucket=bucket_name, Key=raw_data_key)
    raw_data = response["Body"].read().decode("utf-8")
    df = pd.read_csv(io.StringIO(raw_data))
    
    # Process data here
    
    # Save processed data to S3
    buffer = io.StringIO()
    df.to_csv(buffer)
    s3_client.put_object(Bucket=bucket_name, Key=processed_data_key, Body=buffer.getvalue())
    st.write("Data processed and saved to S3")
    
# Display processed data from S3
def display_data():
    # Get processed data from S3
    response = s3_client.get_object(Bucket=bucket_name, Key=processed_data_key)
    data = response["Body"].read().decode("utf-8")
    df = pd.read_csv(io.StringIO(data))
    
    # Display data using Streamlit
    st.write(df)
    
# Run Athena query and display results
def run_athena_query():
    # Run Athena query
    query_execution = athena_client.start_query_execution(
        QueryString=athena_query,
        QueryExecutionContext={
            "Database": database_name
        },
        ResultConfiguration={
            "OutputLocation": "s3://<your_athena_results_bucket>/<your_athena_results_folder>/"
        }
    )
    # Get query execution ID
    query_execution_id = query_execution["QueryExecutionId"]
    # Wait for query to complete
    while True:
        query_execution = athena_client.get_query_execution(QueryExecutionId=query_execution_id)
        query_status = query_execution["QueryExecution"]["Status"]["State"]
        if query_status in ["SUCCEEDED", "FAILED", "CANCELLED"]:
            break
    # Display Athena query results using Streamlit
    if query_status == "SUCCEEDED":
        result_location = query_execution["QueryExecution"]["ResultConfiguration"]["OutputLocation"]
        result_response = s3_client.get_object(Bucket=bucket_name, Key=result_location.replace("s3://" + bucket_name + "/", ""))
        df = pd.read_csv(io.StringIO(result_response["Body"].read().decode("utf-8")))
        st.write(df)
    else:
        st.write("Query failed")
    
# Create Streamlit app
def main():
    st.title("Web Scraper Analyzer")
    
    # Define app menu
    menu_options = ["Process Data", "Display Data", "Run Athena Query"]
    menu = st.sidebar.selectbox("Select an option", menu_options)
    
    # Process data
    if menu == "Process Data":
        process_data()
    
    # Display data
    elif menu == "Display Data":
        display_data()
    
    # Run Athena query
    elif menu == "Run Athena Query":
        run_athena_query()
    
if __name__ == "__main__":
    main()
