'''
Downloads PDFS of the scripts from Bible Project's videos. 
Files are PDFs, so need to convert to txt with the pdf_to_txt.py script afterwards.
Script is the same as scrape_bp_script_refs.py, but with different file paths. I just 
didn't want to rework the logic to make it more modular. :)
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import requests
import re
import os

from supabase import create_client, Client
url: str = os.environ.get('SUPABASE_URL')
key: str = os.environ.get('SUPABASE_KEY')
supabase: Client = create_client(url, key)

#Take a string and convert it to something that can be used as a file name.
def convert_to_file_friendly_format(title):
    # Remove characters that may cause issues
    title = re.sub(r'[^\w\s-]', '', title)
    # Convert to lowercase
    title = title.lower()
    # Replace spaces with dashes
    title = title.replace(' ', '-')
    return title

def main():
    # Create a new instance of the Firefox driver
    driver = webdriver.Chrome()

    # Go to the website
    driver.get("https://bibleproject.com/downloads/study-notes/")

    wait = WebDriverWait(driver, 10)
    first_card = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'download-bundles-card')))

    #Get all cards with Selenium bc we need to click on them
    cards = driver.find_elements(By.CLASS_NAME, 'download-bundles-card')


    #The downloads are interesting here. First there's a popout windows that appears with a download link.
    #However, that is an indirect download link. So we have to first go to that link, then we get redirected
    #to the actual PDF download link. We can then download the PDF from that link.
    for card in cards:

        # Click on the card
        card.click()

        #Since the next card has the same class name, we need to wait for the popout window to appear before we can click on the next card
        #Otherwise the next line just runs immediately and we get a StaleElementReferenceException
        time.sleep(2)

        # Wait for the popout window to appear
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'resource-popout-button')))

        #Get the link for the redirect
        download_page_link = driver.find_element(By.CLASS_NAME, 'resource-popout-button').get_attribute("href")
        
        #Open a new driver to go get the redirect link
        url_fetcher_driver = webdriver.Chrome()
        url_fetcher_driver.get(download_page_link)
        time.sleep(2) #Give the page time to load

        #Now get the actual pdf link
        pdf_url = url_fetcher_driver.current_url
        url_fetcher_driver.quit()

        # Download the PDF file
        download_contents = requests.get(pdf_url)

        #Get the file name from the card children
        div_child = card.find_element(By.TAG_NAME, "div")
        img_child = div_child.find_element(By.TAG_NAME, "img")
        title = convert_to_file_friendly_format(img_child.get_attribute("alt")) + ".pdf"

        download_file_path = '../resources/study-notes/' + title

        #If file already exists, skip it
        if os.path.exists(download_file_path):
            print("Transcript for " + title + " already exists. Skipping.")
            continue

        with open(download_file_path, 'wb') as f:
            print("Downloading " + title + "...")
            f.write(download_contents.content)

        #Close the popout window
        close_button = driver.find_element(By.CLASS_NAME, 'popout-modal-close')
        close_button.click()

        print("Closed popout window and moving to next card.")

    # Close the driver
    driver.quit()

#TODO: I should rewrite this whole script to use send data to Supabase, but for now I'm just going to
#copy the bits I need and then upload the thumbnails.
def get_thumbnails():

    response = requests.get("https://bibleproject.com/downloads/study-notes/")

    soup = BeautifulSoup(response.text, 'html.parser')

    img_tags = soup.find_all("img")

    # Extract the src attribute from each img tag
    image_links = [img['src'] for img in img_tags if 'src' in img.attrs]

    image_alts = [img['alt'] for img in img_tags if 'alt' in img.attrs]

    for i in range(len(image_alts)):
        image_alts[i] = convert_to_file_friendly_format(image_alts[i])
        image_alts[i] += "-study-notes"

    for i in range(len(image_links)):
        if image_links[i].startswith('//'):
            image_links[i] = 'https:' + image_links[i]
        if 'w-' in image_links[i]:
            image_links[i] = image_links[i][:-6]

    for i in range(len(image_links)):
        data, count = supabase.table('source-links')\
            .update({'thumbnail_url': image_links[i]})\
            .eq('file_name', image_alts[i])\
            .execute()

        if data[1]:
            print(f"Thumbnail for {image_alts[i]} updated to {image_links[i]}")
        else:
            print(f"We didn't find a file_name match for {image_alts[i]}.")