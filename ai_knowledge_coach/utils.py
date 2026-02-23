import json
import streamlit as st

def get_prompt_template():
    return (
        """
        Given the topic: {topic}, generate a JSON object with the following fields.\n\n"
        "summary": A concise, structured summary (length: {summary_length}).\n"
        "insights": A list of 5 key insights.\n"
        "interview_questions": A list of 3 interview questions.\n"
        "quiz": A list of 5 objects, each with:\n"
        "    question": The MCQ question (difficulty: {quiz_difficulty}),\n"
        "    options": List of 4 options,\n"
        "    answer": The correct answer.\n\n"
        "Format the response as valid JSON."
        """
    )

def parse_ai_response(response):
    try:
        data = json.loads(response)
        # Validate structure
        assert "summary" in data and "insights" in data and "interview_questions" in data and "quiz" in data
        return data
    except Exception:
        # Try to extract JSON from text
        try:
            start = response.index('{')
            end = response.rindex('}') + 1
            data = json.loads(response[start:end])
            return data
        except Exception as e:
            raise ValueError("Could not parse AI response as JSON. Please try again.") from e

def show_error(e):
    st.error(f"Error: {str(e)}")
