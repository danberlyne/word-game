#!/usr/bin/env python3
# word_game.py - A word-guessing game

import sys, random, time
from collections import defaultdict

# Word lengths for the first and last levels
min_length = 4
max_length = 13
# Number of guesses per level
guesses_per_level = 6
# Text that goes before correct/incorrect letters on the game board
correct_letter_info = 'IN WORD: '
incorrect_letter_info = 'NOT IN WORD: '

# Introduction sequence
def introduce_game():
    print('=' * 50)
    print('''Welcome to The Word Game.

Guess the word correctly to proceed to the next level.
A correct letter in the correct position will be displayed in lower case.
A correct letter in the incorrect position will be displayed in upper case to the right of the game board.

If you wish to quit at any point, type 'quit game'.''')
    print('=' * 50 + '\n')

# Sorts a set of letters alphabetically and turns it into a string
def make_displayable(set_of_letters):
    list_of_letters = list(set_of_letters)
    list_of_letters.sort()
    return ''.join(list_of_letters)

# Creates a display for a set of letters
def make_letter_display(letter_info, letters):
    return letter_info + make_displayable(letters)

# Main class for game logic
class GameProcessor:
    new_game = ''
    remaining_guesses = guesses_per_level

    def __init__(self, word_length):
        self.word_length = word_length
        self.level = word_length - min_length + 1
        self.revealed_letters = list(('_') * word_length)
        self.correct_letters = set()
        self.incorrect_letters = set()
        # Display elements
        self.guess_display = '%s ' * word_length + '  '
        self.empty_guess_display = self.guess_display % ((' ',) * word_length)
        self.correct_letter_display = make_letter_display(correct_letter_info, self.correct_letters)
        self.incorrect_letter_display = make_letter_display(incorrect_letter_info, self.incorrect_letters)
        self.game_board_display = self.guess_display + self.correct_letter_display + '\n' + self.empty_guess_display + self.incorrect_letter_display

    # Updates the game board following player's guess
    def update_game_board(self, word, guess):
        word_letters = list(word)
        guessed_letters = list(guess)
        for i, letter in enumerate(guessed_letters):
            # If player guesses a correct letter in the correct position, reveals that letter and displays it on the right
            if letter == word_letters[i]:
                self.update_revealed_letters(i, letter)
                self.update_correct_letters(letter)
            # If player guesses a correct letter in the incorrect position, displays it on the right
            elif letter in word_letters:
                self.update_correct_letters(letter)
            # If player guesses an incorrect letter, displays it on the right
            else:
                self.update_incorrect_letters(letter)
        self.update_game_display()

    def update_revealed_letters(self, position, letter):
        self.revealed_letters[position] = letter
    
    def update_correct_letters(self, letter):
        self.correct_letters.add(letter.capitalize())

    def update_incorrect_letters(self, letter):
        self.incorrect_letters.add(letter.capitalize())
    
    def update_game_display(self):    
        self.correct_letter_display = make_letter_display(correct_letter_info, self.correct_letters)
        self.incorrect_letter_display = make_letter_display(incorrect_letter_info, self.incorrect_letters)
        self.game_board_display = self.guess_display + self.correct_letter_display + '\n' + self.empty_guess_display + self.incorrect_letter_display
    
    # Player uses up a guess if their guess was valid
    def update_remaining_guesses(self, guess):
        if self.is_valid(guess):
            self.remaining_guesses -= 1

    # Returns True if guess is valid word
    def is_valid(self, guess):
        if len(guess) == self.word_length and guess in dictionary_by_size[len(guess)]:
            return True
        else:
            return False
    
    # Prompts player if guess is invalid
    def warn_player(self, guess):
        if len(guess) != self.word_length:
            print(f'Guess a word of length {self.word_length}.\n')
            time.sleep(1)
        elif guess not in dictionary_by_size[len(guess)]:
            print('Word not found in dictionary.\n')
            time.sleep(1)

    def display_level(self):
        print(f'LEVEL {self.level}')

    # Displays letters the player has guessed so far, together with remaining guesses
    def display_game_state(self):
        self.display_game_board()
        self.display_remaining_guesses()

    def display_game_board(self):
        print(self.game_board_display % tuple(self.revealed_letters))

    def display_remaining_guesses(self):
        print(f'{self.remaining_guesses} guesses remaining')

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


# Picks out legal words in the word list and sorts them by length, ignoring duplicates
def get_words_by_size(word_list):
    words_by_size = defaultdict(set)
    for word in word_list:
        word = word.rstrip('\n ')
        if is_legal(word):
            words_by_size[len(word)].add(word)
    for length in range(min_length, max_length + 1):
        if len(words_by_size[length]) == 0:
            # `word_list[-1]` is the file name
            raise Exception(f'No legal words of length {length} in {word_list[-1]}')
    return words_by_size

# Returns `True` if `word` is a legal word
def is_legal(word):
    return word.isalpha() and word.islower() and len(word) >= min_length and len(word) <= max_length

# Picks a random word of a specified length
def pick_random_word(words_by_size, length):
    return random.choice(list(words_by_size[length]))

# Converts a file to a list of strings indexed by line
def convert_to_list(path):
    file = open(path)
    file_as_list = file.readlines()
    file.close()
    # Adds file name to end of list so it can be accessed in exception handling
    file_as_list.append(path)
    return file_as_list

# Get dictionary and word list from files and sort legal words by length
dictionary = convert_to_list('dictionary.txt')
dictionary_by_size = get_words_by_size(dictionary)
word_list = convert_to_list('word_list.txt')
words_by_size = get_words_by_size(word_list)

# Main game loop
while True:
    introduce_game()

    # Ten levels with word lengths starting at 4 and increasing by 1 each level
    for word_length in range(min_length, max_length + 1):
        game = GameProcessor(word_length)
        word = pick_random_word(words_by_size, word_length)
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
            elif not game.is_valid(guess):
                game.warn_player(guess)
            else:
                game.update_game_board(word, guess)
            game.update_remaining_guesses(guess)
            
        # If player completes final level, asks if player wants to continue
        if correct_guess == True and word_length == max_length:
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