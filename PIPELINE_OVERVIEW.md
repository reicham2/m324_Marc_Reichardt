# 📦 CI/CD Pipeline - Übersicht & Quick Start

## Was wurde implementiert?

✅ **Vollständige CI/CD Pipeline** mit GitHub Actions  
✅ **3 Automation Stages**: CI → Build & Push → Deploy  
✅ **Automatisiertes Deployment** auf Render.com  
✅ **DockerHub Image Publishing** mit Latest & SHA Tags  
✅ **Code Quality** mit Linting & Testing  

---

## 🚀 Quick Start (15 Minuten)

### 1️⃣ GitHub Secrets einrichten
```
GitHub Settings → Secrets → Neue Secrets hinzufügen:
- DOCKER_USERNAME
- DOCKER_PASSWORD (Access Token!)
- RENDER_DEPLOY_HOOK_URL
- RENDER_SERVICE_URL
```

→ Siehe: [SETUP_CI_CD.md](SETUP_CI_CD.md#schritt-1-github-secrets-einrichten)

### 2️⃣ Render Service erstellen
```
Render.com Dashboard → New Web Service → Docker
- Image: your-username/m324-app:latest
- Port: 5002
```

→ Siehe: [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

### 3️⃣ Code pushen
```bash
git add .
git commit -m "feat: add CI/CD pipeline"
git push origin main
```

→ GitHub Actions startet automatisch!

### 4️⃣ Monitoring
```
GitHub → Actions → CI/CD Pipeline (Logs anschauen)
```

---

## 📂 Wichtige Dateien

| Datei | Zweck |
|-------|-------|
| [`.github/workflows/ci-cd.yml`](.github/workflows/ci-cd.yml) | Hauptpipeline |
| [`.github/workflows/manual-deploy.yml`](.github/workflows/manual-deploy.yml) | Manuelles Deploy |
| [`README.md`](README.md) | Projekt-Übersicht |
| [`SETUP_CI_CD.md`](SETUP_CI_CD.md) | Detaillierte Anleitung |
| [`DEPLOYMENT_GUIDE.md`](DEPLOYMENT_GUIDE.md) | Render Deployment |
| [`LOCAL_TESTING.md`](LOCAL_TESTING.md) | Lokales Testen |
| [`CHECKLIST.md`](CHECKLIST.md) | Setup-Checkliste |

---

## 🔄 Pipeline Stages

### Stage 1: CI (Code Quality)
```
✓ flake8 Linting
✓ black Format Check
✓ isort Import Check
✓ pytest Unit Tests
```
**Trigger:** Jeder Push & Pull Request

### Stage 2: Build & Push
```
✓ Docker Image bauen
✓ DockerHub login
✓ Image pushen (with tags: latest, commit-sha)
```
**Trigger:** Push auf `main` (nur wenn CI ✓)

### Stage 3: Deploy
```
✓ Render Deploy Hook aufrufen
✓ Service redeployed automatisch
```
**Trigger:** Push auf `main` (nur wenn Build ✓)

---

## 🔐 Erforderliche Secrets (ohne Werte)

```
DOCKER_USERNAME            # DockerHub Account
DOCKER_PASSWORD            # DockerHub Access Token
RENDER_DEPLOY_HOOK_URL     # Render Deployment URL
RENDER_SERVICE_URL         # Render Public URL
```

**Mehr Infos:** [SETUP_CI_CD.md](SETUP_CI_CD.md#schritt-1-github-secrets-einrichten)

---

## 🌍 Live URL

Nach erfolgreichem Setup:
```
https://m324-app.onrender.com
```

(Wird nach first successful deploy verfügbar)

---

## 🧪 Lokal testen

```bash
# Setup
python3.11 -m venv venv
source venv/bin/activate
pip install -r task-6/requirements.txt

# Tests
pytest task-6/

# Code Quality
flake8 task-6/app.py
black --check task-6/app.py

# Docker
cd task-6
docker build -t m324-app:test .
docker run -p 5002:5002 m324-app:test
```

**Mehr:** [LOCAL_TESTING.md](LOCAL_TESTING.md)

---

## ✅ Anforderungen erfüllt

- ✅ Pipeline mit **2+ Stages** (CI, Build, Deploy)
- ✅ Deploy läuft **nur bei CI-Erfolg** (Job Dependencies)
- ✅ Deploy läuft **nur auf main** (Branch Condition)
- ✅ Docker Image **zu DockerHub** (mit Tags: latest, commit-sha)
- ✅ Deployment **automatisiert** (Deploy Hook, nicht manuell)
- ✅ **README.md** mit öffentlicher URL + Secrets Dokumentation

---

## 🛠️ Troubleshooting

| Problem | Lösung |
|---------|--------|
| GitHub Actions fehlgeschlagen | Logs überprüfen: GitHub → Actions → [Run] |
| DockerHub Push failed | Access Token überprüfen, nicht Passwort! |
| Render Deploy failed | Deploy Hook URL überprüfen (GitHub Secrets) |
| MySQL Connection Error | MYSQL_* Env-Variablen in Render überprüfen |
| Tests lokal fehlgeschlagen | `pip install -r task-6/requirements.txt` |

**Detailliert:** [SETUP_CI_CD.md#troubleshooting](SETUP_CI_CD.md#troubleshooting)

---

## 📚 Weitere Ressourcen

- **GitHub Actions Docs:** https://docs.github.com/en/actions
- **Render Docs:** https://render.com/docs
- **DockerHub:** https://docs.docker.com/docker-hub/
- **Flask:** https://flask.palletsprojects.com/

---

## 🎯 Nächste Schritte

1. Secrets in GitHub konfigurieren (MUSS ZUERST!)
2. Render Service erstellen
3. Code pushen → Pipeline startet automatisch
4. Logs monitoren
5. Live URL testen

→ Detaillierte Anleitung: [SETUP_CI_CD.md](SETUP_CI_CD.md)

---

**Status:** ✅ Implementiert & dokumentiert  
**Test-Status:** Lokal bereit zum Testen  
**Deployment:** Bereit nach Secret-Konfiguration
