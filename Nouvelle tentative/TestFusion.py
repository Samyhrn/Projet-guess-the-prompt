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
        with open (f"Nouvelle tentative//static//image.png", "wb") as f:
            f.write(base64.b64decode(image["base64"]))

    return render_template('guess.html', text_to_guess=text_prompt,trial_number=0,percentage=0)

@app.route('/guess/<prompt>/<trial_number>')
def init_guess(prompt,trial_number):
    print("On est dans guess en get")
    return render_template('guess.html', text_to_guess=prompt,trial_number=trial_number,percentage=0)


#@app.route('/guess/<trials_number>/<prompt>', methods=['GET'])
@app.route('/guess', methods=['POST'])
def guess():
    trials_number = 1
    text_to_guess= request.form['text_to_guess']#prompt
    trials_number = int(request.form['trial_number'])
    if trials_number >= 3:
        return render_template('lose.html', original_sentence=text_to_guess)
    trials_number += 1
    similarity = 0
    text_to_guess_index = nlp(text_to_guess)
    text_guessing = request.form['text_prompt']
    text_guessing_index = nlp(text_guessing)
    similarity = text_to_guess_index.similarity(text_guessing_index) 
    if similarity > 0.98:
        return render_template('win.html', original_sentence=text_to_guess)
    return render_template('guess.html',text_to_guess=text_to_guess, trial_number=trials_number,percentage=similarity*100)

            

if __name__ == '__main__':
    app.run(debug=True)


