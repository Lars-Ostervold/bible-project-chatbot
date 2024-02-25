"""
Requests transcription of audio files in the Cloud Storage bucket "bp-audio" and writes the transcriptions to .txt files.

Needs "GOOGLE_APPLICATION_CREDENTIALS" environment variable to be set to the path of the JSON file 
with the service account key.
"""
import os
import concurrent.futures
from google.cloud import storage
from google.cloud import speech_v1p1beta1 as speech
from dotenv import load_dotenv

load_dotenv()

def transcribe_blob(blob):
    # Check if the transcript file already exists. If it does, skip this blob.
    if os.path.exists(r"..\resources\transcripts\\" + blob.name + ".txt"):
        print("Transcript for " + blob.name + " already exists. Skipping.")
        return

    # Transcribe the file.
    audio = speech.RecognitionAudio(uri="gs://" + bucket_name + "/" + blob.name)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=44100,
        language_code="en-US",
    )
    print("Transcribing " + blob.name + "...")
    operation = speech_client.long_running_recognize(config=config, audio=audio)
    response = operation.result(timeout=3600)

    # Generate a .txt file.
    with open(r"..\resources\transcripts\\" + blob.name + ".txt", "w") as f:
        for result in response.results:
            f.write(result.alternatives[0].transcript + "\n")

    print("Transcription of " + blob.name + " complete.")

def transcribe_audio():
    global bucket_name, speech_client  # Make these variables global so they can be accessed in transcribe_blob

    storage_client = storage.Client()

    # Create a Speech-to-Text client.
    speech_client = speech.SpeechClient()

    # Get a list of all of the files in the Cloud Storage bucket.
    bucket_name = "bp-audio"
    blobs = storage_client.list_blobs(bucket_name)

    # Create a thread pool and submit transcription tasks.
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(transcribe_blob, blobs)

transcribe_audio()