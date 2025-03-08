# Application de Transcription Audio en Texte

Cette application web permet de télécharger un fichier audio et de le transcrire en texte à l'aide du modèle Whisper d'OpenAI. Elle prend en charge plusieurs transcriptions simultanées et offre une interface utilisateur intuitive.

## Fonctionnalités

- Transcription de fichiers audio en texte
- Support de plusieurs formats audio (MP3, WAV, M4A, OGG, FLAC)
- Traitement de plusieurs fichiers en parallèle
- Interface utilisateur moderne et réactive
- Téléchargement automatique des fichiers texte générés

## Déploiement sur Render

Cette application est optimisée pour être déployée sur [Render](https://render.com/).

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
   - `MAX_CONTENT_LENGTH=2097152`
   - `MAX_AUDIO_DURATION=60`
   - `SECRET_KEY=votre_clé_secrète`

## Optimisations pour Render

Cette application a été spécialement optimisée pour fonctionner sur le plan gratuit de Render :

1. **Modèle Whisper "tiny"** : Utilisation du modèle le plus léger pour économiser la mémoire
2. **Limitation de la taille des fichiers** : Maximum 2 Mo pour éviter les problèmes de mémoire
3. **Limitation de la durée audio** : Maximum 60 secondes pour éviter les timeouts
4. **Gestion optimisée de la mémoire** : Libération explicite de la mémoire après chaque transcription
5. **Installation automatique de FFmpeg** : Via le fichier `apt-packages.txt`

## Limitations du plan gratuit de Render

- **Mise en veille** : L'application se met en veille après 15 minutes d'inactivité
- **Temps de démarrage** : Le premier accès après une période d'inactivité peut prendre 30-60 secondes
- **Ressources limitées** : 512 Mo de RAM, ce qui explique les limitations de taille et de durée des fichiers

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

## Configuration

L'application peut être configurée via des variables d'environnement. Consultez le fichier `.env` pour voir les options disponibles. 