from flask import Flask, jsonify, render_template, request, redirect, url_for, session
import spacy

nlps = spacy.load("en_core_web_md")

app = Flask(__name__, static_folder="static", template_folder="templates")

special_characters = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "+", "=", "{", "}", "[", "]", "|", ":", ";", "'", '"', "<", ">", ",", ".", "?", "/", "~", "`"]

connected_users = []

@app.route("/")
def index():
    username = request.args.get("username")
    error = request.args['error'] if 'error' in request.args else None
    return render_template("index.html", error=error, username=username)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Récupérer le nom d'utilisateur depuis le formulaire
        username = request.form.get("username")
        if not username:
            # Si le nom d'utilisateur est vide, retourner une erreur
            return render_template("username.html", error="Username cannot be blank.")
        elif username in connected_users:
            # Si le nom d'utilisateur est déjà connecté, retourner une erreur
            return render_template("username.html", error="Username already taken.")
        else:
            # Ajouter le nom d'utilisateur à la liste des utilisateurs connectés
            connected_users.append(username)
            # Rediriger l'utilisateur vers la page du lobby
            return redirect(url_for("lobby", username=username))
    else:
        # Si la méthode HTTP n'est pas POST, retourner la page pour choisir un nom d'utilisateur
        return render_template("username.html")
    

@app.route("/lobby")
def lobby():
    # Vérifier que l'utilisateur est connecté avant d'afficher la page du lobby
    username = request.args.get("username")
    if username not in connected_users:
        return render_template("index.html", error="You must be logged in to access the lobby.")
    return render_template("lobby.html", username=username, connected_users=connected_users)


@app.route("/get_users")
def get_users():
    return jsonify(connected_users)

@app.route("/guess", methods=["POST"])
def guess():
    phrase = request.form["phrase"]
    #get the prompt string from the generated image and store it in a variable
    prompt_string = response.text
    if phrase=="":
        return render_template("guess.html", error="Phrase cannot be blank.")
    if phrase.isnumeric():
        return render_template("guess.html", error="Phrase cannot be numeric.")
    if phrase.isdecimal():
        return render_template("guess.html", error="Phrase cannot be decimal.")
    if len(phrase) > 100:
        return render_template("guess.html", error="Phrase cannot be longer than 100 characters.")
    if len(phrase) < 5:
        return render_template("guess.html", error="Phrase cannot be shorter than 5 characters.")
    if phrase in special_characters:
        return render_template("guess.html", error="Phrase cannot contain special characters.")
    doc1 = nlps(phrase)
    doc2 = nlps(prompt_string)
    similarity = doc1.similarity(doc2)
    percentage=round(similarity*100,2)
    if percentage > 80:
        return render_template("guess.html", error="You are getting there. Current similarity is "+str(percentage)+"%")
    elif percentage > 90:
        return render_template("guess.html", error="You are almost there. Current similarity is "+str(percentage)+"%")
    else:
        return render_template("guess.html", error="Try again, current similarity is "+str(percentage)+"%")
    

@app.route('/generate-image', methods=['POST'])
def generate_image():
    import base64
    import os
    import requests

    prompt_string = request.form["phrase prompt"]
    if prompt_string=="":
        return render_template("generate.html", error="Phrase cannot be blank.")
    if prompt_string.isnumeric():
        return render_template("generate.html", error="Phrase cannot be numeric.")
    if prompt_string.isdecimal():
        return render_template("generate.html", error="Phrase cannot be decimal.")
    if len(prompt_string) > 100:
        return render_template("generate.html", error="Phrase cannot be longer than 100 characters.")
    if len(prompt_string) < 5:
        return render_template("generate.html", error="Phrase cannot be shorter than 5 characters.")

    engine_id = "stable-diffusion-v1-5"
    api_host = os.getenv('API_HOST', 'https://api.stability.ai')
    api_key = "sk-83pLdqWNDfPpPRfwpTSMSTwmNbrqpv3AfyV5BRXmvUZuR0fQ"

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
                    "text": prompt_string,
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

    return jsonify(data)
