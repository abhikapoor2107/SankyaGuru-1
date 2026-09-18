def validate_quiz(quiz_data, expected_questions):
    """
    Validate the structure and content of a generated quiz.
    """

    # Check root structure
    if not isinstance(quiz_data, dict):
        return False, "Quiz must be a JSON object."

    # Check questions
    questions = quiz_data.get("questions")

    if not isinstance(questions, list):
        return False, "'questions' must be a list."

    # Check number of questions
    if len(questions) != expected_questions:
        return False, (
            f"Expected {expected_questions} questions, "
            f"but received {len(questions)}."
        )

    # Validate every question
    for index, question in enumerate(questions, start=1):

        if not isinstance(question, dict):
            return False, f"Question {index} is not a valid object."

        # Required fields
        required_fields = [
            "question",
            "options",
            "correct_answer",
            "explanation"
        ]

        for field in required_fields:
            if field not in question:
                return False, (
                    f"Question {index} is missing '{field}'."
                )

        # Check question text
        if not isinstance(question["question"], str):
            return False, f"Question {index} has invalid question text."

        # Check options
        options = question["options"]

        if not isinstance(options, dict):
            return False, f"Question {index} options must be an object."

        required_options = ["A", "B", "C", "D"]

        if set(options.keys()) != set(required_options):
            return False, (
                f"Question {index} must contain exactly "
                f"A, B, C and D options."
            )

        # Check correct answer
        correct_answer = question["correct_answer"]

        if correct_answer not in required_options:
            return False, (
                f"Question {index} has an invalid correct answer."
            )

        # Check explanation
        if not isinstance(question["explanation"], str):
            return False, (
                f"Question {index} has an invalid explanation."
            )

    return True, "Quiz is valid."