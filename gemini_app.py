import pandas as pd
import utils
import google.generativeai as genai

from flask import Flask, jsonify, render_template, request, session
from dotenv import load_dotenv

load_dotenv()


genai.configure()
app = Flask(__name__)

model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])
prompt = """
Your task now is to classify comments as Positive, Negative, or Neutral. 

The data you will work with is comments read from a CSV file. Each comment is separated by a new line. 

Please classify each comment according to the following criteria:
- Positive: The comment expresses satisfaction, approval, or a positive sentiment.
- Negative: The comment expresses dissatisfaction, disapproval, or a negative sentiment.
- Neutral: The comment is neither positive nor negative, and does not express a strong sentiment.

Here is the example data string: The product is amazing, I am very satisfied!;
 Customer service was terrible, I am very disappointed.; The product is okay, nothing special.;
 I am very pleased with the quality of the product.;
 Delivery was slow and I couldn’t track the order.; Everything is fine, no complaints.

Please provide your classification for each comment in the format, keep it in one line only:
[{Comment1: Setiment1}, {Comment2: Setiment2}, ... ]

For example:
[{The product is amazing, I am very satisfied!: Positive}, {Customer service was terrible, I am very disappointed.: Negative}]

Thank you!
"""
chat.send_message(prompt)

# chat_history = []

safe = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]


@app.route("/")
def index():
    return render_template(
        "chat.html", chat_history=[], name="Gemini", title="Sentiment Analysis"
    )


@app.route("/chat", methods=["POST"])
def chat_endpoint():
    try:
        user_input = request.json.get("user_input")
        print(user_input)

        if data := utils.read_youtube_video_link(user_input):
            response = chat.send_message(data, safety_settings=safe)
            print(1)
            print(response)
            formatted_response = utils.format_response(response.text)

            return jsonify({"response": formatted_response, "type": "list"})
        elif user_input.endswith(".csv"):
            data = utils.read_csv(user_input)

            if not data:
                return jsonify({"error": "Could not read the CSV file."}), 400

            response = chat.send_message(data)
            formatted_response = utils.format_response(response.text)
            print(response.text)

            return jsonify({"response": formatted_response, "type": "list"})
        elif user_input:
            response = chat.send_message(user_input)
            formatted_response = utils.format_response(response.text)
            sentiment = formatted_response[0]["sentiment"]

            # chat_history.append({"user": user_input, "bot": response.text})
            return jsonify({"response": sentiment, "type": "single"})
        else:
            return jsonify({"error": "No user input provided."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(port=5000)
