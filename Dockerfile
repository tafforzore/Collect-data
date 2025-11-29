# Utilise une image Python officielle
FROM python:3.10-slim

# Empêche Python d'écrire des fichiers .pyc
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Créer un dossier pour l'application
WORKDIR /app

# Copier les fichiers requirements
COPY requirements.txt /app/

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY . /app/

# Exposer le port Flask
EXPOSE 5000

# Commande de lancement
CMD ["python", "app.py"]
