import boto3
import psycopg2
import csv

s3 = boto3.client('s3')
redshift = psycopg2.connect(
    host='<redshift_host>',
    port='<redshift_port>',
    dbname='<redshift_database_name>',
    user='<redshift_username>',
    password='<redshift_password>'
)

def lambda_handler(event, context):
    # Get the S3 bucket and key for the CSV file
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    # Download the CSV file from S3
    csv_file = s3.get_object(Bucket=bucket, Key=key)['Body'].read().decode('utf-8').splitlines()
    
    # Open a cursor for the Redshift connection
    cursor = redshift.cursor()
    
    # Loop through each row in the CSV file and insert it into the Redshift table
    for row in csv.reader(csv_file):
        cursor.execute("INSERT INTO <redshift_table_name> (col1, col2, col3) VALUES (%s, %s, %s)", row)
    
    # Commit the changes to the Redshift database
    redshift.commit()
    
    # Close the cursor and database connection
    cursor.close()
    redshift.close()