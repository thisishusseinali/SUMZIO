import requests 
from flask import Flask, render_template, url_for
from flask import request as req

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def Index():
    return render_template("index.html")

@app.route("/summarize", methods=["GET", "POST"])
def summarize():
    if req.method == "POST":
        API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
        api_token = "YOUR_HUGGING_FACE_API_TOKEN"  # Replace with your actual Hugging Face API token
        headers = {"Authorization": f"Bearer {api_token}"}

        data = req.form["data"]
        max_length = int(req.form["maxL"])
        min_length = max_length // 4

        payload = {
            "inputs": data,
            "parameters": {"min_length": min_length, "max_length": max_length, "do_sample": False}
        }

        response = requests.post(API_URL, headers=headers, json=payload)
        
        # Print the response for debugging
        # print(response.json())

        # Check if "summary_text" is in the response
        if response.json():
            output = response.json()[0]["summary_text"]
            return render_template("index.html", result=output)
        else:
            return render_template("index.html", result="Error: Summary not found in the response.")

    else:
        return render_template("index.html")

if __name__ == '__main__':
    app.debug = True
    app.run()

