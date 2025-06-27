from flask import Flask, request, jsonify
import openai
import os
import logging

app = Flask(__name__)
openai.api_key = os.environ.get("OPENAI_API_KEY")
logging.basicConfig(level=logging.INFO)

@app.route("/", defaults={"path": ""}, methods=["GET", "POST"])
@app.route("/<path:path>", methods=["GET", "POST"])
def chat(path):
    if request.method == "GET":
        return jsonify({"response": "Voice agent is ready."})

    if not request.is_json:
        app.logger.warning("❌ Received non-JSON request.")
        return jsonify({"response": "Invalid request: expecting JSON."}), 400

    try:
        data = request.get_json()
        app.logger.info("📥 Incoming JSON from Retell:")
        app.logger.info(data)

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
        app.logger.error(f"💥 Error: {e}")
        return jsonify({"response": "Sorry, something broke on my end."}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
