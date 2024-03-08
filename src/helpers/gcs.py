import logging
import os
import json
import blob


from google.cloud import storage

from flask import url_for, send_from_directory

# Set up Google Cloud Storage client
client = storage.Client()

def UploadGCS(FileBlob: blob) -> str:
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
        
        # Get the uploaded file
        uploaded_file = FileBlob

        # Create a new blob in the bucket
        blob = client.bucket(bucket_name).blob(uploaded_file.filename)

        # Upload the file
        blob.upload_from_file(uploaded_file)

        # Grab the public URL
        public_url = storage.get_public_url(blob)
        print(f"Upload Complete: {public_url}")

        # Redirect to the uploaded file
        return public_url

    except Exception as ex:
        logging.error(ex)
        return (f"Unable to upload to GCS: {ex}")



