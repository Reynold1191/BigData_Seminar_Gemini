from flask import Flask, jsonify, render_template, request, session
import google.generativeai as genai
from api import Gemini_API_KEY as api
import pandas as pd


genai.configure(api_key=api)
model = genai.GenerativeModel('gemini-pro')

app = Flask(__name__)

model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])
prompt = """
Your task now is to classify comments as Positive, Negative, or Neutral. 

The data you will work with is a single string read from a CSV file. Each comment in the string is separated by a semi-colon ';'. 

Please classify each comment according to the following criteria:
- Positive: The comment expresses satisfaction, approval, or a positive sentiment.
- Negative: The comment expresses dissatisfaction, disapproval, or a negative sentiment.
- Neutral: The comment is neither positive nor negative, and does not express a strong sentiment.

Here is the example data string: The product is amazing, I am very satisfied!;
 Customer service was terrible, I am very disappointed.; The product is okay, nothing special.;
 I am very pleased with the quality of the product.;
 Delivery was slow and I couldn’t track the order.; Everything is fine, no complaints.

Please provide your classification for each comment in the format:
- [{Comment 1: Setiment 1}, {Comment 2: Setiment 2}, ... ]

Thank you!
"""
chat.send_message(prompt)

chat_history = []

def read_data(path):
    df = pd.read_csv('data/comments.csv')
    all_comments = '; '.join(df['Comment'])
    return all_comments

@app.route('/')
def index():
    return render_template('chat.html', chat_history=chat_history)

@app.route('/chat', methods=['POST'])
def chat_endpoint():
    try:
        user_input = request.json.get('user_input')
        print(user_input)
        if user_input.endswith(".csv"):
            data = read_data(user_input)
            response = chat.send_message(data)
            chat_history.append({"user": user_input, "bot": response.text})

            return jsonify({"response": response.text})
        elif user_input:
            response = chat.send_message(user_input)
            chat_history.append({"user": user_input, "bot": response.text})

            return jsonify({"response": response.text})
        else:
            return jsonify({"error": "No user input provided."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

