from GuessThePrompt import app
from models import db, User, Room, Prompt

def purge_db():
    with app.app_context():
        try:
            db.session.query(User).delete()
            db.session.query(Room).delete()
            db.session.query(Prompt).delete()
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(str(e))

# Appeler cette fonction purgera toutes les données
purge_db()
