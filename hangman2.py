import random
import time

# ASCII art for hangman stages
HANGMAN_PICS = ['''
    +---+
         |
         |
         |
        ===''', '''
    +---+
    O   |
        |
        |
       ===''', '''
    +---+
    O   |
    |   |
        |
       ===''', '''
    +---+
    O   |
   /|   |
        |
       ===''', '''
    +---+
    O   |
   /|\  |
        |
       ===''', '''
    +---+
    O   |
   /|\  |
   /    |
       ===''', '''
    +---+
    O   |
   /|\  |
   / \  |
       ===''']

# Categories for the game
CATEGORIES = {
    "Food": ['pizza', 'burger', 'pasta', 'sushi', 'steak', 'pancake', 'sandwich', 'lasagna', 'taco', 'noodle'],
    "Countries": ['india', 'france', 'brazil', 'china', 'canada', 'italy', 'germany', 'japan', 'australia', 'spain'],
    "Cars": ['ford', 'honda', 'toyota', 'bmw', 'audi', 'volkswagen', 'mercedes', 'subaru', 'jeep', 'porsche'],
    "Animals": ['elephant', 'tiger', 'giraffe', 'rhinoceros', 'hippopotamus', 'zebra', 'kangaroo', 'crocodile', 'penguin', 'gorilla'],
    "Colors": ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink', 'black', 'white', 'brown']
}

# Function to choose a random word from a given category
def getRandomWord(category):
    wordList = CATEGORIES[category]
    return random.choice(wordList)

# Function to display the hangman board and guessed letters
def displayBoard(missedLetters, correctLetters, secretWord, chancesLeft):
    print()
    print(HANGMAN_PICS[len(missedLetters)])
    print()
    print(f'Chances left: {chancesLeft}')
    print('Missed letters:', end=' ')
    for letter in missedLetters:
        print(letter, end=' ')
    print()

    blanks = '_' * len(secretWord)
    for i in range(len(secretWord)):
        if secretWord[i] in correctLetters:
            blanks = blanks[:i] + secretWord[i] + blanks[i+1:]
    for letter in blanks:
        print(letter, end=' ')
    print()

# Function to get a valid guess from the player
def getGuess(alreadyGuessed):
    while True:
        print('Please guess a letter:')
        guess = input().lower()
        if len(guess) != 1:
            print('Only a single letter is allowed.')
        elif guess in alreadyGuessed:
            print('You have already guessed that letter. Choose again.')
        elif guess not in 'abcdefghijklmnopqrstuvwxyz':
            print('Please enter a letter from the alphabet.')
        else:
            return guess

# Function to play again
def playAgain():
    print('Would you like to play again? (yes/no)')
    return input().lower().startswith('y')

# Function to play hangman game
def playHangman():
    print('|H_A_N_G_M_A_N|')

    # Player details
    num_players = int(input('Enter the number of players: '))
    players = []
    for i in range(num_players):
        name = input(f'Enter name for Player {i+1}: ')
        players.append({'name': name, 'score': 0})

    # Game settings
    category_options = list(CATEGORIES.keys())
    category_input = input(f'Choose a category ({"/".join(category_options)}): ')
    category = category_options[int(category_input) - 1] if category_input.isdigit() else next((option for option in category_options if option.startswith(category_input.capitalize())), None)
    
    level_options = {'Easy': 9, 'Medium': 7, 'Hard': 5}
    level_input = input(f'Choose difficulty level ({"/".join(level_options.keys())}): ')
    level = level_options[level_input.capitalize()] if level_input.capitalize() in level_options else level_options.get(level_input.capitalize()[0], None)

    if level is None:
        print('Invalid difficulty level!')
        return

    secretWord = getRandomWord(category)
    chancesLeft = level

    # Game loop
    while True:
        missedLetters = ''
        correctLetters = ''
        gameIsDone = False
        startTime = time.time()

        while time.time() - startTime < 60:
            displayBoard(missedLetters, correctLetters, secretWord, chancesLeft)
            guess = getGuess(missedLetters + correctLetters)

            if guess in secretWord:
                correctLetters += guess
                foundAllLetters = all(letter in correctLetters for letter in secretWord)
                if foundAllLetters:
                    print('You guessed it!')
                    print('The secret word is "' + secretWord + '"! You win!')
                    for player in players:
                        player['score'] += 1
                    gameIsDone = True
                    break
            else:
                missedLetters += guess
                chancesLeft -= 1

            if len(missedLetters) == len(HANGMAN_PICS) - 1 or chancesLeft == 0:
                displayBoard(missedLetters, correctLetters, secretWord, chancesLeft)
                print('You have run out of guesses!')
                print('The word was "' + secretWord + '"')
                gameIsDone = True
                break

        # Update scoreboard
        print('\nScoreboard:')
        for player in players:
            print(f'{player["name"]}: {player["score"]}')
        
        # Check if players want to play again
        if not playAgain():
            break

playHangman()