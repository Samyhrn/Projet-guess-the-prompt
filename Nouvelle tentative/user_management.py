# user_management.py
from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        hashed_password = generate_password_hash(password)
        
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('user_bp.dashboard'))
    
    return render_template('register.html')

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            # Connecte l'utilisateur ici
            session['user_id'] = user.id
            return redirect(url_for('user_bp.dashboard'))  # Redirige vers la page de création de room
        else:
            return 'Nom d’utilisateur ou mot de passe incorrect!'
    
    return render_template('login.html')

@user_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Ajouter d'autres routes liées à la gestion des utilisateurs si nécessaire
