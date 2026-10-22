from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

secret_number = random.randint(1, 100)
attempts = 0


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/guess", methods=["POST"])
def guess_number():
    global secret_number, attempts

    data = request.get_json()
    guess = data.get("guess")

    try:
        guess = int(guess)
    except (ValueError, TypeError):
        return jsonify({
            "message": "Please enter a valid number."
        })

    if guess < 1 or guess > 100:
        return jsonify({
            "message": "Please enter a number between 1 and 100."
        })

    attempts += 1

    if guess < secret_number:
        return jsonify({
            "message": "Too low! Try again.",
            "attempts": attempts,
            "won": False
        })

    elif guess > secret_number:
        return jsonify({
            "message": "Too high! Try again.",
            "attempts": attempts,
            "won": False
        })

    else:
        return jsonify({
            "message": "🎉 Congratulations! You guessed the number!",
            "attempts": attempts,
            "won": True
        })


@app.route("/reset", methods=["POST"])
def reset_game():
    global secret_number, attempts

    secret_number = random.randint(1, 100)
    attempts = 0

    return jsonify({
        "message": "New game started!"
    })


if __name__ == "__main__":
    app.run(debug=True)