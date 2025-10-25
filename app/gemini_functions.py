import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

CLIENT = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-2.0-flash"
GENERAL_SYSTEM_INSTRUCTION = """
    You are an intelligent, friendly, and concise AI study assistant designed to help online students learn from long, text-based course modules. Your job is to make learning easier, more interactive, and more engaging. When given a module or reading passage, be prepared to do any of the following based on the request:

    1. Summarize key points clearly using bullet points or short paragraphs.
    2. Generate short multiple choice quizzes to help reinforce learning.
    3. Provide simplified explanations for complex topics in the style of “Explain like I'm 5”.
    4. Offer real-world examples or analogies to help students relate to the concept.
    5. Always keep responses conversational, educational, and positive in tone.
    6. Avoid repeating the exact text — rephrase, simplify, and clarify.

    Keep answers concise and friendly. Assume the student is learning alone and appreciates encouragement and clarity.
    """
CONTENT_CONFIG = types.GenerateContentConfig(
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(
                text=GENERAL_SYSTEM_INSTRUCTION
            ),
        ]
    )


def generate_summary(userInput):
    response = CLIENT.models.generate_content(
        model=MODEL,
        config=CONTENT_CONFIG,
        contents=[
            "Generate a summary of this module with key points, then generate an 'Explain it like I'm 5' summary as well at the bottom. Return your response as HTML code, with nothing else (no other text other than html). Make sure not to include any color styling in the html. \n"
            + userInput
        ]
    )
    response = response.text
    response = response.strip().removeprefix("```html").removesuffix("```")
    return response


def generate_flashcards(userInput):
    response = CLIENT.models.generate_content(
        model=MODEL,
        config=CONTENT_CONFIG,
        contents=[
            "Your goal is to create flashcards. Flashcards will be represented by a dictionary formated like {key:value} with the keys being questions based on the input, and the values being their answer. Your output should consist of nothing else except this dictionary. Do not include any other text besides the dictionary. It should be formatted as a JSON.\nInput:\n"
            + userInput
        ]
    )
    response = response.text
    response = response.strip().removeprefix("```json").removesuffix("```")
    return response


def generate_quiz(userInput):
    response = CLIENT.models.generate_content(
        model=MODEL,
        config=CONTENT_CONFIG,
        contents=[
            """Generate quiz questions using the information from the input. Return your response as a list of objects in JSON format. Each object will have a question attribute representing the question, and answers attribute that is a list of 4 possible answers, and a correct_answer_index attribute that gives the index of the correct answer. So the returned format should look like something like [{question: 'question goes here', answers:[possible answers], correct_answer_index: 1}...]. Only return this list of objects, no other text.\n input:\n"""
            + userInput
        ],
    )
    response = response.text
    response = response.strip().removeprefix("```json").removesuffix("```")
    print(response)
    return response
