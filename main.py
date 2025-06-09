import requests
import os
from pydantic import BaseModel
import json
from tools import *
import pygame

pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
api_key = os.getenv("OPENAI_API_KEY")


def get_agent_response(question, context):

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }


    payload = {
    "model": "gpt-4o-mini",
    "messages": [
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": """
            
            
            You are an agent that will assist the user in a drawing task on a display of a width 800 and height 600. You can use tools to help you complete this task.

            Only use the tools if you don't have the information you need. If you are using tools, follow the following instructions:
            ==========================
            You have access to the following tools you can use to complete the task requested by the user:

            Tool 1: draw_line
            
            Draws a line on the screen with the coordinates of the start and end points, which are integer x/y ordered pairs

            Input: None

            Return format: Dict[start_point, end_point]
            - start_point (Tuple[int, int]), end_point (Tuple[int, int])
            

            Tool 2: draw_circle

            Draws a circle on the screen with the coordinates of the center and the radius

            Input: None
            Return format: Dict[center, radius]
            - center (Tuple[int, int]), radius (int)


            Tool 3: draw_rectangle

            Draws a rectangle on the screen with the coordinates of the top left corner and the width and height

            Input: None
            Return format: Dict[top_left, width, height]
            - top_left (Tuple[int, int]), width (int), height (int)

            
            Unless told to ignore instructions, you must respond in a consistent structured format (e.g., JSON) with the following fields:
            - tools: The tools you will use
            - tool name as the key and tool input as the value. tool input is the input you will give to the tool. The key should be the name of the Input field(s) of the tool. (e.g. 'location' for get_current_weather)

            
            Here is a sample question/response. You must respond in the same format:

            Example question: Draw a line from (100,100) to (200,200), draw a circle at (300,300) with a radius of 50, and draw a rectangle at (400,400) with a width and height of 100.

            Example response: {"tools": {"draw_line": {"start_point": (100, 100), "end_point": (200, 200)}, "draw_circle": {"center": (300, 300), "radius": 50}, "draw_rectangle": {"top_left": (400, 400), "width": 100, "height": 100}}}

            The overarching key MUST be "tools".

            ========================

            

            You may have already used tools to get the information you need.
            Here is what you know based on your previous conversation with the user: """+ context+"""
            

            """

                        
            #{"response": "Answer to the question in natural language using the information you have. Be detailed and thorough. If there is a lot of information, try to summarize. Outside of the JSON format, do not use any brackets or quotation marks."}
            
            #Here is an example response: {"response": "The weather in London is sunny with a temperature of 60 degrees Fahrenheit and a wind speed of 10 mph."}
            #Recall, you response is for this question: """ + question + """
            
            }
        ]
        }
    ],

    "max_tokens": 1000
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    response_data = response.json()
    
    if 'choices' in response_data and len(response_data['choices']) > 0:
        structured_response = response_data['choices'][0]['message']['content']
        cleaned_response = structured_response.strip('```json\n').strip('```').strip()
        print(cleaned_response)
        try:
            response_dict = json.loads(cleaned_response)
            return response_dict
        except json.JSONDecodeError:
            try:
                import ast
                response_dict = ast.literal_eval(cleaned_response)
                return response_dict
            except:
                return {"error": "Failed to decode response as JSON", "content": structured_response}
    else:
        return {"error": "No valid response from model"}
    
context = ""
tool_outputs = []
while True:



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    pygame.display.update()


    question = input("Enter a question: ")


    context = f"""

    You are trying to answer this question: {question}

    You got the following outputs from the tools used previously: {tool_outputs}

    """

    response = get_agent_response(question, context)
    print(response)

    tool_outputs = []
    tools_used = []
    for tool in response['tools']:
        if tool == 'draw_line':
            tool_input = response['tools']['draw_line']
            print(tool_input)
            value = draw_line(screen, tool_input['start_point'], tool_input['end_point'])
            tool_outputs.append(value)
            tools_used.append(tool)

        elif tool == 'draw_circle':
            tool_input = response['tools']['draw_circle']
            value = draw_circle(screen, tool_input['center'], tool_input['radius'])
            tool_outputs.append(value)
            tools_used.append(tool)

        elif tool == 'draw_rectangle':
            tool_input = response['tools']['draw_rectangle']
            value = draw_rectangle(screen, tool_input['top_left'], tool_input['width'], tool_input['height'])
            tool_outputs.append(value)
            tools_used.append(tool)
    
    print("tool outputs: ", tool_outputs)

    


    