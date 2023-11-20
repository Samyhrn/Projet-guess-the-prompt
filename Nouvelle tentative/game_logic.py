# game_logic.py
from flask import Blueprint, render_template, request, redirect, url_for, session
from models import db, User, Room, Prompt

game_bp = Blueprint('game_bp', __name__)

@game_bp.route('/create_room', methods=['GET', 'POST'])
def create_room():
    if request.method == 'POST':
        room_name = request.form['room_name']
        room_password = request.form['room_password']  # Envisage de sécuriser ceci aussi
        players_limit = request.form['players_limit']

        new_room = Room(name=room_name, password=room_password, players_limit=players_limit)
        db.session.add(new_room)
        db.session.commit()
        
        return redirect(url_for('room', room_id=new_room.id))
    
    return render_template('create_room.html')

@game_bp.route('/join_room', methods=['GET', 'POST'])
def join_room():
    if request.method == 'POST':
        room_name = request.form['room_name']
        room_password = request.form['room_password']
        user_id = session.get('user_id')
        if not user_id:
            return redirect(url_for('login'))

        room = Room.query.filter_by(name=room_name, password=room_password).first()
        
        if room:
            user = User.query.get(user_id)
            room.participants.append(user)
            db.session.commit()
            return redirect(url_for('room', room_id=room.id))
        else:
            return 'Room introuvable ou mot de passe incorrect !'
    return render_template('join_room.html')

@game_bp.route('/leave_room/<int:room_id>', methods=['POST'])
def leave_room(room_id):
    user_id = session['user_id']
    room = Room.query.get(room_id)
    user = User.query.get(user_id)
    room.participants.remove(user)
    db.session.commit()
    return redirect(url_for('dashboard'))

@game_bp.route('/room/<int:room_id>')
def room(room_id):
    room = Room.query.get(room_id)
    return render_template('room.html', room=room)

# Ajouter d'autres routes liées au jeu si nécessaire
