
import requests
from bs4 import BeautifulSoup
import os
import time
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

url_map = {}

def get_podcasts_loaded(driver_source):
    soup = BeautifulSoup(driver_source, 'html.parser')
    podcasts = soup.find_all("a", class_="cardpodcast cardpodcast-episode cardpodcast-type-horizontal-narrow")
    return len(podcasts)

def get_last_podcast_loaded(driver_source):
    soup = BeautifulSoup(driver_source, 'html.parser')
    podcasts = soup.find_all("a", class_="cardpodcast cardpodcast-episode cardpodcast-type-horizontal-narrow")
    last_podcast = podcasts[-1]
    return last_podcast['data-modal-meta-title']

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

    # Loop through each podcast
    for podcast in podcasts:
        # Get the podcast title. Title is in a class called 'cardpodcast-title' and is a child of the podcast element.
        title = podcast.find("div", class_="cardpodcast-title").text

        #Pull the link to the podcast. The link is in the href attribute of the podcast element.
        link = podcast["href"]

        #Let's just ignore the filename ending. We can now make a dictionary with the key
        #is the file name, first value is link, second value is title.
        
        #First we have to regenerate the file name from the link
        file_name = convert_to_file_friendly_format(title)

        #Now make the dictionary
        url_map[file_name] = [link, title]

    driver.quit()

    #Write the dictionary to a file
    with open("podcast_links.json", "w") as file:
        json.dump(url_map, file)

if __name__ == "__main__":
    main()