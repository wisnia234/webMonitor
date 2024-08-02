import os
from google.cloud import storage

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'ServiceKey_GoogleCloud.json'

storageClient = storage.Client()
bucketName = 'response_results_bucket'

def upload_to_bucket(blobName, filePath):

    bucket = storageClient.get_bucket(bucketName)
    blob = bucket.blob(blobName)
    blob.upload_from_filename(filePath)
    return blob