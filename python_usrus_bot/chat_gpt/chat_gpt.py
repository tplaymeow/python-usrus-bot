from os import getenv
from openai import ChatCompletion
import openai

openai.api_key = getenv("OPENAI_API_KEY")


async def chat_gpt_request(content: str) -> str:
    response = await ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": content}])
    return response.choices[0].message.content
