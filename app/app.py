from flask import Flask, render_template, json, request, session
from gemini_functions import generate_summary, generate_flashcards, generate_quiz
import os

app = Flask(__name__)

app.secret_key = os.environ.get("FLASK_SECRET_KEY")


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        gemini_response = session.get("gemini_response")
        if gemini_response:
            return render_template("index.html", gemini_response=gemini_response)
        return render_template("index.html")

    if request.method == "POST":
        if request.form.get("userInput"):
            session.clear()
            session.modified = True
            userInputData = request.form["userInput"]
            gemini_response = generate_summary(userInputData)
            session["gemini_response"] = gemini_response
            session["userInputData"] = userInputData
        return render_template("index.html", gemini_response=gemini_response)


@app.route("/flashcards", methods=["GET", "POST"])
def flashcards():
    if request.method == "GET":
        userInputData = session.get("userInputData")
        gemini_flashcards_response = generate_flashcards(userInputData)
        flashcardDict = json.loads(gemini_flashcards_response)
        return render_template("flashcards.html", gemini_flashcards_response=flashcardDict)


@app.route("/quizzes", methods=["GET", "POST"])
def quizzes():
    if request.method == "GET":
        userInputData = session.get("userInputData")
        quizResponse = generate_quiz(userInputData)
        responseList = json.loads(quizResponse)  # converts from string to list
        session["responseList"] = responseList
        return render_template("quizzes.html", gemini_quizzes_response=responseList)

    if request.method == "POST":
        responseList = session.get("responseList")
        userAnswers = request.form.to_dict()
        results = []
        score = 0

        for i, entry in enumerate(responseList):
            question_index = i
            user_answer_index = int(userAnswers.get(str(question_index)))
            correct_answer_index = entry["correct_answer_index"]
            if user_answer_index == correct_answer_index:
                score += 1
                is_correct = "Correct"
            else:
                is_correct = "Incorrect"

            results.append(
                {
                    "question": entry['question'],
                    "user_answer": entry['answers'][user_answer_index],
                    "correct_answer": entry['answers'][correct_answer_index],
                    "is_correct": is_correct,
                }
            )
        return render_template("results.html", results=results)


@app.route("/about", methods=["GET", "POST"])
def about():
    if request.method == "GET":
        return render_template("about.html")


if __name__ == "__main__":
    # Start app on port 8000, will be different once hosted
    app.run(port=8000, debug=True)
