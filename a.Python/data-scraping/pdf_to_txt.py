from PyPDF2 import PdfReader

def pdf_to_txt(pdf_path, txt_path):
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PdfReader(pdf_file)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        with open(txt_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(text)

#Let's make a loop that will transcribe all the pdfs in the transcripts folder, then
#make a .txt with the same name in the same folder. Change path to the folder.
            
import os

folder_path = '../resources/script-refs/'
            
for file in os.listdir(folder_path):
    if file.endswith('.pdf'):
        print("Converting " + file + " to .txt...")
        #Check if .txt already exists, if it does, skip this file
        if os.path.exists(folder_path + file.replace('.pdf', '.txt')):
            print("Transcript for " + file + " already exists. Skipping.")
            continue
        pdf_to_txt(folder_path + file, folder_path + file.replace('.pdf', '.txt'))
        print("Conversion of " + file + " complete.")
