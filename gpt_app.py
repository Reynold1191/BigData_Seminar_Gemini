import os
import utils
import fetcher

from dotenv import load_dotenv
from openai import OpenAI
from flask import Flask, jsonify, render_template, request, session

load_dotenv()


client = OpenAI()
app = Flask(__name__)


def format_message(role, content):
    return {"role": role, "content": content}

def get_response(messages):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    content = completion.choices[0].message.content
    return content

prompt = """
Your task now is to read all the comments from a livestream and summarize in 1 short sentence what people seem to be talking about

The data you will work with are multiple comments separated by a new line.

Thank you!
"""


@app.route('/')
def index():
    return render_template('chat.html', chat_history=[], name='GPT-3')

@app.route('/chat', methods=['POST'])
def chat_endpoint():
    try:
        user_input = request.json.get('user_input')
        print("User input received:", user_input)

        if (data := utils.read_youtube_livestream_link(user_input)):
            messages = [format_message("system", prompt),
                        format_message("user", data)]
            
            response = get_response(messages)

            return jsonify({"response": response, "type": "single"})
        elif user_input.endswith(".csv"):
            data = utils.read_csv(user_input)
            if not data:
                return jsonify({"error": "Could not read the CSV file."}), 400
            
            messages = [format_message("system", prompt),
                        format_message("user", data)]

            response = get_response(messages)

            return jsonify({"response": response, "type": "single"})

        elif user_input:
            messages = [format_message("system", prompt),
                        format_message("user", user_input)]
            
            response = get_response(messages)
            
            return jsonify({"response": response, "type": "single"})
        else:
            return jsonify({"error": "No user input provided."}), 400
    except Exception as e:
        print("Exception occurred:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)