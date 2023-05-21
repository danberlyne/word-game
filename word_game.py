#!/usr/bin/env python3
# word_game.py - A word-guessing game

import sys, random
from pathlib import Path

# Removes illegal words from the word list
word_list_file = open('word_list.txt')
word_list = word_list_file.readlines()
word_list_file.close()
    
for line, word in enumerate(word_list):
    word_list[line] = word.rstrip('\n')

for line, word in enumerate(word_list):
    if word.isalpha() and word.islower():
        continue
    else:
        del word_list[line]

word_list_file = open('word_list.txt', 'w')
word_list_file.write('\n'.join(word_list))
word_list_file.close()

# Splits the word list into separate lists according to word length
level_word_lists = []

for i in range(9):
    level_word_lists.append([])
        
    for word in word_list:
        if len(word) == i + 4:
            level_word_lists[i].append(word)

# Main game loop
while True:
    print('=' * 50)
    print('''Welcome to The Word Game.

Guess the word correctly to proceed to the next level.
A correct letter in the correct position will be displayed in upper case.
A correct letter in the incorrect position will be displayed in lower case.''')
    print('=' * 50 + '\n')

    new_game = ''

    # Ten levels with word lengths starting at 4 and increasing by 1 each level
    for length in range(4,13):
        remaining_guesses = 6
        # Chooses a random word of length corresponding to the level
        word = random.choice(level_word_lists[length - 4])
        display = '%s ' * length
        revealed_letters = list(('_') * length)
        correct_guess = False
        print('LEVEL ' + str(length - 3))

        # Player has 6 guesses before game over
        while remaining_guesses > 0:
            # Prints letters the player has revealed so far
            print(display % tuple(revealed_letters))
            print(str(remaining_guesses) + ' guesses remaining')  
            guess = input().lower()

            if guess == word:
                correct_guess = True
                break
            elif len(guess) != length:
                print('Guess a word of length ' + str(length) + '.')
                continue
            elif not guess.isalpha():
                print('Guess must contain only letters.')
                continue
            else:
                word_letters = list(word)
                guessed_letters = list(guess)
                
                for i, letter in enumerate(guessed_letters):
                    
                    # If player guesses a correct letter in the correct position, reveals that letter in lower case
                    if letter == word_letters[i]:
                        revealed_letters.pop(i)
                        revealed_letters.insert(i, letter)
                    # If player guesses a correct letter in the incorrect position, displays as upper case
                    elif letter in word_letters:
                        revealed_letters.pop(i)
                        revealed_letters.insert(i, letter.capitalize())

            remaining_guesses -= 1
        
        if correct_guess == True and length == 13:
            while True:
                print('Congratulations! You have completed all levels. Play again? (y/n)')
                new_game = input()
                if new_game == 'y':
                    break
                elif new_game == 'n':
                    sys.exit()
                else:
                    continue
        elif correct_guess == True:
            print('Congratulations! You guessed correctly. Proceed to the next level.')
        else:
            break
    
    # If player completed all levels and chose to play again, restarts main game loop
    if new_game == 'y':
        continue

    # If player uses up all guesses, proceeds to 'game over' sequence
    while True:
        print(f'GAME OVER. The correct word was {word}. Try again? (y/n)')
        new_game = input()
        if new_game == 'y':
            break
        elif new_game == 'n':
            sys.exit()
        else:
            continue