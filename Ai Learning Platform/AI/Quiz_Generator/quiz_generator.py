
import os
import json
from pathlib import Path
from dotenv import load_dotenv
from google import genai

from document_reader import extract_text
from text_processor import clean_text
from quiz_validator import validate_quiz


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found.")

client = genai.Client(api_key=api_key)


def generate_quiz(file_path, number_of_questions=10, difficulty="medium"):

    # Read document
    text = extract_text(file_path)

    if not text:
        raise ValueError("Could not extract text from document.")

    # Clean text
    cleaned_text = clean_text(text)

    # Prompt
    prompt = f"""
You are an AI quiz generator.

Generate {number_of_questions} multiple-choice questions
from the study material below.

Difficulty: {difficulty}

Rules:
- Each question must have exactly 4 options.
- Options must be A, B, C and D.
- Only one option can be correct.
- Questions must be based ONLY on the study material.
- Provide a short explanation.
- Avoid duplicate questions.
- Return ONLY valid JSON.

JSON format:

{{
    "questions": [
        {{
            "question": "...",
            "options": {{
                "A": "...",
                "B": "...",
                "C": "...",
                "D": "..."
            }},
            "correct_answer": "A",
            "explanation": "..."
        }}
    ]
}}

Study Material:

{cleaned_text}
"""

    # Generate quiz
    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

    except Exception as e:
        raise RuntimeError(
            f"Failed to generate quiz using Gemini API: {e}"
        )

    # Remove Markdown code fences if Gemini adds them
    cleaned_response = response.text.strip()

    if cleaned_response.startswith("```json"):
        cleaned_response = cleaned_response[7:]

    if cleaned_response.endswith("```"):
        cleaned_response = cleaned_response[:-3]

    # Convert JSON string to Python dictionary
    quiz_data = json.loads(cleaned_response)

    # Validate quiz
    is_valid, message = validate_quiz(
        quiz_data,
        number_of_questions
    )

    if not is_valid:
        raise ValueError(f"Invalid quiz: {message}")

    return quiz_data
