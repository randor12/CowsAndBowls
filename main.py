import requests  # new import
import datetime  # new import
import random    # new import
import pandas as pd  # new import

# New list of candidate 4-letter words
df = pd.read_csv("four_letter_words_valid.csv")
word_list = df[df["word"].str.len() == 4]["word"].tolist()

def daily_random_word() -> str:
    """
    Generate a daily constant random 4-letter word.
    """
    today = datetime.date.today().strftime("%Y%m%d")
    random.seed(today)
    return random.choice(word_list)

def always_random_word() -> str:
    """
    Generate a random 4-letter word.
    """
    return random.choice(word_list)

def guess_the_word() -> str:
    """
    Ask the user to guess a word.
    :return: the user's guess
    """
    print("Please enter a word: ")
    user_input = input()
    return user_input

def check_word_exists(word: str) -> bool:
    """
    Check if a word exists using the Datamuse API.
    :param word: The word to check.
    :return: True if the word is found, False otherwise.
    """
    response = requests.get(f"https://api.datamuse.com/words?sp={word}&max=1")
    if response.ok:
        data = response.json()
        return bool(data) and data[0].get("word", "").lower() == word.lower()
    return False

def check_guess(user_input: str, answer: str) -> tuple:
    """
    Check the user's guess against the answer using frequency counts.
    :param user_input: The user's guess
    :param answer: The correct answer
    :return: the number of correct letters in the correct position and the number of correct letters in the wrong position
    """
    correct_position = 0
    wrong_position = 0
    guess_freq = {}
    answer_freq = {}
    for i in range(min(len(user_input), len(answer))):
        if user_input[i] == answer[i]:
            correct_position += 1
        else:
            answer_freq[answer[i]] = answer_freq.get(answer[i], 0) + 1
            guess_freq[user_input[i]] = guess_freq.get(user_input[i], 0) + 1
    for letter in guess_freq:
        wrong_position += min(guess_freq[letter], answer_freq.get(letter, 0))
    return correct_position, wrong_position

def is_quit_command(user_input: str) -> bool:
    """
    Check if the user input is a quit command.
    :param user_input: The user's input
    :return: True if the input is a quit command, False otherwise
    """
    return user_input == "opt" or user_input == "q"

def welcome_message(answer,maxTries) -> None:
    """
    Display a welcome message.
    """
    print("Welcome to the game, Cows and Bulls!")
    print("You have to guess the word.")
    print("The word is", len(answer), "letters long.")
    print("You can quit the game by typing 'opt' or 'q'.")
    print("The word is not a proper noun.")
    print("The word is not a verb.")
    print("The word is not a plural.")
    print("You have", maxTries, "tries.")
    print("Good luck!")

def print_round_info(roundNumber: int, maxTries: int) -> None:
    """
    Print the round information.
    """
    print("\n")  # add spacing
    print("Round:", roundNumber + 1)                # show upcoming round
    print("You have", maxTries - roundNumber, "tries left.")  # tries left before a valid guess

def main(maxTries: int=15, answer: str="random") -> None:
    """
    Main function to run the game.
    """
    if maxTries < 1:
        print("Maximum tries must be at least 1.")
        return
    if is_quit_command(answer):
        print("The answer cannot be a quit command.")
        return
    guesses = []
    # Use daily random word if the default answer is in place.
    if answer == "random":
        answer = daily_random_word()
    if answer == "always":
        answer = always_random_word()
    answer = answer.lower()
    quit = False
    win = False
    roundNumber = 0
    welcome_message(answer, maxTries)
    while not quit:
        print_round_info(roundNumber, maxTries)
        user_input = guess_the_word()
        user_input = user_input.lower()
        if is_quit_command(user_input):
            print("You quit the game.")
            quit = True
            break
        if user_input == "":
            print("You must enter a word.")
            continue  # do not count as a round
        if not check_word_exists(user_input):
            print("Invalid word. Please try again.")
            continue  # do not count as a round
        if user_input in guesses:
            print("You already guessed that word. Please try again.")
            continue
        if len(user_input) != len(answer):
            print("The word must be", len(answer), "letters long.")
            continue
        if not user_input.isalpha():
            print("The word must contain only letters.")
            continue
        guesses.append(user_input)
        roundNumber += 1  # count only valid guesses
        if roundNumber > maxTries:
            print("You lose! The answer was:", answer)
            quit = True
            break
        if user_input == answer:
            win = True
            quit = True
        else:
            correct_position, wrong_position = check_guess(user_input, answer)
            if correct_position == len(answer):
                win = True
                quit = True
            print("Bulls:", correct_position)
            print("Cows:", wrong_position)
    if win:
        print("You win! The word was:", answer + "!")

if __name__ == '__main__':
    # parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(description="Cows and Bulls game.")
    parser.add_argument("--maxTries", type=int, default=15, help="Maximum number of tries")
    parser.add_argument("--answer", type=str, default="random", help="The answer to guess. Use 'random' for a daily random word or 'always' for a random word.")
    args = parser.parse_args()
    # run the game with command line arguments
    main(maxTries=args.maxTries, answer=args.answer)