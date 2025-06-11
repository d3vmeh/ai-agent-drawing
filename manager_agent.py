import requests
import os
import base64

api_key = os.getenv("OPENAI_API_KEY")


def encode_image(path):
    image = open(path, "rb")
    return base64.b64encode(image.read()).decode('utf8')

def get_llm_response(question,image_path):
    encoded_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    message = {
        "role": "user",
        "content": [
            {"type": "text", 
             "text": f"""
             You are a manager that commands an AI agent to draw on a black display of width 800 and height 600. 

            The user will tell you something they want to be drawn on the display. You will command the agent to draw it. 
            The agent has the ability to draw lines, circles, and rectangles within the display at specific coordinates.

            Once the agent has drawn the image, you will decide if the image is good enough to show the user or if it needs to be redrawn from scratch.

            Respond to the user with the following format:

            {"""
            "response": "Your evaluation of the image",
            "redraw": True/False
            """}

            The "response" should be your evaluation/feedback of the image in natural language.

            The "redraw" should be True if the image is not good enough and you need to redraw it from scratch.

            The "redraw" should be False if the image is good enough and you can show it to the user.

            Here is what the image wants drawn: {question}
             """},
            {"type": "image_url", "image_url": {"url": f"data:image/jpg;base64,{encoded_image}", "detail": "low"}}
        ]
    }

    payload = {
        "model": "gpt-4o-mini",
        "temperature": 0.5,
        "messages": [message],
        "max_tokens": 800
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    return response.json()