import boto3
import pandas as pd
from datetime import datetime
import io

def lambda_handler(event, context):
    
    # Set up S3 client
    s3 = boto3.client('s3')
    
    # Get the input file name and bucket name from the event
    file_obj = event["Records"][0]
    bucket_name = file_obj['s3']['bucket']['name']
    file_name = file_obj['s3']['object']['key']
    
    # Load the CSV file into a pandas dataframe
    obj = s3.get_object(Bucket=bucket_name, Key=file_name)
    df = pd.read_csv(io.BytesIO(obj['Body'].read()))
    
    # Drop rows with null values in specified columns
    df = df.dropna(subset=['column_1', 'column_2'])
    
    # Add a new column with the current timestamp value
    df['new_column'] = datetime.now()
    
    # Convert the cleaned dataframe back to CSV format
    cleaned_csv = df.to_csv(index=False)
    
    # Set up the output S3 bucket name and file name
    output_bucket = 'your-output-bucket'
    output_file_name = 'cleaned_file.csv'
    
    # Upload the cleaned CSV file to the output S3 bucket
    s3.put_object(Bucket=output_bucket, Key=output_file_name, Body=cleaned_csv)
    
    # Delete the original CSV file from the input bucket
    s3.delete_object(Bucket=bucket_name, Key=file_name)
    
    return {
        'statusCode': 200,
        'body': 'CSV file cleaned and moved to output S3 bucket!'
    }