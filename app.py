from flask import Flask, request, jsonify
import openai
import os
import logging

app = Flask(__name__)
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Enable logging
logging.basicConfig(level=logging.INFO)

@app.route("/", defaults={"path": ""}, methods=["POST"])
@app.route("/<path:path>", methods=["POST"])
def chat(path):
    try:
        data = request.json
        app.logger.info("Incoming JSON from Retell:")
        app.logger.info(data)

        # Fallback: handle different JSON formats from Retell
        messages = data.get("messages")
        if not messages:
            user_text = data.get("text") or data.get("utterance") or "Hi"
            messages = [
                {"role": "system", "content": "You are a helpful voice assistant."},
                {"role": "user", "content": user_text}
            ]

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
        )
        reply = response.choices[0].message.content
        return jsonify({"response": reply})
    except Exception as e:
        app.logger.error(f"Error: {e}")
        return jsonify({"response": "Sorry, something broke on my end."}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
