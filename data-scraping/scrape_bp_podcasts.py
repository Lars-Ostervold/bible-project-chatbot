"""
Scrapes the Bible Project website for podcasts and downloads their transcripts or mp3 files.

Instructions:
1. Make sure you have the necessary dependencies installed: requests, BeautifulSoup, selenium.
2. Download the Chrome WebDriver and place it in the same directory as this script. (or globally in your PATH)
3. Set the 'url' variable to the URL of the page with the podcasts.
4. Run the script.

This script uses Selenium to load the page and click the "Load More" button until all podcasts are loaded.
It then uses BeautifulSoup to parse the page and extract the podcast titles and links.
For each podcast, it checks if a transcript is available. If yes, it downloads the transcript.
If not, it downloads the mp3 file.

The downloaded files are saved in the 'resources' directory, under 'audio' for mp3 files and 'transcripts' for transcripts.
The file names are generated based on the podcast titles, with special characters removed and spaces replaced with dashes.
"""

import requests
from bs4 import BeautifulSoup
import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re


def get_podcasts_loaded(driver_source):
    soup = BeautifulSoup(driver_source, 'html.parser')
    podcasts = soup.find_all("a", class_="cardpodcast cardpodcast-episode cardpodcast-type-horizontal-narrow")
    return len(podcasts)

def get_last_podcast_loaded(driver_source):
    soup = BeautifulSoup(driver_source, 'html.parser')
    podcasts = soup.find_all("a", class_="cardpodcast cardpodcast-episode cardpodcast-type-horizontal-narrow")
    last_podcast = podcasts[-1]
    return last_podcast['data-modal-meta-title']


def main():
    driver = webdriver.Chrome()

    # URL of the page with all the podcasts
    url = "https://bibleproject.com/podcasts/the-bible-project-podcast/"

    #Open the page in a browser
    driver.get(url)

    # Wait for the "Load More" button to become clickable
    wait = WebDriverWait(driver, 10)
    load_more_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "hero-podcast-subscribe-loadmore-button")))

    
    # Keep clicking the "Load More" button until it disappears. 
    # Try to click the button twice after waiting to make sure it's not just a loading issue.
    for i in range(1000):
        try:
            load_more_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "hero-podcast-subscribe-loadmore-button")))
            load_more_button.click() 
            print("Number of podcasts loaded is now: " + str(get_podcasts_loaded(driver.page_source)))
            time.sleep(0.5)
        except:
            print("Attempting backup method to load more podcasts")
            time.sleep(5)
            try:
                load_more_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "hero-podcast-subscribe-loadmore-button")))
            except:
                print("Backup failed")
                print("Number of podcasts loaded is now: " + str(get_podcasts_loaded(driver.page_source)))
                print("Last podcast loaded is: " + get_last_podcast_loaded(driver.page_source))
                break

    #Parse the driver page with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find all the podcast elements on the page. Podcast class pulled from the website.
    podcasts = soup.find_all("a", class_="cardpodcast cardpodcast-episode cardpodcast-type-horizontal-narrow")

    #Write podcast data to a file for debugging if needed
    with open("../resources/podcast-scrape-log.txt", "w") as file:
        #write total number of podcasts to file
        file.write("Total number of podcasts: " + str(len(podcasts)) + "\n\n")
        # Loop through each podcast
        for podcast in podcasts:
            # Get the podcast title. Title is in a class called 'cardpodcast-title' and is a child of the podcast element.
            title = podcast.find("div", class_="cardpodcast-title").text
            file.write(title + "\n")

            #Pull the link to the podcast. The link is in the href attribute of the podcast element.
            link = podcast["href"]
            file.write(link + "\n")

            #Load html from the podcast page. Use driver.
            driver.get(link)
            podcast_soup = BeautifulSoup(driver.page_source, 'html.parser')

            #Look for the transcript element, if found, download the transcript, otherwise download the mp3 file.
            transcript_element = podcast_soup.find("div", class_="grid-podcasts-toolbar-menuitem-icon transcript")
            
            #Take a string and convert it to something that can be used as a file name.
            def convert_to_file_friendly_format(title):
                # Remove characters that may cause issues
                title = re.sub(r'[^\w\s-]', '', title)
                # Convert to lowercase
                title = title.lower()
                # Replace spaces with dashes
                title = title.replace(' ', '-')
                return title
            
            def mp3_download(podcast_soup):
                mp3_element = podcast_soup.find("div", class_="grid-podcasts-toolbar-menuitem-icon download")
                mp3_link = mp3_element.parent["href"]
                mp3_response = requests.get(mp3_link)
                mp3_file_name = convert_to_file_friendly_format(title) + ".mp3"
                mp3_file_path = os.path.join("../resources/audio", mp3_file_name)

                with open(mp3_file_path, "wb") as f:
                    f.write(mp3_response.content)

                file.write("Mp3 found and downloaded" + "\n")

            if transcript_element is not None:
                # Download the transcript
                # Some transcript links have permission errors. If invalid download, we'll just download the mp3 file.
                try:
                    transcript_link = transcript_element.parent["href"]
                    if transcript_link.startswith('//'):
                        transcript_link = 'https:' + transcript_link
                    transcript_response = requests.get(transcript_link)
                    transcript_file_name = convert_to_file_friendly_format(title)
                    if transcript_link.endswith('.pdf'):
                        transcript_file_name += ".pdf"
                        transcript_file_path = os.path.join("../resources/transcripts", transcript_file_name)
                        with open(transcript_file_path, "wb") as f:
                            f.write(transcript_response.content)
                    else: 
                        transcript_file_name += ".txt"
                        transcript_file_path = os.path.join("../resources/transcripts", transcript_file_name)
                        with open(transcript_file_path, "w") as f:
                            f.write(transcript_response.text)
                    file.write("Transcript found and downloaded" + "\n")
                except:
                    mp3_download(podcast_soup)
                    file.write("Transcript download failed, mp3 downloaded instead" + "\n")

            else:
                # Download the mp3 file
                mp3_download(podcast_soup)

    driver.quit()

if __name__ == "__main__":
    main()