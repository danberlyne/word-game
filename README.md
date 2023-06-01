# Game instructions
Guess the word correctly to proceed to the next level. You have six chances to guess the word. Words start out at length four and increase by one with each level. There are ten levels in total.

If your guess contains a correct letter in the correct position, this letter will be revealed in lower case. All correct and incorrect letters in your guesses will be kept track of in a panel on the right.

This game uses American English by default.

# Changing the word list and/or dictionary
By default, The Word Game generates words using [mahsu's list of 5000 common words](https://github.com/mahsu/IndexingExercise/blob/master/5000-words.txt). This list is found in this package as the file `word_list.txt`. 

The Word Game also uses a dictionary to check whether the player's guesses are valid words. By default, the game uses the dictionary found in all Unix systems at `/usr/share/dict/words`. This list is found in this package as the file `dictionary.txt`.

If you wish, you may replace the default word list and/or dictionary with another of your choosing. Simply replace `word_list.txt` and/or `dictionary.txt` with a file of the same name containing your word list or dictionary, with each word on a separate line. All words containing capitals or non-letter characters are automatically removed by `word_game.py`.
