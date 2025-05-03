import csv
import enchant

def load_words(filename="four_letter_words.csv"):
    with open(filename, "r") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # skip header
        return [row[0] for row in reader]

def validate_words(words):
    d = enchant.Dict("en_US")
    return [word for word in words if d.check(word)]

def write_to_csv(words, filename="four_letter_words_valid.csv"):
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["word"])
        for word in words:
            writer.writerow([word])
    print(f"CSV file '{filename}' created with validated words.")

if __name__ == "__main__":
    words = load_words()
    valid_words = validate_words(words)
    write_to_csv(valid_words)
    print(f"Number of valid words: {len(valid_words)}")
    print(f"Number of invalid words: {len(words) - len(valid_words)}")