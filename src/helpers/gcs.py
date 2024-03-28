import logging
import os

from google.cloud import storage

from flask import url_for, send_from_directory

# Set up Google Cloud Storage client
client = storage.Client()

def UploadGCS(filename: str) -> str:
    """
        This function uploads a file to a GCS bucket read from OS environment

        Args:
            FileBlob: String - File Blob For Upload
        Returns:
            String - Path to file
    """
    try:
        # Check for GCS Bucket ENV variable if missing rage quit
        if os.environ['GCS_BUCKET']:
            bucket_name = os.environ['GCS_BUCKET']
        else:
            logging.error("No GCS_BUCKET Environment variable set")
            return "No GCS_BUCKET Environment variable set"

        storage_client: storage.Client = storage.Client()
        bucket: storage.Bucket = storage_client.bucket(bucket_name)
        blob: storage.Blob = bucket.blob(filename.split("/")[-1])
        blob.upload_from_filename(filename)
        blob.make_public()
        public_url: str = blob.public_url
        print(f"Image uploaded to {public_url}")
        os.remove(filename)

        # Redirect to the uploaded file
        return public_url
       

    except Exception as ex:
        logging.error(ex)
        return (f"Unable to upload to GCS: {ex}")