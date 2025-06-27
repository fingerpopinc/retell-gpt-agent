from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/", defaults={"path": ""}, methods=["POST"])
@app.route("/<path:path>", methods=["POST"])
def chat(path):
    try:
        data = request.json
        messages = data.get("messages", [])

        if not messages:
            return jsonify({"response": "Sorry, I didn’t catch that."})

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
        )
        reply = response.choices[0].message.content
        return jsonify({"response": reply})
    except Exception as e:
        print("Error:", e)
        return jsonify({"response": "Something went wrong. Try again later."}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
