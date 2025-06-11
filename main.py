import requests
import os
from pydantic import BaseModel
import json
from tools import *
import pygame
import pygame.image
from manager_agent import get_manager_response, encode_image

pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
api_key = os.getenv("OPENAI_API_KEY")
screen.fill((255,255,255))

def save_screen_as_image(filename="drawing.png"):

    try:
        pygame.image.save(screen, filename)
        print(f"Screen saved as {filename}")
        return f"Successfully saved screen as {filename}"
    except Exception as e:
        print(f"Error saving screen: {e}")
        return f"Error saving screen: {e}"


def clean_json_response(response_text):
    """
    Clean the response text by removing any comments and ensuring it's valid JSON.
    """
    # Remove any lines that start with // or contain //
    lines = response_text.split('\n')
    cleaned_lines = []
    for line in lines:
        if '//' in line:
            line = line.split('//')[0]
        if line.strip():
            cleaned_lines.append(line)
    
    cleaned_response = '\n'.join(cleaned_lines)
    return cleaned_response.strip()


def get_agent_response(question, context, feedback = ""):

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

            CRITICAL: You must respond with ONLY valid JSON. No comments, no explanations, no additional text. Your response must be parseable JSON.

            Only use the tools if you don't have the information you need. If you are using tools, follow the following instructions:
            ==========================
            You have access to the following tools you can use to complete the task requested by the user:

            Tool 1: draw_line
            
            Draws one or more lines on the screen. Each line is defined by the coordinates of the start and end points.

            Input: None

            Return format: List[Dict[start_point, end_point]]
            - Each item: start_point (Array[int, int]), end_point (Array[int, int])
            Example:
            "draw_line": [
              {"start_point": [0, 0], "end_point": [0, 100]},
              {"start_point": [0, 100], "end_point": [100, 100]}
            ]

            Tool 2: draw_circle

            Draws one or more circles on the screen. Each circle is defined by its center and radius.

            Input: None
            Return format: List[Dict[center, radius]]
            - Each item: center (Array[int, int]), radius (int)
            Example:
            "draw_circle": [
              {"center": [200, 200], "radius": 50}
            ]


            Tool 3: draw_rectangle

            Draws one or more rectangles on the screen. Each rectangle is defined by its top-left corner, width, and height.

            Input: None

            Return format: List[Dict[top_left, width, height]]
            - Each item: top_left (Array[int, int]), width (int), height (int)
            Example:
            "draw_rectangle": [
              {"top_left": [300, 300], "width": 100, "height": 50}
            ]

            
            RESPONSE FORMAT RULES:
            1. You must respond in a consistent structured format (e.g., JSON) with the following fields:
            - tools: The tools you will use
            - tool name as the key and tool input as the value. tool input is the input you will give to the tool. The key should be the name of the Input field(s) of the tool. (e.g. 'location' for get_current_weather)

            2. ABSOLUTELY NO COMMENTS: Do not include any comments with // or # or any other comment syntax
            3. NO EXPLANATIONS: Do not include any explanatory text outside the JSON
            4. PURE JSON ONLY: Your entire response must be valid JSON that can be parsed directly
            
            Here is a sample question/response. You must respond in the same format:

            Example question: Draw a line from (100,100) to (200,200), draw a circle at (300,300) with a radius of 50, and draw a rectangle at (400,400) with a width and height of 100.

            Example response: {"tools": {"draw_line": {"start_point": (100, 100), "end_point": (200, 200)}, "draw_circle": {"center": (300, 300), "radius": 50}, "draw_rectangle": {"top_left": (400, 400), "width": 100, "height": 100}}}

            The overarching key MUST be "tools".

            

            Example using multiple tools: Draw a line from (0,0) to (0,100) and a line from (0,100) to (100,100). Also, draw a circle at (200,200) with a radius of 50. Finally, draw a rectangle at (300,300) with a width of 100 and height of 50.


            Example response for multiple tools:
            {
            "tools": {
                "draw_line": [
                {"start_point": [0, 0], "end_point": [0, 100]},
                {"start_point": [0, 100], "end_point": [100, 100]}
                ],
                "draw_circle": [
                {"center": [200, 200], "radius": 50}
                ],
                "draw_rectangle": [
                {"top_left": [300, 300], "width": 100, "height": 50}
                ]
            }
            }

            FINAL REMINDER: Output ONLY valid JSON. No comments, no explanations, no additional text. The response must be parseable by json.loads().
            
            ========================

            

            You may have already used tools to get the information you need. 
            Here is what you know based on your previous conversation with the user: """+ context+"""

            You will also receive important feedback from your manager. It is essential that you listen to and implement this feedback. 
            Do not use the feedback to simply add on to your drawing. It is okay to redraw the image from scratch and remove components of the image that are not needed.
            Here is the feedback from your manager: """+ feedback+"""

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
        cleaned_response = clean_json_response(cleaned_response)
        print("Cleaned response:", cleaned_response)
        try:
            response_dict = json.loads(cleaned_response)
            return response_dict
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            try:
                import ast
                response_dict = ast.literal_eval(cleaned_response)
                return response_dict
            except Exception as ast_error:
                print(f"AST literal_eval error: {ast_error}")
                return {"error": "Failed to decode response as JSON", "content": cleaned_response}
    else:
        return {"error": "No valid response from model"}
    
context = ""
tool_outputs = []
pygame.display.update()

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    #pygame.display.update()
    question = input("Enter a question: ")
    if question.lower().strip() == "clear":
        screen.fill((255, 255, 255))
        pygame.display.update()
        continue
    
    #save_screen_as_image()
    while True:
        pygame.display.update()
        save_screen_as_image()
        # Manager agent response
        response = get_manager_response(question, "drawing.png")
        print(response)
        response_text = response['response']
        print(response_text)
        manager_decision = response['redraw']

        if manager_decision == "False":
            print("Drawing completed")
            save_screen_as_image()
            break

        screen.fill((255, 255, 255))

            
        context = f"""

        You are trying to answer this question: {question}

        You got the following outputs from the tools used previously: {tool_outputs}

        Do not include any comments (with the '//') or written text in the JSON response at all.
        Note: You may never use the word "//" in your response under any circumstances.

        """
        response = get_agent_response(question, context, feedback = response_text)
        print(response)
        tool_outputs = []
        tools_used = []
        tools = response.get('tools', {})
        for line in tools.get('draw_line', []):
            value = draw_line(screen, line['start_point'], line['end_point'])
            tool_outputs.append(value)
            tools_used.append('draw_line')
        for circle in tools.get('draw_circle', []):
            value = draw_circle(screen, circle['center'], circle['radius'])
            tool_outputs.append(value)
            tools_used.append('draw_circle')
        for rect in tools.get('draw_rectangle', []):
            value = draw_rectangle(screen, rect['top_left'], rect['width'], rect['height'])
            tool_outputs.append(value)
            tools_used.append('draw_rectangle')
        print("tool outputs: ", tool_outputs)
