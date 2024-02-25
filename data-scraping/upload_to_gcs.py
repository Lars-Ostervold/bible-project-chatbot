"""
Uploads everything from the resources/audio directory to the bp-audio bucket in Google Cloud Storage.

Needs "GOOGLE_APPLICATION_CREDENTIALS" environment variable to be set to the path of the JSON file 
with the service account key.
"""
import os
from google.cloud import storage
from dotenv import load_dotenv

load_dotenv()

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )

def upload_all_blobs():
    bucket_name = "bp-audio"

    # Directory containing the files to be uploaded
    directory_name = r"..\resources\audio"

    # List all files in the directory
    files = os.listdir(directory_name)
    
    # Upload all files
    for file_name in files:
        source_file_name = os.path.join(directory_name, file_name)
        destination_blob_name = file_name
        upload_blob(bucket_name, source_file_name, destination_blob_name)

def transcribe_audio():
    from google.cloud import speech_v1p1beta1 as speech

    storage_client = storage.Client()

    # Create a Speech-to-Text client.
    speech_client = speech.SpeechClient()

    # Get a list of all of the files in the Cloud Storage bucket.
    bucket_name = "bp-audio"
    blobs = storage_client.list_blobs(bucket_name)
    

    # For each file, transcribe the file and generate a .txt file.
    for blob in blobs:
        # Transcribe the file.
        audio = speech.RecognitionAudio(uri="gs://" + bucket_name + "/" + blob.name)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.MP3,
            sample_rate_hertz=44100,
            language_code="en-US",
        )
        #Perform the long running operation
        print("Transcribing " + blob.name + "...")
        operation = speech_client.long_running_recognize(config=config, audio=audio)
        response = operation.result(timeout=3600)

        # Generate a .txt file.
        with open(blob.name + ".txt", "w") as f:
            for result in response.results:
                f.write(result.alternatives[0].transcript + "\n")
        #end the loop on first iteration for testing purposes. Print name of file and break loop
        print("Transcription of " + blob.name + " complete.")
        break

transcribe_audio()