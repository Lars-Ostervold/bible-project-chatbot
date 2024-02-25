**Currently a work in progress, just updating the README as I go.**
Latest update - scraping script for podcasts completed. Audio files were converted to text using Google's speech-to-text before this PR.


# bible-project-chatbot
A chatbot that will answer questions from Bible Project material. Augmented with all podcasts, videos, study notes, and blog posts from Bible Project.

# Data Scraping
Files for data scraping are found in ./data-scraping. Podcasts, videos, study notes, and blog posts each have their own scraping function.
Transcripts were generated from .mp3 files by uploading to Google Cloud (see ./data-scraping/upload-to-gcs.py), then using their speech-to-text feature. 
If a transcript existed in .pdf form, it was converted to .txt with ./data-scraping/pdf-to-txt.py.

# Resources
This is where I stored all the files from webscraping. They are in subfolders based on the source. I deleted the audio files from the local repo (stored in Google Cloud) since it was a massive amount of data. There's also an 'images' subfolder for the frontend. The rest of the folders contain .txt files from the data scraping. I'll likely play around with vectorization schemes, so I'm holding on to the text files for now 😊.

# Vectorization
The script in this folder used Langchain_pinecone to vectorize the txt files and upload them to the Pinecone database. It's a 'first thing I got to work' situation and there's likely some tweaking I need to do for the vectorization scheme.