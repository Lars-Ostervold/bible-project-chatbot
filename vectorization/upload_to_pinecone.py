'''
UNUSED IN FINAL PROJECT
Script iterates through folders in the vectorization directory and uploads the vectors to Pinecone.
Should be run after vectorization/txt_to_vectors.py
'''
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
import numpy as np
import os
import itertools

load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

#For initial setup, create a new index. Commented out after the first run, but kept for reference.
pc.create_index(
    name="bible-project-index",
    dimension=1536, #en-core-web-md vectors are 300-dimensional
    metric="cosine", #cosine similarity
    spec=ServerlessSpec(
        cloud="aws",
        region="us-west-2"
    ) 
)

#---------------------------------------------------------------
#Now we upload the vectors to Pinecone

index = pc.Index("bible-project-index")

#Pinecone docs recommend uploading vectors in batches
def chunks(iterable, batch_size=100):
    """A helper function to break an iterable into chunks of size batch_size."""
    it = iter(iterable)
    chunk = tuple(itertools.islice(it, batch_size))
    while chunk:
        yield chunk
        chunk = tuple(itertools.islice(it, batch_size))

def data_generator():
    for subfolders in os.listdir('.'):
        subfolder_path = os.path.join('.', subfolders)

        if os.path.isdir(subfolder_path):
            for file_name in os.listdir(subfolder_path):
                if file_name.endswith('.npy'):
                    file_path = os.path.join(subfolder_path, file_name)
                    vector = np.load(file_path)
                    yield (file_path.replace('\\', '/'), vector.tolist())

# Upsert data with 100 vectors per upsert request
for ids_vectors_chunk in chunks(data_generator(), batch_size=100):
    index.upsert(vectors=ids_vectors_chunk)
    