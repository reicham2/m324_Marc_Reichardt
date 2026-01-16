# CI/CD Pipeline Setup & Konfiguration

## Überblick

Diese Pipeline implementiert ein modernes CI/CD System mit:
- **Automatische Tests & Code Quality** auf jedem Push
- **Docker Image Publishing** auf DockerHub
- **Automatisches Cloud Deployment** auf Render

## 🔑 Schritt 1: GitHub Secrets einrichten

### 1.1 In GitHub Repository gehen
```
GitHub → Repository → Settings → Secrets and variables → Actions
```

### 1.2 Neue Secrets hinzufügen

#### DOCKER_USERNAME
- **Wert:** Dein DockerHub Benutzername
- **Beispiel:** `marcreichardt`

#### DOCKER_PASSWORD
- **Wert:** DockerHub Access Token (NICHT dein Passwort!)
- **So erstellst du ein Token:**
  1. Gehe zu [Docker Hub Account Settings](https://hub.docker.com/settings/security)
  2. Klicke "New Access Token"
  3. Gib einen Namen ein (z.B. "GitHub Actions")
  4. Kopiere den Token (wird nur 1x angezeigt!)

#### RENDER_DEPLOY_HOOK_URL
- **Wert:** Deploy Hook von Render
- **So erhältst du den Hook:**
  1. Erstelle einen Web Service auf Render
  2. Gehe zu Service Settings → Deploy Hook
  3. Kopiere die vollständige URL

#### RENDER_SERVICE_URL (Optional)
- **Wert:** Die öffentliche URL deines Render Services
- **Beispiel:** `https://m324-app.onrender.com`

## 🐳 Schritt 2: DockerHub Repository vorbereiten

### 2.1 Repository erstellen
```bash
# Auf DockerHub.com anmelden
# Neues Repository erstellen:
#   Name: m324-app
#   Description: M324 CI/CD Demo
#   Visibility: Public
```

### 2.2 Lokal testen (optional)
```bash
# Lokal bauen
cd task-6
docker build -t dein-username/m324-app:latest .

# Lokal pushen (zum Testen)
docker login
docker push dein-username/m324-app:latest
```

## 🚀 Schritt 3: Render Service einrichten

### 3.1 Neuen Web Service erstellen
1. Gehe zu [render.com](https://render.com) → Dashboard
2. Klicke "New +" → "Web Service"
3. Wähle "Public Git repository" oder "Docker registry"

### 3.2 Docker-Konfiguration
```
Service name: m324-app
Registry: Docker Hub
Image URL: dein-username/m324-app:latest
Region: Frankfurt (eu-central-1)
Plan: Free
```

### 3.3 Environment Variables setzen
```
MYSQL_HOST=your_mysql_host
MYSQL_USER=demo
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=demo
FLASK_ENV=production
```

### 3.4 Deploy Hook kopieren
1. Service Settings → Deploy Hook
2. Copy den Link
3. In GitHub Secret `RENDER_DEPLOY_HOOK_URL` einfügen

### 3.5 PostgreSQL-Alternative (wenn MySQL auf Render nicht möglich)
Falls du PostgreSQL verwenden möchtest:
1. Füge PostgreSQL-Service zu Render hinzu
2. Kopiere die Connection String
3. Passe app.py an für PostgreSQL statt MySQL

## 📋 Schritt 4: Workflow testen

### 4.1 Lokale Tests ausführen
```bash
# In der task-6 Verzeichnis gehen
cd task-6

# Dependencies installieren
pip install -r requirements.txt

# Tests laufen
pytest -v

# Linting Check
flake8 app.py
black --check app.py
isort --check-only app.py
```

### 4.2 Docker lokal bauen
```bash
cd task-6
docker build -t m324-app:test .
docker run -p 5002:5002 m324-app:test
# http://localhost:5002 aufrufen
```

### 4.3 Workflow starten
```bash
# Code pushen triggert automatisch die Pipeline
git add .
git commit -m "feat: add CI/CD pipeline"
git push origin main

# GitHub → Actions → Workflow Run anschauen
```

## 🔍 Pipeline-Stages im Detail

### Stage 1: CI (Code Quality & Tests)
```yaml
Jobs:
  ✓ Code Checkout
  ✓ Python 3.11 Setup
  ✓ pip Cache Nutzung
  ✓ Dependencies Installation
  ✓ Flake8 Linting (max-line-length: 127)
  ✓ Black Format Check
  ✓ isort Import Sort Check
  ✓ Pytest Unit Tests
  ✓ Test Results Report
```

**Trigger:** Jeder Push & Pull Request auf main

### Stage 2: Build & Push
```yaml
Jobs:
  ✓ Dockerfile Parse
  ✓ Docker Buildx Setup (Multi-Platform)
  ✓ DockerHub Login
  ✓ Tag Generation (latest + commit-sha)
  ✓ Layer Caching (GitHub Actions Cache)
  ✓ Image Build & Push
  ✓ Image Verification
```

**Trigger:** Push auf main oder Tag `v*`  
**Bedingung:** Nur wenn CI erfolgreich ist

### Stage 3: Deploy
```yaml
Jobs:
  ✓ Checkout Latest Code
  ✓ Render Deploy Hook POST
  ✓ Deployment Triggering
  ✓ Status Notification
```

**Trigger:** Push auf main  
**Bedingung:** Nur wenn Build & Push erfolgreich ist  
**Nicht triggern bei:** Pull Requests, anderen Branches, Tags

## 🔒 Sicherheit

### Secrets Best Practices
- ✅ Verwende **Access Tokens**, nicht Passwörter
- ✅ Secrets sind **nicht sichtbar** in Logs
- ✅ Secrets nur in **authorized** Branches
- ✅ Regelmäßig **rotieren** (Token erneuern)

### Credential Handling
```yaml
# ❌ FALSCH
docker login --username $DOCKER_USERNAME --password $DOCKER_PASSWORD

# ✅ RICHTIG (automatisch durch GitHub)
- uses: docker/login-action@v3
  with:
    username: ${{ secrets.DOCKER_USERNAME }}
    password: ${{ secrets.DOCKER_PASSWORD }}
```

## 🐛 Troubleshooting

### Problem: "Unauthorized to access Docker image"
**Lösung:**
- Check: DockerHub Username/Token in GitHub Secrets
- Token erstellen auf dockerhub.com
- Repository auf DockerHub existiert?

### Problem: "Deploy Hook returned 404"
**Lösung:**
- Render Service existiert?
- Deploy Hook URL korrekt kopiert?
- URL endet auf `/deploy`?

### Problem: "MySQL Connection refused"
**Lösung:**
- MYSQL_HOST korrekt in Render ENV?
- Database existiert?
- Firewall Port 3306 offen?

### Problem: "Tests failed locally but not in GitHub"
**Lösung:**
```bash
# Gleiche Python-Version testen
python3.11 -m venv venv
source venv/bin/activate
pip install -r task-6/requirements.txt
pytest task-6/
```

### Problem: "Docker layer cache not working"
**Lösung:**
- Buildx Cache ist auf GitHub Actions optional
- Disable im Workflow: `cache-from: type=registry`

## 📈 Monitoring & Logging

### GitHub Actions Logs
```
Repository → Actions → [Workflow Name] → [Run] → [Job] → Logs
```

### DockerHub Builds
```
DockerHub.com → Repositories → m324-app → Tags → Build Status
```

### Render Deployment
```
Render Dashboard → m324-app → Logs → Event Log
```

## 🔄 Weitere Verbesserungen (Optional)

### OIDC Token für DockerHub
Sicherer als Access Token:
```yaml
- uses: docker/login-action@v3
  with:
    registry: docker.io
    username: ${{ secrets.DOCKER_USERNAME }}
    password: ${{ secrets.DOCKER_PASSWORD }}
```

### Code Coverage Reports
```bash
pip install coverage
coverage run -m pytest task-6/
coverage report
```

### Multi-Platform Builds
```yaml
platforms: |
  linux/amd64
  linux/arm64
```

### Slack Notifications
```yaml
- name: Notify Slack
  if: failure()
  uses: slackapi/slack-github-action@v1
  with:
    webhook-url: ${{ secrets.SLACK_WEBHOOK }}
```

## 📚 Weitere Ressourcen

- [GitHub Actions Dokumentation](https://docs.github.com/en/actions)
- [Docker GitHub Actions](https://github.com/docker/build-push-action)
- [Render Deploy Hooks](https://render.com/docs/deploy-hooks)
- [DockerHub Access Tokens](https://docs.docker.com/docker-hub/access-tokens/)
