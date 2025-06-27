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

    try:
        # Read raw body text from Retell
        raw_input = request.data.decode("utf-8").strip()
        app.logger.info(f"🗣️ Retell raw input: {raw_input}")

        messages = [
            {"role": "system", "content": "You are a warm, natural-sounding voice assistant."},
            {"role": "user", "content": raw_input or "Hi"}
        ]

        # New OpenAI v1 client call
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
        )
        reply = response.choices[0].message.content.strip()
        return jsonify({"response": reply})

    except Exception as e:
        app.logger.error(f"💥 Error: {e}")
        return jsonify({"response": "Something went wrong, but I'm still here!"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
