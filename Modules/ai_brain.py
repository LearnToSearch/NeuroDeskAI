import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Get API key from .env
API_KEY = os.getenv("API_KEY")

# Initialize client
client = OpenAI(api_key=API_KEY)

def ask_ai(question):

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": question}
        ]
    )

    answer = response.choices[0].message.content

    return answer[:500]