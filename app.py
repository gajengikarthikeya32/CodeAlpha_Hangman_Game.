from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = "change-this-to-a-random-secret-key"

WORDS = ["python", "computer", "program", "developer", "coding"]
MAX_ATTEMPTS = 6


def new_game():
    session["word"] = random.choice(WORDS)
    session["guessed"] = []
    session["wrong"] = 0
    session["status"] = "playing"


@app.route("/", methods=["GET", "POST"])
def index():
    if "word" not in session:
        new_game()

    message = ""

    if request.method == "POST":
        action = request.form.get("action", "")

        if action == "new":
            new_game()
            return redirect(url_for("index"))

        if session.get("status") == "playing":
            guess = request.form.get("guess", "").strip().lower()

            if len(guess) != 1 or not guess.isalpha():
                message = "Please enter one alphabet letter."
            elif guess in session["guessed"]:
                message = "You already guessed that letter."
            else:
                guessed = session["guessed"]
                guessed.append(guess)
                session["guessed"] = guessed

                if guess not in session["word"]:
                    session["wrong"] += 1
                    message = "Not quite! Try another letter."
                else:
                    message = "Good guess!"

                if all(letter in session["guessed"] for letter in session["word"]):
                    session["status"] = "won"
                elif session["wrong"] >= MAX_ATTEMPTS:
                    session["status"] = "lost"

    word = session["word"]
    guessed = session["guessed"]
    display_word = " ".join(letter if letter in guessed else "_" for letter in word)
    remaining = MAX_ATTEMPTS - session["wrong"]
    alphabet = "abcdefghijklmnopqrstuvwxyz"

    return render_template(
        "index.html",
        display_word=display_word,
        guessed=guessed,
        remaining=remaining,
        alphabet=alphabet,
        status=session["status"],
        answer=word if session["status"] in ("won", "lost") else "",
        message=message,
    )


if __name__ == "__main__":
    app.run(debug=True)
