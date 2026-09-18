
from quiz_generator import generate_quiz
import json


# Quiz settings
number_of_questions = 5
difficulty = "easy"


# Generate quiz
quiz = generate_quiz(
    "sample.docx",
    number_of_questions=number_of_questions,
    difficulty=difficulty
)


# Display quiz
print("===== GENERATED QUIZ =====")
print(json.dumps(quiz, indent=4))
