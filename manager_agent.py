import requests
import os
import base64
import json

api_key = os.getenv("OPENAI_API_KEY")


def encode_image(path):
    image = open(path, "rb")
    return base64.b64encode(image.read()).decode('utf8')

def get_manager_response(question,image_path="drawing.png"):
    encoded_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    message = {
        "role": "user",
        "content": [
            {"type": "text", 
             "text": """
             You are a manager that commands an AI agent to draw on a blank display of width 800 and height 600. 

            The user will tell you something they want to be drawn on the display. You will give the agent simple, geometric, specific instructions to draw it. 
            The agent has the ability to draw lines, circles, and rectangles within the display at specific coordinates.

            Once the agent has drawn the image, you will decide if the image is good enough to show the user or if it needs to be redrawn from scratch.

            Respond to with the following format:

            {
            "response": "Your evaluation/feedback of the image",
            "redraw": "True/False"
            }

            The "response" should be your evaluation/feedback of the image in natural language. This feedback will be given to the agent to help it redraw the image and make it better.
            Ensure this feedback is specific and detailed.

            The "redraw" should be True if the image is not good enough and you need to redraw it from scratch, or if the screen is blank.

            The "redraw" should be False if the image is good enough and you can show it to the user.

            Here is what the image wants drawn: """+question+"""

            The image of the drawing is below:
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
    response_data = response.json()
    
    try:
        if 'choices' in response_data and len(response_data['choices']) > 0:
            structured_response = response_data['choices'][0]['message']['content']
            cleaned_response = structured_response.strip('```json\n').strip('```').strip()
            
            try:
                response_dict = json.loads(cleaned_response)
                return {
                    'response': response_dict.get('response', ''),
                    'redraw': response_dict.get('redraw', True)
                }
            except json.JSONDecodeError:
                try:
                    import ast
                    response_dict = ast.literal_eval(cleaned_response)
                    return {
                        'response': response_dict.get('response', ''),
                        'redraw': response_dict.get('redraw', True)
                    }
                except:
                    return {
                        'response': 'Error parsing manager response',
                        'redraw': True
                    }
        else:
            return {
                'response': 'No valid response from manager',
                'redraw': True
            }
    except Exception as e:
        return {
            'response': f'Error processing manager response: {str(e)}',
            'redraw': True
        }