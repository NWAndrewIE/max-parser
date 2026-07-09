"""
A program for scraping images from the russian national messenger MAX
Possible variants of links: 64*43=(2^6)^43=2^258=~4.6e77 
"""
"""    (fuck that shit and VK!)
________________█████       
 ______________██____██
 ______________██_██_██
 ______________██____██
 ______________██____██
 ______________██____██
 __________██████____██████
 ________██    ██____██    ████
 ________██    ██____██    ██  ██
 ██████__██    ██    ██    ██   ██
 ██    ████                ██    ██
 ██      ██______________________██
 __██    ██______________________██
 ___███  ██______________________██
 ____██                          ██
 _____███                        ██
 ______██                      ███
 _______███                    ██
 ________██                    ██
 _________███                ███
 __________██                ██
"""

import os, logging, random, requests
from time import sleep

# example: https://i.oneme.ru/i?r=BTE2sh_eZW7g8kugOdIm2Not5x-NU1dtPrcz-J_uAAH38kX7rfYAhZiNpfCTjwQmWO8 (67 symbs)
test_part = "5x-NU1dtPrcz-J_uAAH38kX7rfYAhZiNpfCTjwQmWO8"

ONEME_FILES_PATH = "https://i.oneme.ru/i?r=BTE2sh_eZW7g8kugOdIm2Not"    # identical for all files, only the last part changes
MAIN_DIRECTORY = "max_parser"
FILES_DIRECTORY = os.path.join(MAIN_DIRECTORY, "max_files")
LOG_FILE = "maxparserlog.txt"
ALPHABET = "abcdefghijklnmopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
INVALID_SIZE = [0, 503, 5082, 4939, 4940, 4941, 12003, 5556]

def create_folder(folder_name: str) -> None:
    """
    Creates a folder if it doesn't exist. If it already exists, does nothing.
    
    :param folder_name: The name of the folder to create.
    :type folder_name: str
    """
    os.makedirs(folder_name, exist_ok=True)

def check_link(link: str) -> bool:
    """
    Checks if a link is valid by sending a HEAD request and checking the status code.

    :param link: The URL to check.
    :type link: str
    :return: True if the link is valid (status code 200), False otherwise.
    :rtype: bool
    """
    logging.info(f"Checking link: {link}")
    print(f"Checking link: {link}")
    try:
        response = requests.head(link)
        return True if response.status_code == 200 else False
    except requests.RequestException as e:
        logging.error(f"Error checking link: {link} - {e}")
        print(f"Error checking link: {link} - {e}")
        return False

def download_image(link: str) -> None:
    """
    Downloads an image from the given link and saves it to the FILES_DIRECTORY if it's valid and not of an invalid size.
    
    :param link: The URL of the image to download.
    :type link: str
    """
    try:
        if check_link(link):
            response = requests.get(link)
            if response.status_code == 200:
                filename = os.path.join(FILES_DIRECTORY, link.split('=')[-1] + ".webp")
                if len(response.content) not in INVALID_SIZE:
                    with open(filename, 'wb') as f:
                        f.write(response.content)
            else:
                logging.error(f"Failed to download: {link} - Status code: {response.status_code}")
                print(f"Failed to download: {link} - Status code: {response.status_code}")
    except requests.RequestException as e:
        logging.error(f"Error downloading image: {link} - {e}")
        print(f"Error downloading image: {link} - {e}")

if __name__ == "__main__":
    downloaded = 0
    create_folder(MAIN_DIRECTORY)
    create_folder(FILES_DIRECTORY)
    logging.basicConfig(filename=os.path.join(MAIN_DIRECTORY, LOG_FILE), level=logging.INFO, 
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("---------------------------------------")
    amount = int(input("Enter the amount of files to try to download: "))
    while downloaded < amount:
        random_string = ''.join(random.choices(ALPHABET, k=random.randint(42, 43)))
        link = ONEME_FILES_PATH + random_string
        # link = ONEME_FILES_PATH + test_part   # for testing purposes, to check if the program works correctly with a valid link
        if check_link(link):
            download_image(link)
            logging.info(f"Successfully downloaded: {link} as {random_string}.webp")
            print(f"Successfully downloaded: {link} as {random_string}.webp")
            downloaded += 1
        else:
            if requests.get(link).status_code == 400:
                logging.error(f"File not found: {link}")
                print(f"File not found: {link}")
            else:
                logging.error(f"Error accessing link: {link} - Status code: {requests.get(link).status_code}")
                print(f"Error accessing link: {link} - Status code: {requests.get(link).status_code}")
        sleep(0.1)  # To avoid overwhelming the server with requests
