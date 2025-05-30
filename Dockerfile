# 1. Image de base officielle Python
FROM python:3.10-slim

# 2. Définir le dossier de travail dans le conteneur
WORKDIR /app

# 3. Copier les fichiers de l'hôte vers le conteneur
COPY . .

# 4. Installer les dépendances
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 5. Exposer le port utilisé par FastAPI
EXPOSE 8000

# 6. Commande de démarrage de l'application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
