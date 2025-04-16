#Data scraper made in python using BeautifulSoup that saves scraped data in file of users choice and allows filtering data which is scraped using keywords.
#author: danielCodingGuy

import requests
from bs4 import BeautifulSoup
import csv
import json

def get_page_content(url):
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"An error ocurred while downloading the site: {e}")
        return None
    
def scrape_titles(html):
    soup = BeautifulSoup(html, "html.parser")
    titles = [title.get_text(strip=True) for title in soup.find_all("h2")]
    return titles if titles else None

def filter_titles(titles, keyword=None):
    if keyword:
        titles = [title for title in titles if keyword.lower() in title.lower()]
    return list(set(titles))

def sort_titles(titles, method="alphabetically"):
    if method == "length":
        return sorted(title, key=len, reverse=True)
    return sorted(titles)

def save_to_file(titles, file_format="txt"):
    if not titles:
        print("Haven't found any matches to save.")
        return
    
    filename = f"scraped_data.{file_format}"

    if file_format == "txt":
        with open(filename, "w", encoding="utf-8") as file:
            file.write("\n".join(titles))
    elif file_format == "csv":
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Num", "Title"])
            for idx, title in enumerate(titles, 1):
                writer.writerow([idx, title])
    elif file_format == "json":
        with open(filename, "w", encoding="utf-8") as file:
            json.dump({"titles": titles}, file, ensure_ascii=False, indent=4)
    print(f"Data was saved to file: {filename}")

def main():
    url = input("Paste adress of the site you want to scrap: ")
    html = get_page_content(url)
    if not html:
        return
    
    titles = scrape_titles(html)
    if not titles:
        print("Haven't found any titles to save on this page.")
        return
    
    print("\nTitles found:")
    for idx, title in enumerate(titles, 1):
        print(f"{idx}.{title}")

    keyword = input("Write a keyword to find (Press ENTER to pass): ").strip()
    titles = filter_titles(titles, keyword)

    if not titles:
        print("No matches that match your filters.")
        return
    
    print("\nSorting options:")
    print("1. Alphabetically(by default)")
    print("2. By length(from the longest)")
    sort_choice = input("Choose the sorting option (1/2): ").strip()
    titles = sort_titles(titles, method="length" if sort_choice == "2" else "alphabetically")

    print("\nSave as:")
    print("1. txt")
    print("2. csv")
    print("3. json")
    format_choice = input("Choose saving format (1/2/3)").strip
    file_format = txt if format_choice == "1" else "csv" if format_choice == "2" else "json"

    save_to_file(titles, file_format)

if __name__ == "__main__":
    main()