from flask import Flask, render_template, request
import base64
import os
import requests
import spacy


app = Flask(__name__)

engine_id = "stable-diffusion-v1-5"
api_host = os.getenv('API_HOST', 'https://api.stability.ai')
api_key = "sk-83pLdqWNDfPpPRfwpTSMSTwmNbrqpv3AfyV5BRXmvUZuR0fQ"

nlp = spacy.load("en_core_web_md")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def generate_image():
    text_prompt = request.form['text_prompt']
    
    if api_key is None:
        raise Exception("Missing Stability API key.")

    response = requests.post(
        f"{api_host}/v1/generation/{engine_id}/text-to-image",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        },
        json={
            "text_prompts": [
                {
                    "text": text_prompt
                }
            ],
            "cfg_scale": 7,
            "clip_guidance_preset": "FAST_BLUE",
            "height": 512,
            "width": 512,
            "samples": 1,
            "steps": 30,
        },
    )

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()

    for i, image in enumerate(data["artifacts"]):
        with open(f"./out/v1_txt2img_{i}.png", "wb") as f:
            f.write(base64.b64decode(image["base64"]))

    return render_template('result.html', text_prompt=text_prompt)


@app.route('/guess')
def guess():
    text_prompt = request.args.get('text_prompt')
    remaining_trials = 3
    doc2 = text_prompt

    while remaining_trials > 0:
        doc1 = request.args.get('doc1')
        doc1 = nlp(doc1)
        doc2 = nlp(doc2)
        similarity = doc1.similarity(doc2)

        percentage = similarity * 100
        if similarity > 0.9:
            return render_template('win.html', original_sentence=doc2)
        else:
            remaining_trials -= 1
            if remaining_trials == 0:
                return render_template('lose.html', original_sentence=doc2)
            else:
                return render_template('guess.html', remaining_trials=remaining_trials, percentage=percentage)
            

if __name__ == '__main__':
    app.run(debug=True)


