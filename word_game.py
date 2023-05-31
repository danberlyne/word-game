#!/usr/bin/env python3
# word_game.py - A word-guessing game

import sys, random
from collections import defaultdict

# Word lengths for the first and last levels
min_length = 4
max_length = 13
# Number of guesses per level
guesses_per_level = 6

# Introduction sequence
def introduce_game():
    print('=' * 50)
    print('''Welcome to The Word Game.

Guess the word correctly to proceed to the next level.
A correct letter in the correct position will be displayed in lower case.
A correct letter in the incorrect position will be displayed in upper case to the right of the game board.

If you wish to quit at any point, type 'quit game'.''')
    print('=' * 50 + '\n')

# Returns `True` if `word` is a legal word
def is_legal(word):
    return word.isalpha() and word.islower() and len(word) >= min_length and len(word) <= max_length

# Picks out legal words in the word list and sorts them by length, ignoring duplicates
def get_words_by_size(word_list):
    words_by_size = defaultdict(set)
    for word in word_list:
        word = word.rstrip('\n')
        if is_legal(word):
            words_by_size[len(word)].add(word)
    return words_by_size

# Picks a random word of a specified length
def pick_random_word(words_by_size, length):
    return random.choice(list(words_by_size[length]))

# Main class for game logic
class GameProcessor:
    new_game = ''
    remaining_guesses = guesses_per_level

    def __init__(self, length):
        self.length = length
        self.display = '%s ' * length
        self.level = length - min_length + 1
        self.revealed_letters = list(('_') * length)
        self.correct_letters = []
        self.incorrect_letters = []

    # Displays level
    def display_level(self):
        print(f'LEVEL {self.level}')

    # Displays letters the player has revealed so far
    def display_game_board(self):
        print(self.display % tuple(self.revealed_letters))

    def display_remaining_guesses(self):
        print(f'{self.remaining_guesses} guesses remaining')

    def display_game_state(self):
        self.display_game_board()
        self.display_remaining_guesses()

    # Tracks correctly guessed letters
    def update_revealed_letters(self, word, guess):
        word_letters = list(word)
        guessed_letters = list(guess)
        for i, letter in enumerate(guessed_letters):
            # If player guesses a correct letter in the correct position, reveals that letter in lower case
            if letter == word_letters[i]:
                self.revealed_letters[i] = letter
            # If player guesses a correct letter in the incorrect position, displays as upper case
            elif letter in word_letters:
                self.revealed_letters[i] = letter.capitalize()
    
    # Returns True if guess is illegal
    def is_illegal(self, guess):
        if len(guess) != self.length or not guess.isalpha():
            return True
        else:
            return False
    
    # Prompts player if guess is illegal
    def warn_player(self, guess):
        if len(guess) != self.length:
            print(f'Guess a word of length {self.length}.')
        elif not guess.isalpha():
            print('Guess must contain only letters.')

    # Player uses up a guess if their guess was a legal word
    def update_remaining_guesses(self, guess):
        if not self.is_illegal(guess):
            self.remaining_guesses -= 1

    # Checks if player wishes to continue after completing all levels
    def check_to_continue(self):
        while True:
            print('Congratulations! You have completed all levels. Play again? (y/n)')
            self.new_game = input()
            if self.new_game == 'y':
                break
            elif self.new_game == 'n':
                sys.exit()
            else:
                continue

    # Reveals word and checks if player wishes to try again after a game over
    def check_to_try_again(self, word):
        while True:
            print(f"GAME OVER. The correct word was '{word}'. Try again? (y/n)")
            self.new_game = input()
            if self.new_game == 'y':
                break
            elif self.new_game == 'n':
                sys.exit()
            else:
                continue

# Get word list from file and sort by length
word_list_file = open('word_list.txt')
word_list = word_list_file.readlines()
word_list_file.close()
words_by_size = get_words_by_size(word_list)

# Main game loop
while True:
    introduce_game()

    # Ten levels with word lengths starting at 4 and increasing by 1 each level
    for length in range(min_length, max_length + 1):
        game = GameProcessor(length)
        word = pick_random_word(words_by_size, length)
        correct_guess = False
        game.display_level()

        while game.remaining_guesses > 0:
            game.display_game_state()
            guess = input().lower()
            if guess == 'quit game':
                sys.exit()
            elif guess == word:
                correct_guess = True
                break
            elif game.is_illegal(guess):
                game.warn_player(guess)
            else:
                game.update_revealed_letters(word, guess)
            game.update_remaining_guesses(guess)

        # If player completes final level, asks if player wants to continue
        if correct_guess == True and length == max_length:
            game.check_to_continue()
        elif correct_guess == True:
            print('Congratulations! You guessed correctly. Proceed to the next level.')
        else:
            break
    
    # If player completed all levels and chose to play again, restarts main game loop
    if game.new_game == 'y':
        continue

    # If player used up all guesses, reveals word and asks if player wants to try again
    game.check_to_try_again(word)