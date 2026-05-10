from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client()


def generateBotResponse(query: str) -> str | None:
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=str(query),
    )
    return response.text
