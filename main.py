from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)  # Permet à n'importe quel site d'accéder à l'API

# ═══════════════════════════════════════════════════════════
# 📊 INITIALISATION DE LA BASE DE DONNÉES
# ═══════════════════════════════════════════════════════════

def init_db():
    """Crée la base de données et la table scripts"""
    conn = sqlite3.connect('scripts.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scripts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            discord_id TEXT NOT NULL,
            script_name TEXT NOT NULL,
            script_code TEXT NOT NULL,
            script_type TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Base de données initialisée")

# Initialise au démarrage
init_db()

# ═══════════════════════════════════════════════════════════
# 🌐 ROUTES API
# ═══════════════════════════════════════════════════════════

@app.route('/')
def home():
    """Page d'accueil - Documentation de l'API"""
    return jsonify({
        'status': 'API ZenithCode en ligne! ✅',
        'version': '1.0',
        'endpoints': {
            'GET /api/scripts/<user_id>': 'Récupère les scripts d\'un utilisateur',
            'POST /api/scripts': 'Ajoute un nouveau script (appelé par le bot)',
            'GET /api/stats': 'Statistiques globales',
            'GET /api/test': 'Test de l\'API'
        },
        'documentation': 'https://github.com/ton-username/zenithcode-api'
    })

@app.route('/api/test')
def test():
    """Route de test"""
    return jsonify({
        'status': 'API fonctionne!',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/scripts/<user_id>', methods=['GET'])
def get_scripts(user_id):
    """
    Récupère tous les scripts d'un utilisateur
    
    Paramètres:
        user_id (str): ID Discord de l'utilisateur
    
    Retour:
        Liste de scripts au format JSON
    """
    try:
        conn = sqlite3.connect('scripts.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, script_name, script_code, script_type, created_at 
            FROM scripts
