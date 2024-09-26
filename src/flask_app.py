# src/flask_app.py

from flask import Flask, request, jsonify
from chatbot import get_chatbot_response

app = Flask(__name__)


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message")
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    response = get_chatbot_response(user_input)
    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(debug=True)
