# AI Agent Drawing System

An interactive AI-powered drawing system that uses multiple AI agents to create geometric drawings on a pygame canvas. The system features a drawing agent that creates shapes based on user requests and a manager agent that evaluates the results and provides feedback for improvements.

## 🎨 Features

- **Interactive Drawing**: Create geometric shapes (lines, circles, rectangles) on a white canvas
- **AI-Powered Drawing Agent**: Uses GPT-4o-mini to interpret drawing requests and generate geometric instructions
- **Manager Agent**: Evaluates drawings and provides feedback for improvements
- **Real-time Canvas**: Live pygame display showing the drawing process
- **Image Export**: Save drawings as PNG files
- **Iterative Improvement**: The system can redraw based on manager feedback
- **Comment-Free JSON**: Robust parsing that handles AI responses without breaking on comments

## 🏗️ Architecture

The system consists of three main components:

### 1. Drawing Agent (`main.py`)
- Interprets user drawing requests
- Generates geometric instructions using AI
- Executes drawing commands on the pygame canvas
- Handles the main application loop

### 2. Manager Agent (`manager_agent.py`)
- Evaluates completed drawings using image analysis
- Provides feedback on drawing quality
- Decides whether to redraw or accept the current result
- Uses GPT-4o-mini with vision capabilities

### 3. Drawing Tools (`tools.py`)
- `draw_line()`: Draws lines between specified points
- `draw_circle()`: Draws circles with specified center and radius
- `draw_rectangle()`: Draws rectangles with specified dimensions

## 🎯 Usage

### Basic Commands

1. **Start Drawing**: Run the application and enter your drawing request
   ```
   Enter a question: Draw a house
   ```

2. **Clear Canvas**: Clear the current drawing
   ```
   Enter a question: clear
   ```

3. **View Results**: The system will:
   - Generate drawing instructions
   - Execute the drawing on the canvas
   - Save the image as `drawing.png`
   - Get manager feedback
   - Redraw if needed based on feedback

### Drawing Examples

- **Simple shapes**: "Draw a circle in the center"
- **Complex objects**: "Draw a house with a roof and door"
- **Multiple elements**: "Draw a tree with branches and leaves"
- **Geometric patterns**: "Draw a star with 5 points"

### How It Works

1. **User Input**: You describe what you want to draw
2. **Drawing Agent**: AI interprets your request and generates geometric instructions
3. **Canvas Drawing**: The system draws shapes on the pygame canvas
4. **Image Capture**: The current canvas is saved as an image
5. **Manager Evaluation**: Another AI agent evaluates the drawing quality
6. **Feedback Loop**: If needed, the system redraws based on manager feedback
7. **Completion**: When satisfied, the final drawing is saved

## 🔧 Technical Details

### AI Models Used
- **Drawing Agent**: GPT-4o/GPT-4o-mini for instruction generation
- **Manager Agent**: GPT-4o/GPT-4o-mini with vision for image evaluation
