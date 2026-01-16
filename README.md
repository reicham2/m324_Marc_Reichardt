# M324 - CI/CD Pipeline mit Docker & GitHub Actions

## Übersicht

Dieses Projekt demonstriert eine vollständige CI/CD Pipeline mit GitHub Actions, Docker und automatischem Cloud Deployment.

## 📋 Anforderungen erfüllt

✅ **CI/CD Pipeline mit 2+ Stages:**
- CI: Linting (flake8), Formatting (black), Import Sorting (isort), Tests (pytest)
- Build & Push: Docker Image zu DockerHub
- Deploy: Automatisches Deployment auf Render

✅ **Deploy nur bei CI-Erfolg:** Deploy Job wird durch `needs: build-and-push` gesteuert

✅ **Deploy nur auf Main/Tags:** `if: github.ref == 'refs/heads/main' || startsWith(github.ref, 'refs/tags/v')`

✅ **DockerHub Publishing:** Mit `latest` und Commit-SHA Tags

✅ **Automatisiertes Deployment:** Deploy Hook/Webhook (nicht manuell)

---

## 🚀 Deployment & Öffentliche URL

### Render Deployment
- **Live URL:** `https://<your-render-service>.onrender.com` (wird nach Deployment-Setup verfügbar)
- **Deployment Method:** Render Deploy Hook
- **Auto-Redeploy:** Bei jedem Push auf `main` Branch

### GitHub Actions Dashboard
- **Workflows:** [GitHub Actions](https://github.com/YOUR-USERNAME/YOUR-REPO/actions)
- **CI/CD Pipeline:** `.github/workflows/ci-cd.yml`
- **Manual Deploy:** `.github/workflows/manual-deploy.yml`

---

## 🔐 Erforderliche Secrets & Umgebungsvariablen

### GitHub Secrets (müssen in GitHub konfiguriert werden)

```
DOCKER_USERNAME          # DockerHub Benutzername
DOCKER_PASSWORD          # DockerHub Access Token oder Passwort
RENDER_DEPLOY_HOOK_URL   # Render Deploy Hook URL
RENDER_SERVICE_URL       # Render Service URL (z.B. https://m324-app.onrender.com)
```

### Umgebungsvariablen in Render (Runtime)

```
MYSQL_HOST               # MySQL Server Host
MYSQL_USER               # MySQL Benutzer
MYSQL_PASSWORD           # MySQL Passwort
MYSQL_DATABASE           # MySQL Datenbank Name
PORT                     # Port (z.B. 5002)
```

---

## 📦 Project Structure

```
├── .github/
│   └── workflows/
│       ├── ci-cd.yml              # Automatische CI/CD Pipeline
│       └── manual-deploy.yml       # Manuelles Deployment
├── task-6/
│   ├── app.py                      # Flask Application
│   ├── Dockerfile                  # Docker Image Definition
│   ├── docker-compose.yml          # Lokale Dev Environment
│   ├── init.sql                    # Datenbank Initialisierung
│   ├── requirements.txt            # Python Dependencies
│   ├── conftest.py                 # Pytest Fixtures
│   ├── test_app.py                 # Unit Tests
│   └── templates/
│       └── index.html              # Frontend Template
├── .gitignore                       # Git Ignore
├── .dockerignore                    # Docker Ignore
└── README.md                        # Diese Datei
```

---

## 🔄 Pipeline Workflow

### 1. **CI Stage** (auf jedem Push & PR)
```
✓ Code Checkout
✓ Python Setup (3.11)
✓ Dependencies Installieren
✓ Linting mit flake8
✓ Format-Check mit black
✓ Import-Check mit isort
✓ Tests mit pytest
```

### 2. **Build & Push Stage** (nur bei main branch push oder Tags)
```
✓ Docker Image bauen
✓ Login zu DockerHub
✓ Tag generieren (latest, commit-sha)
✓ Image zu DockerHub pushen
✓ Cache-Optimierung
```

### 3. **Deploy Stage** (nur bei main branch push nach erfolgreichem Build)
```
✓ Deploy Hook URL aufrufen
✓ Render triggern zum Redeploy
✓ Deployment Status ausgeben
```

---

## 📋 Setup-Anleitung

### 1. GitHub Secrets konfigurieren

Gehe zu **Settings → Secrets and variables → Actions** und füge folgende Secrets hinzu:

```bash
# DockerHub
DOCKER_USERNAME=your_docker_username
DOCKER_PASSWORD=your_docker_token  # Verwende ein Access Token!

# Render
RENDER_DEPLOY_HOOK_URL=https://api.render.com/deploy/...
RENDER_SERVICE_URL=https://your-service.onrender.com
```

### 2. DockerHub vorbereiten

```bash
# Login
docker login

# Erstelle ein Repository: your-docker-username/m324-app

# Optional: Lokal testen
cd task-6
docker build -t your-docker-username/m324-app:latest .
docker push your-docker-username/m324-app:latest
```

### 3. Render Service erstellen

1. Gehe zu [render.com](https://render.com)
2. Erstelle neue **Web Service**
3. Wähle **Docker** als Environment
4. Registry: Docker Hub
5. Image: `your-docker-username/m324-app:latest`
6. Environment Variables setzen (MYSQL_HOST, MYSQL_USER, etc.)
7. Deploy Hook kopieren → in GitHub Secrets speichern

### 4. Lokales Testen

```bash
# Requirements installieren
pip install -r task-6/requirements.txt

# Tests laufen
pytest task-6/

# Linting
flake8 task-6/app.py
black --check task-6/app.py
isort --check-only task-6/app.py

# Docker lokal testen
cd task-6
docker-compose up --build
```

---

## 📊 CI/CD Pipeline Status

| Stage | Trigger | Bedingung | Status |
|-------|---------|-----------|--------|
| CI | Push, PR | Immer | ✓ Aktiv |
| Build & Push | Push | `main` oder Tags `v*` | ✓ Aktiv |
| Deploy | Push | `main` nach Build-Erfolg | ✓ Aktiv |

---

## 🛠️ Troubleshooting

### Build schlägt fehl
- Logs anschauen: GitHub Actions → Workflow Run
- Lokal testen: `docker build -f task-6/Dockerfile task-6/`

### Deploy schlägt fehl
- Deploy Hook URL überprüfen (in GitHub Secrets)
- Render Service Logs überprüfen

### Tests schlagen fehl
- Lokal laufen: `pytest task-6/ -v`
- Abhängigkeiten überprüfen: `pip install -r task-6/requirements.txt`

### DockerHub Push schlägt fehl
- Docker Credentials überprüfen
- Access Token verwenden (kein Passwort)
- Repository-Namen korrekt konfigurieren

---

## 🚀 Features

- ✅ Automatische Tests & Code Quality Checks
- ✅ Docker Image Building & Publishing
- ✅ Automatisches Cloud Deployment
- ✅ Nur erfolgreiche Builds deployen
- ✅ Deployment nur auf Production Branch
- ✅ Version Tags unterstützen (v1.0.0, etc.)
- ✅ Manual Deploy Option
- ✅ Deployment Notifications

---

## 📄 Lizenzen & Technologien

- **Framework:** Flask
- **Database:** MySQL
- **Container:** Docker
- **CI/CD:** GitHub Actions
- **Registry:** DockerHub
- **Hosting:** Render