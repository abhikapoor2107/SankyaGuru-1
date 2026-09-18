import sys
import os
import tempfile

from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException

from auth import get_current_user
from models import UserDB


# Connect Backend to AI Quiz Generator
AI_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../AI/Quiz_Generator")
)

if AI_PATH not in sys.path:
    sys.path.append(AI_PATH)

from quiz_generator import generate_quiz


router = APIRouter(
    prefix="/api/v1/quiz",
    tags=["Quiz Generator"]
)


@router.post("/generate")
async def generate_quiz_endpoint(
    file: UploadFile = File(...),
    number_of_questions: int = Form(10),
    difficulty: str = Form("medium"),
    current_user: UserDB = Depends(get_current_user)
):
    # Check file type
    allowed_extensions = [".pdf", ".docx", ".pptx"]

    file_extension = os.path.splitext(file.filename)[1].lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, DOCX and PPTX files are supported."
        )

    # Check number of questions
    if number_of_questions < 1 or number_of_questions > 50:
        raise HTTPException(
            status_code=400,
            detail="Number of questions must be between 1 and 50."
        )

    # Check difficulty
    allowed_difficulties = ["easy", "medium", "hard"]

    if difficulty.lower() not in allowed_difficulties:
        raise HTTPException(
            status_code=400,
            detail="Difficulty must be easy, medium or hard."
        )

    temp_file_path = None

    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=file_extension
        ) as temp_file:

            temp_file_path = temp_file.name

            # Save uploaded file
            content = await file.read()
            temp_file.write(content)

        # Generate quiz using AI module
        quiz = generate_quiz(
            temp_file_path,
            number_of_questions=number_of_questions,
            difficulty=difficulty.lower()
        )

        return {
            "success": True,
            "message": "Quiz generated successfully.",
            "filename": file.filename,
            "questions": quiz["questions"]
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except RuntimeError as e:
        error_message = str(e)

        if "503" in error_message or "UNAVAILABLE" in error_message:
            raise HTTPException(
                status_code=503,
                detail="The AI service is temporarily unavailable. Please try again."
            )

        raise HTTPException(
            status_code=500,
            detail=error_message
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Quiz generation failed: {str(e)}"
        )

    finally:
        # Delete temporary file
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)