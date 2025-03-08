import os
import whisper
from flask import Flask, render_template, request, send_file, redirect, url_for, jsonify, session
from werkzeug.utils import secure_filename
from pydub import AudioSegment
import tempfile
import uuid
import threading
import time
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER', 'uploads')
app.config['ALLOWED_EXTENSIONS'] = {'mp3', 'wav', 'm4a', 'ogg', 'flac'}
app.config['MAX_CONTENT_LENGTH'] = int(os.environ.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16 MB par défaut
app.secret_key = os.environ.get('SECRET_KEY', 'transcription_app_secret_key')
app.config['WHISPER_MODEL'] = os.environ.get('WHISPER_MODEL', 'base')  # Modèle Whisper à utiliser

# Créer le dossier uploads s'il n'existe pas
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Dictionnaire pour stocker les tâches de transcription en cours
transcription_tasks = {}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def write_text_with_line_breaks(text, filepath, line_length=100):
    words = text.split()
    current_line = ""
    
    with open(filepath, 'w', encoding='utf-8') as f:
        for word in words:
            if len(current_line) + len(word) + 1 <= line_length:
                if current_line:
                    current_line += " "
                current_line += word
            else:
                f.write(current_line + '\n')
                current_line = word
        
        if current_line:
            f.write(current_line + '\n')

def audio2txt_thread(audio_path, task_id, original_filename):
    try:
        # Mettre à jour le statut de la tâche
        transcription_tasks[task_id]['status'] = 'processing'
        
        # Générer un nom de fichier unique pour éviter les collisions
        unique_id = str(uuid.uuid4())
        wav_path = os.path.join(tempfile.gettempdir(), f"{unique_id}.wav")
        txt_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{unique_id}.txt")
        
        # Convertir en WAV si nécessaire
        file_ext = os.path.splitext(audio_path)[1].lower()
        if file_ext != '.wav':
            audio = AudioSegment.from_file(audio_path)
            audio.export(wav_path, format='wav')
            audio_file_for_whisper = wav_path
        else:
            audio_file_for_whisper = audio_path
        
        # Charger le modèle Whisper et transcrire
        model = whisper.load_model(app.config['WHISPER_MODEL'])
        result = model.transcribe(audio_file_for_whisper)
        text = str(result["text"])
        
        # Écrire le texte dans un fichier
        write_text_with_line_breaks(text, txt_path)
        
        # Nettoyer les fichiers temporaires
        if file_ext != '.wav':
            os.remove(wav_path)
        
        # Mettre à jour le statut de la tâche
        transcription_tasks[task_id]['status'] = 'completed'
        transcription_tasks[task_id]['txt_path'] = txt_path
        transcription_tasks[task_id]['original_filename'] = original_filename
        
        # Nettoyer le fichier audio original
        os.remove(audio_path)
        
    except Exception as e:
        # En cas d'erreur, mettre à jour le statut
        transcription_tasks[task_id]['status'] = 'error'
        transcription_tasks[task_id]['error_message'] = str(e)
        
        # Nettoyer les fichiers si nécessaire
        if 'audio_path' in locals() and os.path.exists(audio_path):
            os.remove(audio_path)
        if 'wav_path' in locals() and os.path.exists(wav_path):
            os.remove(wav_path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': 'Aucun fichier sélectionné'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'status': 'error', 'message': 'Aucun fichier sélectionné'}), 400
    
    if file and allowed_file(file.filename):
        # Générer un ID unique pour cette tâche
        task_id = str(uuid.uuid4())
        
        # Sécuriser le nom du fichier
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{task_id}_{filename}")
        file.save(file_path)
        
        # Créer une entrée pour cette tâche
        transcription_tasks[task_id] = {
            'status': 'queued',
            'file_path': file_path,
            'filename': filename,
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'original_filename': os.path.splitext(filename)[0]
        }
        
        # Démarrer la transcription dans un thread séparé
        thread = threading.Thread(
            target=audio2txt_thread, 
            args=(file_path, task_id, os.path.splitext(filename)[0])
        )
        thread.daemon = True
        thread.start()
        
        # Retourner l'ID de la tâche
        return jsonify({
            'status': 'success', 
            'message': 'Fichier téléchargé avec succès, transcription en cours',
            'task_id': task_id
        })
    
    return jsonify({'status': 'error', 'message': 'Type de fichier non autorisé'}), 400

@app.route('/task_status/<task_id>', methods=['GET'])
def task_status(task_id):
    if task_id not in transcription_tasks:
        return jsonify({'status': 'error', 'message': 'Tâche non trouvée'}), 404
    
    task = transcription_tasks[task_id]
    
    if task['status'] == 'completed':
        return jsonify({
            'status': 'completed',
            'message': 'Transcription terminée',
            'download_url': f'/download/{task_id}'
        })
    elif task['status'] == 'error':
        return jsonify({
            'status': 'error',
            'message': f"Erreur lors de la transcription: {task.get('error_message', 'Erreur inconnue')}"
        })
    else:
        return jsonify({
            'status': task['status'],
            'message': 'Transcription en cours'
        })

@app.route('/download/<task_id>', methods=['GET'])
def download_file(task_id):
    if task_id not in transcription_tasks or transcription_tasks[task_id]['status'] != 'completed':
        return jsonify({'status': 'error', 'message': 'Fichier non disponible'}), 404
    
    task = transcription_tasks[task_id]
    
    # Renvoyer le fichier texte
    return send_file(
        task['txt_path'], 
        as_attachment=True, 
        download_name=f"{task['original_filename']}.txt"
    )

@app.route('/tasks', methods=['GET'])
def list_tasks():
    # Filtrer les informations à renvoyer pour chaque tâche
    tasks_info = {}
    for task_id, task in transcription_tasks.items():
        tasks_info[task_id] = {
            'status': task['status'],
            'filename': task['filename'],
            'created_at': task['created_at']
        }
    
    return jsonify(tasks_info)

# Nettoyage périodique des tâches terminées depuis longtemps
def cleanup_old_tasks():
    while True:
        time.sleep(3600)  # Vérifier toutes les heures
        now = datetime.now()
        to_delete = []
        
        for task_id, task in transcription_tasks.items():
            if task['status'] in ['completed', 'error']:
                created_at = datetime.strptime(task['created_at'], "%Y-%m-%d %H:%M:%S")
                # Supprimer les tâches terminées depuis plus de 24 heures
                if (now - created_at).total_seconds() > 86400:
                    to_delete.append(task_id)
                    # Supprimer le fichier texte si présent
                    if 'txt_path' in task and os.path.exists(task['txt_path']):
                        os.remove(task['txt_path'])
        
        for task_id in to_delete:
            del transcription_tasks[task_id]

# Démarrer le thread de nettoyage
cleanup_thread = threading.Thread(target=cleanup_old_tasks)
cleanup_thread.daemon = True
cleanup_thread.start()

# Point d'entrée pour les applications WSGI
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    debug = os.environ.get('FLASK_ENV', 'production') == 'development'
    app.run(host=host, port=port, debug=debug) 