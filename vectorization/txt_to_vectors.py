'''
UNUSED IN FINAL PROJECT.
I was playing around with spaCy's en-core-web-md model to vectorize the text files in the resources folder.
Then I saw that LangChain has its own vectorization process, so I didn't use this script.
'''
import spacy
import os
import numpy as np 

nlp = spacy.load('en_core_web_md')

def vectorize_text(file_path):
    #Some encodings don't work for certain files. I didn't figure out why.
    #Just use a try/except block
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
    except:
        with open(file_path, 'r') as file:
            text = file.read()
    doc = nlp(text)
    return doc.vector


resources_path = '../resources'
vectorization_path = '.'

for subfolder in os.listdir(resources_path):
    subfolder_path = os.path.join(resources_path, subfolder)
    
    if os.path.isdir(subfolder_path):
        for file_name in os.listdir(subfolder_path):
            if file_name.endswith('.txt'):
                file_path = os.path.join(subfolder_path, file_name)
                vector = vectorize_text(file_path)
                
                # Create a corresponding subfolder in /vectorization if it doesn't exist
                vector_subfolder_path = os.path.join(vectorization_path, subfolder)
                os.makedirs(vector_subfolder_path, exist_ok=True)
                
                # Check if the .npy file already exists
                vector_file_path = os.path.join(vector_subfolder_path, file_name.replace('.txt', '.npy'))
                if not os.path.exists(vector_file_path):
                    # Save the vector as a .npy file
                    np.save(vector_file_path, vector)
                else:
                    print(vector_file_path + " already exists. Skipping.")
