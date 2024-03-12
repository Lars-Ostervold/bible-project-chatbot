
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import requests
import re
import os
import json

study_notes_links = {}

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

        #Get the file name from the card children
        div_child = card.find_element(By.TAG_NAME, "div")
        img_child = div_child.find_element(By.TAG_NAME, "img")
        title = img_child.get_attribute("alt") + " Study Notes"

        download_file_path = '../resources/study-notes/' + convert_to_file_friendly_format(title)

        link = 'https://bibleproject.com/downloads/study-notes/'

        study_notes_links[download_file_path] = [link, title]


        #Close the popout window
        close_button = driver.find_element(By.CLASS_NAME, 'popout-modal-close')
        close_button.click()

        print("Closed popout window and moving to next card.")

    # Close the driver
    driver.quit()

    with open('study_notes_links.json', 'w') as f:
        json.dump(study_notes_links, f)


if __name__ == "__main__":
    main()