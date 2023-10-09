from google.cloud import storage

def upload_blob(bucket_name, source_file_name, destination_blob_name, credentials_path):
    storage_client = storage.Client.from_service_account_json(credentials_path)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(f'File {source_file_name} uploaded to {destination_blob_name}.')

bucket_name = 'pricebook-etl-stage'
folder_name = 'testing/pricebook'
local_file_path = "C:\\Users\\mchan\\Downloads\\file1.csv"
credentials_path = "C:\\Users\\mchan\\Downloads\\key.json"

destination_blob_name = f'{folder_name}/bgl_output.csv'

upload_blob(bucket_name, local_file_path, destination_blob_name, credentials_path)
