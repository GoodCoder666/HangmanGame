import pgzrun
from random import choice

WIDTH = 960
HEIGHT = 720
TITLE = 'Hangman'

center_x = WIDTH / 2
center_y = HEIGHT / 2

def read_words():
    words = []
    filename = 'wordList.txt'
    with open(filename) as file:
        for line in file:
            if line == '\n':
                continue
            word = line.rstrip('\n')
            words.append(word)
    return words

def draw():
    global game_over, lives, won, player_guess, word
    screen.clear()
    screen.blit('background', (0, 0))
    new_button.draw()
    hangman.draw()
    s = ''
    for i in display_word:
        s += i + '       '
    screen.draw.text(str(lives), center=(center_x + 348, center_y + 62), color='orange', fontsize=80, shadow=(0.85, 0.85))
    screen.draw.text(s, topleft=(center_x - 368, center_y + 160), color='red', fontsize=80)
    if game_over:
        screen.draw.text('Sorry! You lose.', center=(center_x, center_y + 286), color='blue', fontsize=80, shadow=(0.25, 0.25))
    elif won:
        screen.draw.text('Goob job! You won.', center=(center_x, center_y + 286), color='blue', fontsize=80, shadow=(0.25, 0.25))
    else:
        s = 'Please press a letter to guess.' if player_guess == '' else ('Your last guess is: ' + player_guess)
        screen.draw.text(s, center=(center_x, center_y + 286), color='blue', fontsize=80, shadow=(0.25, 0.25))

def new_game():
    global word, display_word, words, lives, game_over, won, player_guess
    word = choice(words)
    display_word = '?' * len(word)
    player_guess = ''
    lives = 8
    hangman.image = '0'
    won = game_over = False

def update_display_word(letter):
    global lives, display_word, word, game_over, won
    letter = letter.lower()
    got_letter = False
    for i in range(0, len(word)):
        if word[i] == letter:
            got_letter = True
            l = list(display_word)
            l[i] = word[i]
            display_word = ''.join(l)

    # Player has not got the letter?
    if not got_letter:
        lives -= 1
        hangman.image = str(int(hangman.image) + 1)
        if lives < 1:
            game_over = True
            display_word = word
            return
    if display_word == word:
        won = True

def on_mouse_down(pos, button):
    global new_pressed
    if button != mouse.LEFT:
        return
    if new_button.collidepoint(pos):
        new_button.x += 2
        new_button.y += 2
        new_pressed = True

def on_mouse_up():
    global new_pressed
    if new_pressed:
        new_pressed = False
        new_button.x -= 2
        new_button.y -= 2
        new_game()

def on_key_up(key):
    global game_over
    if game_over:
        return
    for i in range(ord('A'), ord('Z') + 1):
        l = chr(i)
        script = '''
if key == keys.%s:
    global player_guess
    update_display_word(l)
    player_guess = l.lower()''' %(l)
        exec(script)

words = read_words()
new_button = Actor('new', center=(center_x + 316, center_y - 52))
hangman = Actor('0', center=(center_x - 280, center_y - 32))

new_pressed = won = game_over = False
player_guess = ''
word = ''
display_word = ''
lives = 8
new_game()

pgzrun.go()
