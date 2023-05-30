# Game instructions
Guess the word correctly to proceed to the next level. You have six chances to guess the word. Words start out at length four and increase by one with each level. There are ten levels in total.

If your guess contains a correct letter in the correct position, this letter will be revealed in lower case. If your guess contains a correct letter in the incorrect position, this letter with be revealed in upper case.

This game uses American English by default.

# Changing the word list
By default, The Word Game uses [mahsu's list of 5000 common words](https://github.com/mahsu/IndexingExercise/blob/master/5000-words.txt). This list is found in this package as the file `word_list.txt`. 

If you wish, you may replace the default word list with another list of your choosing. Simply replace `word_list.txt` with a file of the same name containing your word list, with each word on a separate line. All words containing capitals or non-letter characters are automatically removed by `word_game.py`.