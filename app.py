from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import requests
import json
import base64
import os
import csv
import io
from flask import make_response
from werkzeug.utils import secure_filename
# 1WmQ6_Ms5ho9mQBa4abYkrz47WAJXbfEHZN7_bZCzvKM
app = Flask(__name__)
app.secret_key = 'votre_cle_secrete_ici'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# URL de votre Google Apps Script
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbyoIB5cs79v2-66jVPLomTdf2mfvdRQq_WgYbqtDjpORJ36AsdG4vtqBDE3n9NssCsnpw/exec"

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
    plants_data = []
    try:
        print("cool")
    except Exception as e:
        print(f"Erreur lors de la récupération du CSV : {e}")
    
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
    
@app.route('/plants/download-csv')
def download_csv():
    """Télécharger les données en CSV"""
    try:
        response = requests.get(GOOGLE_SCRIPT_URL+"?mode=csv")
        if response.status_code == 200:
            # Créer la réponse avec le CSV
            output = make_response(response.text)
            output.headers["Content-Disposition"] = "attachment; filename=plantes_medicinales.csv"
            output.headers["Content-type"] = "text/csv; charset=utf-8"
            return output
        else:
            flash("Erreur lors du téléchargement du CSV", "error")
            return redirect(url_for('plants'))
    except Exception as e:
        flash(f"Erreur: {str(e)}", "error")
        return redirect(url_for('plants'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)