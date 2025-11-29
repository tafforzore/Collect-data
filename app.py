from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import requests
import json
import base64
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'votre_cle_secrete_ici'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# URL de votre Google Apps Script
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzAZksClzf5hQKC6QJrR7aeJQfuQQQ0hKbl8NE1UpRWlQqZouVn7mN0guiW8STlPJYlNw/exec"

# Créer le dossier uploads s'il n'existe pas
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

def image_to_base64(image_path):
    """Convertit une image en base64"""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        print(f"Erreur conversion image: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add-plant', methods=['GET', 'POST'])
def add_plant():
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            virtues = request.form.get('virtues')
            photos = []
            
            # Traitement des images
            if 'photos' in request.files:
                files = request.files.getlist('photos')
                for file in files:
                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        file.save(filepath)
                        
                        # Convertir en base64
                        base64_image = image_to_base64(filepath)
                        if base64_image:
                            photos.append(base64_image)
                        
                        # Supprimer le fichier temporaire
                        os.remove(filepath)
            
            # Préparation des données pour l'API
            plant_data = {
                "name": name,
                "virtues": virtues,
                "photos": photos
            }
            
            # Envoi vers Google Apps Script
            response = requests.post(
                GOOGLE_SCRIPT_URL,
                json=plant_data,
                headers={'Content-Type': 'application/json'}
            )
            print(response)
            if response.status_code == 200:
                flash('Plante enregistrée avec succès!', 'success')
                return redirect(url_for('plants'))
            else:
                flash('Erreur lors de l\'enregistrement', 'error')
                
        except Exception as e:
            flash(f'Erreur: {str(e)}', 'error')
    
    return render_template('add_plant.html')

@app.route('/plants')
def plants():
    try:
        # Récupérer les plantes depuis l'API
        response = requests.get(GOOGLE_SCRIPT_URL)
        if response.status_code == 200:
            plants_data = response.json()
        else:
            plants_data = []
    except:
        plants_data = []
    
    return render_template('plants.html', plants=plants_data)

@app.route('/api/plants', methods=['POST'])
def api_add_plant():
    """API endpoint pour ajouter une plante"""
    try:
        data = request.get_json()
        
        response = requests.post(
            GOOGLE_SCRIPT_URL,
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        
        return jsonify({
            'success': response.status_code == 200,
            'message': 'Plante ajoutée avec succès' if response.status_code == 200 else 'Erreur'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)