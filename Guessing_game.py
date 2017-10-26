# Ben Stutzman
# Project 2 - Guessing Game
# 10/11/17
# A simple number guessing game that keeps track of high scores

import time
from random import randint

def change_boolean_setting(prompt, old_setting):
    """
    Change a boolean setting (print_num or clear_highscores)
    based on input.
    """
    entry = input(prompt).lower()
    if entry.startswith('y'):
        return 'yes'
    elif entry.startswith('n'):
        return 'no'
    elif entry.startswith('o'):
        return 'once'
    else:
        return old_setting

def change_int_setting(prompt, old_setting):
    """
    Change an integer setting (max_guesses or num_highscores)
    based on input.
    """
    entry = input(prompt)
    try:
        return int(entry)
    except:
        return old_setting

def check_num(prompt):
    """Ask the user the given prompt until he/she enters an integer"""
    guess = input(prompt)
    guess_is_int = False
    while guess_is_int == False:
        try:
            return int(guess)
            guess_is_int == True
        except:
            guess = input("That's not a valid number. Guess again!\n")

def guess_num(number, print_num, max_guesses):
    """
    Prompt the user to guess the number, and say if the guess is high or low.
    Repeat until the user guesses the number or runs out of guesses.
    """
    if print_num == 'yes' or print_num == 'once':
        print(number)
    num_guesses = 0
    guess = check_num("I'm thinking of a number from 1 to 100. "
                      "Can you guess it?\n")
    num_guesses += 1
    while guess != number and num_guesses < max_guesses:
        if num_guesses + 1 == max_guesses:
            last_guess = 'This is your last chance!'
        else:
            last_guess = 'Guess again!'
        if guess < number:
            guess = check_num('Too low. %s\n' % last_guess)
        else:
            guess = check_num('Too high. %s\n' % last_guess)
        num_guesses += 1
        
    if num_guesses == 1:
        plural = ''
    else:
        plural = 'es'
        
    if guess == number:
        print('\nYou got it! It took you %i guess%s.' % (num_guesses, plural))
        return True, num_guesses
    else:
        print("\nSorry, you've used up all your guesses. My number was %d."
              % number)
        return False, num_guesses

def make_score_list(score_file, num_highscores):
    """
    Create a score list from the score file;
    if no file exists, create a blank one.
    """
    try:
        with open(score_file, 'r+') as f:
            old_score_list = f.readlines()
        print('\nRetrieving high scores from database...')
        for i in range(39):
            print('|', end='')
            time.sleep(0.02)
        print('|')
        score_list = []
        i = 0
        while i < num_highscores * 2 and i < len(old_score_list):
            score_list.append(old_score_list[i])
            i += 1
        for i in range(0, len(score_list), 2):
            score_list[i] = score_list[i].strip()
            score_list[i + 1] = int(score_list[i + 1].strip())
    except:
        with open(score_file, 'w+') as f:
            score_list = []
    return score_list
    

def add_highscore(score_list, score_file, num_guesses, num_highscores):
    """Check if a score is a high score, and add it to the list if it is."""
    new_high = False
    i = 1
    while i < num_highscores * 2 and not new_high:
        try:
            if num_guesses < score_list[i]:
                new_high = True
                print('You have a high score!')
                if len(score_list) < num_highscores * 2:
                    score_list.append(score_list[-2])
                    score_list.append(score_list[-2])
                for j in range(len(score_list) - 3, i - 2, -1):
                    score_list[j+2] = score_list[j]
                name = input('\nEnter your name: ')
                while not name:
                    name = input("Surely they must call you something!\n"
                                 "Enter your name: ")
                score_list[i - 1] = name
                score_list[i] = num_guesses                        
        except:
            new_high = True
            print('You have a high score!')
            name = input('\nEnter your name: ')
            while not name:
                name = input("Surely they must call you something!\n"
                             "Enter your name: ")
            score_list.append(name)
            score_list.append(num_guesses)
        i += 2
    if new_high == False:
        print("Sorry, that's not a high score.")
    return score_list
    
print_num = 'no'
clear_highscores = 'no'
num_highscores = 3
max_guesses = 7
score_file = 'highscores.txt'
password = 'settings'

choice = input('Welcome to NUMBER GUESSER!\nTo begin playing, '
               'just press enter.\n')

# Repeats the game until the user decides to quit

while not choice.lower().startswith('q'):

    # Allows administrator to change settings before playing

    if choice == password:
        print('\nSettings (Leaving a field blank will make no change):')
        print_num = change_boolean_setting('Print number (y/n or once '
                                           'for one time)? ', print_num)
        max_guesses = change_int_setting('Max number of guesses? ', max_guesses)
        num_highscores = change_int_setting('Max number of high scores '
                                            'on leaderboard? ', num_highscores)
        clear_highscores = change_boolean_setting('Clear leaderboard (y/n '
                                                  'or once for once time)? ',
                                                  clear_highscores)
        print('Changes saved.\n')
        choice = input("Press enter to keep playing, or 'q' to quit:\n")
        continue

    # Clears the high score list and file, if desired
        
    if clear_highscores == 'yes' or clear_highscores == 'once':
        with open('highscores.txt', 'w+') as f:
            f.truncate()
            
    number = randint(1,100)

    (got_it, num_guesses) = guess_num(number, print_num, max_guesses)

    score_list = make_score_list(score_file, num_highscores)
        
    if got_it:
        score_list = add_highscore(score_list, score_file, num_guesses,
                                   num_highscores)

    # Updates the score file

    with open(score_file, 'w+') as f:
        for entry in score_list:
            f.write(str(entry) + '\n')

    # Prints the updated leaderboard

    if score_list:
        print('\nLeaderboard:')
        for i in range(0, len(score_list), 2):
            if score_list[i + 1] == 1:
                plural = ''
            else:
                plural = 'es'  
            print('%i. %s: %i guess%s' % ((i + 2) // 2, score_list[i],
                                          score_list[i + 1], plural))
    else:
        print("\nThere aren't any high scores yet.")

    # Resets temporary settings

    if print_num == 'once':
        print_num = 'no'
    if clear_highscores == 'once':
        clear_highscores = 'no'
    
    choice = input("\nPress enter to play again, or 'q' to quit:\n")

print('\nThanks for playing!')

time.sleep(3)
