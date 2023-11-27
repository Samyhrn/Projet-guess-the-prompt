from GuessThePrompt import app
from models import db, User, Room, Prompt

def reset_db():
    with app.app_context():
        db.drop_all()
        db.create_all()

# Appeler cette fonction réinitialisera la base de données
reset_db()
