from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/", methods=["POST"])
def chat():
    data = request.json
    messages = data.get("messages", [])

    if not messages:
        return jsonify({"response": "Sorry, I didn’t catch that."})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
        )
        return jsonify({"response": response.choices[0].message.content})
    except Exception as e:
        print("Error:", e)
        return jsonify({"response": "Something went wrong. Try again later."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
