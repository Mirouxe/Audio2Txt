# Guide de déploiement sur Render

Ce guide vous explique comment déployer votre application de transcription audio sur Render, étape par étape.

## Prérequis

- Un compte Render (inscription gratuite sur [render.com](https://render.com/))
- Votre code source prêt à être déployé

## Option 1 : Déploiement via GitHub

### Étape 1 : Préparer votre dépôt GitHub

1. Créez un nouveau dépôt sur GitHub
2. Poussez votre code vers ce dépôt :
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/votre-nom/votre-repo.git
   git push -u origin main
   ```

### Étape 2 : Connecter Render à GitHub

1. Connectez-vous à votre compte Render
2. Cliquez sur "New" puis "Web Service"
3. Choisissez "Connect to GitHub"
4. Autorisez Render à accéder à vos dépôts GitHub
5. Sélectionnez le dépôt que vous venez de créer

### Étape 3 : Configurer le service

1. Donnez un nom à votre service (ex: "transcription-audio")
2. Laissez la branche par défaut (main)
3. Sélectionnez "Python 3" comme environnement
4. Définissez la commande de build : `pip install -r requirements.txt`
5. Définissez la commande de démarrage : `gunicorn wsgi:app`
6. Sélectionnez le plan "Free"

### Étape 4 : Configurer les variables d'environnement

Ajoutez les variables d'environnement suivantes :
- `FLASK_APP` = `app.py`
- `FLASK_ENV` = `production`
- `WHISPER_MODEL` = `tiny`
- `MAX_CONTENT_LENGTH` = `5242880`
- `SECRET_KEY` = `une_clé_aléatoire_sécurisée` (ou laissez Render en générer une)

### Étape 5 : Déployer

1. Cliquez sur "Create Web Service"
2. Render va automatiquement construire et déployer votre application
3. Le processus prend généralement 5-10 minutes

## Option 2 : Déploiement direct (sans GitHub)

### Étape 1 : Préparer votre code

1. Assurez-vous que tous les fichiers nécessaires sont présents :
   - `app.py`
   - `wsgi.py`
   - `requirements.txt`
   - `templates/index.html`
   - `Procfile`
   - `runtime.txt`
   - `render.yaml` (optionnel)
   - Dossier `uploads` avec `.gitkeep`

2. Compressez tous ces fichiers dans un fichier ZIP

### Étape 2 : Créer un nouveau service sur Render

1. Connectez-vous à votre compte Render
2. Cliquez sur "New" puis "Web Service"
3. Choisissez "Upload Files"
4. Téléchargez votre fichier ZIP
5. Cliquez sur "Next"

### Étape 3 : Configurer le service

1. Donnez un nom à votre service (ex: "transcription-audio")
2. Sélectionnez "Python 3" comme environnement
3. Définissez la commande de build : `pip install -r requirements.txt`
4. Définissez la commande de démarrage : `gunicorn wsgi:app`
5. Sélectionnez le plan "Free"

### Étape 4 : Configurer les variables d'environnement

Ajoutez les variables d'environnement suivantes :
- `FLASK_APP` = `app.py`
- `FLASK_ENV` = `production`
- `WHISPER_MODEL` = `tiny`
- `MAX_CONTENT_LENGTH` = `5242880`
- `SECRET_KEY` = `une_clé_aléatoire_sécurisée` (ou laissez Render en générer une)

### Étape 5 : Déployer

1. Cliquez sur "Create Web Service"
2. Render va automatiquement construire et déployer votre application
3. Le processus prend généralement 5-10 minutes

## Accès à votre application

Une fois le déploiement terminé :
1. Render vous fournira une URL (comme `https://transcription-audio.onrender.com`)
2. Partagez cette URL avec vos utilisateurs
3. Ils pourront accéder à l'application et l'utiliser sans aucune installation

## Limitations du plan gratuit de Render

- **Mise en veille** : L'application se met en veille après 15 minutes d'inactivité
- **Temps de démarrage** : Lorsqu'un utilisateur accède à l'application après une période d'inactivité, le premier chargement peut prendre 30-60 secondes
- **Ressources limitées** : 512 Mo de RAM, ce qui est pourquoi nous utilisons le modèle "tiny"
- **Bande passante** : 100 Go/mois (largement suffisant pour tester)

## Dépannage

### L'application ne démarre pas

Vérifiez les logs dans l'interface Render pour identifier le problème. Les erreurs courantes sont :
- Dépendances manquantes dans `requirements.txt`
- Erreur dans la commande de démarrage
- Variables d'environnement mal configurées

### L'application est lente

- Le premier chargement après une période d'inactivité est normal (30-60 secondes)
- Si l'application reste lente, envisagez de passer à un plan payant pour plus de ressources

### Erreurs de mémoire

- Utilisez le modèle Whisper "tiny" pour économiser la mémoire
- Limitez la taille des fichiers audio à transcrire
- Envisagez de passer à un plan payant pour plus de mémoire 