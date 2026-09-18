import re


def clean_text(text):
    # Replace multiple spaces with a single space
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    # Remove spaces at the beginning and end
    text = text.strip()

    return text