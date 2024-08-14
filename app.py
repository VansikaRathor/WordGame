from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# List of words suitable for the age group
WORDS = ['apple', 'banana', 'orange', 'grape', 'peach']

def select_word():
    return random.choice(WORDS)

def check_guess(word, guesses):
    return "".join([letter if letter in guesses else "_" for letter in word])

def check_win(word, guesses):
    return all(letter in guesses for letter in word)

@app.route('/')
def index():
    if 'word' not in session:
        session['word'] = select_word()
        session['guesses'] = []
        session['tries'] = 5  # Set limited tries
        session['message'] = ""
    return render_template('index.html', word=check_guess(session['word'], session['guesses']),
                           tries=session['tries'], message=session['message'])

@app.route('/guess', methods=['POST'])
def guess():
    guess = request.form['guess'].lower()
    if guess in session['guesses']:
        session['message'] = "You already guessed that letter."
    elif guess in session['word']:
        session['guesses'].append(guess)
        if check_win(session['word'], session['guesses']):
            session['message'] = "You won! The word was: " + session['word']
            session['word'] = None
    else:
        session['tries'] -= 1
        if session['tries'] == 0:
            session['message'] = "You lost! The word was: " + session['word']
            session['word'] = None
        else:
            session['guesses'].append(guess)
            session['message'] = "Incorrect guess."
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
