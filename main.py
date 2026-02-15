# API_BACKEND.PY - À lancer en même temps que le bot

from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)  # Permet les requêtes depuis le site web

# Chemin vers la base de données du bot
DB_PATH = 'roblox_users.db'  # Même DB que le bot

@app.route('/api/scripts/<user_id>', methods=['GET'])
def get_user_scripts(user_id):
    """Récupère tous les scripts d'un utilisateur"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Récupère les scripts de l'utilisateur
        cursor.execute('''
            SELECT id, script_name, script_code, script_type, created_at 
            FROM scripts 
            WHERE discord_id = ? 
            ORDER BY created_at DESC
        ''', (user_id,))
        
        scripts = cursor.fetchall()
        conn.close()
        
        # Formate les résultats
        result = []
        for script in scripts:
            result.append({
                'id': script[0],
                'name': script[1],
                'code': script[2],
                'type': script[3],
                'created_at': script[4],
                'description': f"Script {script[3]}"
            })
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/user/<user_id>', methods=['GET'])
def get_user_info(user_id):
    """Récupère les infos d'un utilisateur"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT discord_id, credits, user_key, language, created_at 
            FROM users 
            WHERE discord_id = ?
        ''', (user_id,))
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return jsonify({
                'id': user[0],
                'credits': user[1],
                'key': user[2],
                'language': user[3],
                'created_at': user[4]
            })
        else:
            return jsonify({'error': 'User not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Statistiques globales"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM users')
        total_users = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM scripts')
        total_scripts = cursor.fetchone()[0]
        
        conn.close()
        
        return jsonify({
            'total_users': total_users,
            'total_scripts': total_scripts
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 API Backend démarrée sur http://localhost:3000")
    print("📊 Endpoints disponibles:")
    print("   - GET /api/scripts/<user_id>")
    print("   - GET /api/user/<user_id>")
    print("   - GET /api/stats")
    app.run(host='0.0.0.0', port=3000, debug=True)
