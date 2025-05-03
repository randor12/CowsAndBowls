# Cows and Bulls

This is an example game of cows and bulls that can be played over the terminal. This uses Python. 

The goal of cows and bulls is to guess the correct 4 letter word.

A bull means a letter was correctly guessed in the correct position. 

A cow means a letter was correctly guessed in the incorrect position. 

You have 15 rounds. Good luck and enjoy!

# How to Play

To play this game, run the command `python main.py`. 

The required dependencies is listed in the requirements.txt file. This can be installed using `pip install -r requirements.txt`


## Configuration

You can set more rounds / specific answers if you want a more custom challenge. Just run 
`python main.py --maxTries # --answer word` where # is the max number of tries and word is the answer. Set the answer to "always" to have the word be randomized entirely for your run. Else the word will randomize daily by default. 