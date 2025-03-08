# Application de Transcription Audio en Texte

Cette application web permet de télécharger un fichier audio et de le transcrire en texte à l'aide du modèle Whisper d'OpenAI. Elle prend en charge plusieurs transcriptions simultanées et offre une interface utilisateur intuitive.

## Fonctionnalités

- Transcription de fichiers audio en texte
- Support de plusieurs formats audio (MP3, WAV, M4A, OGG, FLAC)
- Traitement de plusieurs fichiers en parallèle
- Interface utilisateur moderne et réactive
- Téléchargement automatique des fichiers texte générés

## Déploiement sur Render

Cette application est configurée pour être déployée facilement sur [Render](https://render.com/).

### Étapes de déploiement

1. Créez un compte sur [Render](https://render.com/)
2. Créez un nouveau service Web
3. Connectez votre dépôt GitHub ou téléchargez directement les fichiers
4. Configurez le service avec les paramètres suivants :
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn wsgi:app`
5. Ajoutez les variables d'environnement suivantes :
   - `FLASK_APP=app.py`
   - `FLASK_ENV=production`
   - `WHISPER_MODEL=tiny`
   - `MAX_CONTENT_LENGTH=5242880`
   - `SECRET_KEY=votre_clé_secrète`

## Développement local

### Prérequis

- Python 3.8 ou supérieur
- FFmpeg installé sur votre système

### Installation

1. Clonez ce dépôt ou téléchargez les fichiers
2. Créez un environnement virtuel : `python -m venv venv`
3. Activez l'environnement virtuel :
   - Windows : `venv\Scripts\activate`
   - macOS/Linux : `source venv/bin/activate`
4. Installez les dépendances : `pip install -r requirements.txt`

### Exécution locale

1. Lancez l'application : `python app.py`
2. Ouvrez votre navigateur à l'adresse : http://127.0.0.1:5000

## Limitations

- La taille maximale du fichier est limitée à 5 Mo par défaut
- Le modèle Whisper "tiny" est utilisé par défaut pour économiser les ressources
- Sur le plan gratuit de Render, l'application se met en veille après 15 minutes d'inactivité

## Configuration

L'application peut être configurée via des variables d'environnement. Consultez le fichier `.env` pour voir les options disponibles. 