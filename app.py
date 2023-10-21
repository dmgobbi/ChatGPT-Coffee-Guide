from dotenv import load_dotenv
import os
import openai
from flask import Flask, redirect, render_template, request, url_for, session

load_dotenv()

app = Flask(__name__)
app.secret_key = 'supersecretkey'
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=("GET", "POST"))
def index():
    session.setdefault('conversation', [])

    if request.method == "POST":
        user_input = request.form["user_input"]
        session['conversation'].append({"role": "user", "content": user_input})
        
        # Detailed Custom Instructions
        prompt = """
        1. ChatGPT's Role: ChatGPT should know that it is responsible for guiding a human in making brewed coffee in a kitchen.

        2. Human Feedback: The human will provide continuous feedback by describing what they see.

        3. Instruction Type: The AI system should only follow short, direct, and specific instructions that can be expressed in natural language.

        4. Complexity Limit: Complex or lengthy tasks are not suitable as the human lacks the knowledge to perform these actions.

        5. Human Capabilities: The human can follow instructions like 'grab the pot with the coffee grounds from above the countertop' and will provide continuous feedback through text descriptions of the current situation.

        6. Desired Response Style: I would like ChatGPT to respond in a manner that is both precise and engaging.

        7. Step-by-Step Guidance: The model should provide one step at a time and then wait for the human's confirmation or description of the current situation before providing the next step.

        8. Example Interaction: For example, if the human says, 'I see a countertop with a coffee pot, a kettle, and a faucet,' ChatGPT could respond with, 'Great! Let's start by grabbing the coffee pot that's on the countertop.' If the human then says, 'I have the coffee pot,' ChatGPT could say, 'Excellent! Now, please grab the kettle that's also on the countertop.'

        9. Key Principles: The key is to keep the instructions simple, direct, and specific, while also maintaining a conversational tone and expecting further input from the human.
        """

        # Add the conversation history to the prompt
        for turn in session['conversation']:
            prompt += f"{turn['role']}: {turn['content']}\n"
        
        # Generate a response from ChatGPT
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.6,
            max_tokens=100
        )
        
        # Add the generated response to the conversation history
        session['conversation'].append({"role": "ChatGPT", "content": response.choices[0].text.strip()})
        # Prints ChatGPT's response to the console
        print(f"ChatGPT: {response.choices[0].text.strip()}")
        session.modified = True  
        return redirect(url_for("index"))
 
    return render_template("index.html", conversation=session['conversation'])

@app.route("/clear", methods=["POST"])
def clear():
    session['conversation'] = []
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
