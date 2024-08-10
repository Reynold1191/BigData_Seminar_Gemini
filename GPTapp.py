from openai import OpenAI
from flask import Flask, jsonify, render_template, request, session


app = Flask(__name__)
# client = OpenAI(api_key="")

def format_message(role, content):
    return {"role": role, "content": content}

def get_response(messages):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    content = completion.choices[0].message.content
    return content

prompt = '''Your task is to find 3-4 most important keywords in the given paragraph'''

chat_history = []
@app.route('/')
def index():
    return render_template('chat.html', chat_history=chat_history)

@app.route('/chat', methods=['POST'])
def chat_endpoint():
    try:
        user_input = request.json.get('user_input')
        print("User input received:", user_input)
        
        if user_input:
            messages = [format_message("system", prompt),
                        format_message("user", user_input)]
            print("Messages constructed:", messages)
            
            response = get_response(messages)
            print("Response received:", response)
            
            # Directly return the response since it's already a string
            return jsonify({"response": response})
        else:
            return jsonify({"error": "No user input provided."}), 400
    except Exception as e:
        print("Exception occurred:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)