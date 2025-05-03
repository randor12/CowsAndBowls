import requests
import csv
from bs4 import BeautifulSoup

URL = "https://scrabble.collinsdictionary.com/word-lists/four-letter-words-in-scrabble/"

def get_four_letter_words(url: str):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")
    words = set()
    # Assuming words are within list items; adjust the selector if needed.
    for li in soup.find_all("li"):
        text = li.get_text(strip=True)
        if len(text) == 4 and text.isalpha():
            words.add(text.lower())
    return sorted(words)

def write_to_csv(words, filename="four_letter_words.csv"):
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["word"])
        for word in words:
            writer.writerow([word])
    print(f"CSV file '{filename}' created successfully.")

if __name__ == "__main__":
    word_list = get_four_letter_words(URL)
    write_to_csv(word_list)