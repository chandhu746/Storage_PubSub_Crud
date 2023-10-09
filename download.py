from flask import Flask, render_template, request, jsonify
from google.cloud import storage

app = Flask(__name__)

def download_blob(bucket_name, source_blob_name, destination_file_name, credentials_path):
    storage_client = storage.Client.from_service_account_json(credentials_path)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    blob.download_to_filename(destination_file_name)

    print(f'File {source_blob_name} downloaded to {destination_file_name}.')

@app.route('/')
def index():
    return render_template('download.html')

@app.route('/download', methods=['POST'])
def download():
    # Getting data from form
    bucket_name = request.form.get('bucket_name')
    folder_name = request.form.get('folder_name')
    file_name = request.form.get('file_name')

    local_file_path = "C:\\Users\\mchan\\Downloads\\file4.csv"
    credentials_path = "C:\\Users\\mchan\\Downloads\\key.json"

    source_blob_name = f'{folder_name}/{file_name}'

    download_blob(bucket_name, source_blob_name, local_file_path, credentials_path)

    return jsonify({'message': 'File downloaded successfully'})

if __name__ == '__main__':
    app.run(debug=True)
