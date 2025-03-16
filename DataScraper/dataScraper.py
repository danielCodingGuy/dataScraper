#Data simple data scraper made in python with BeautifulSoup that saves scraped data to the text file.
#author: danielCodingGuy

import requests
from bs4 import BeautifulSoup

#Simple input where user pastes the link to the page he wants to scrape data from.
url = input("Paste the link to the page here:")

try:
    #Sending HTTP request.
    response = requests.get(url)

    #Checking if the request succeded.
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        #In this example we are scraping titles from the page, feel free to change it to whatever you want.
        titles = soup.find_all("h2")
        
        #Saving the data to the text file.
        if titles:
            with open("scraped_data.txt", "w", encoding="utf-8") as file:
                file.write(f"Titles from the site you have chosen: {url}\n\n")
                for idx, title in enumerate(titles, 1):
                    title_text = title.get_text(strip=True)
                    print(f"{idx}. {title_text}")
                    file.write(f"{idx}. {title_text}\n")
            print("\n Data has been saved in file 'scraped_data.txt'.")

        else:
            print("Haven't found any titles. Check the HTML selector and try again.")

    else:
        print(f"Ocurred an error while downloading the site. Status code: {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"Connection error: {e}")