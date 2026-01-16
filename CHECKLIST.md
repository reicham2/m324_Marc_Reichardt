# CI/CD Pipeline - Setup Checkliste

## Pre-Setup (Vorbereitung)

### GitHub
- [ ] Repository ist öffentlich (oder Private mit Actions enabled)
- [ ] Git auf neuesten Stand: `git pull origin main`
- [ ] Keine uncommitted Changes: `git status`

### DockerHub
- [ ] DockerHub Account erstellt: https://hub.docker.com
- [ ] Angemeldet bei `docker login`
- [ ] Repository `m324-app` erstellt (oder wird auto-created)

### Render
- [ ] Render Account erstellt: https://render.com
- [ ] Mit GitHub verknüpft (optional)

---

## Step 1: GitHub Secrets (MUSS ZUERST ERFOLGEN!)

### 1.1 Secrets hinzufügen

Gehe zu: **GitHub Repository → Settings → Secrets and variables → Actions → New repository secret**

| Secret Name | Beschreibung | Beispiel | Quelle |
|---|---|---|---|
| `DOCKER_USERNAME` | DockerHub Benutzername | `marcreichardt` | DockerHub Account |
| `DOCKER_PASSWORD` | DockerHub Access Token | `dckr_pat_xxxxx` | DockerHub Account → Settings → Security |
| `RENDER_DEPLOY_HOOK_URL` | Render Deploy URL | `https://api.render.com/deploy/srv-...` | (setzen nach Render Setup) |
| `RENDER_SERVICE_URL` | Service Public URL | `https://m324-app.onrender.com` | (setzen nach Render Deploy) |

### 1.2 Secrets überprüfen
```bash
# GitHub Secrets sollten diese Struktur haben:
Settings → Secrets → DOCKER_USERNAME, DOCKER_PASSWORD, etc.
```

- [ ] DOCKER_USERNAME hinzugefügt
- [ ] DOCKER_PASSWORD hinzugefügt (Token, nicht Passwort!)
- [ ] Alle Secrets sichtbar in Settings

---

## Step 2: Lokales Testen

### 2.1 Python Setup
```bash
cd /Users/marcreichardt/Projects/m324_Marc_Reichardt
python3.11 -m venv venv
source venv/bin/activate
pip install -r task-6/requirements.txt
```

- [ ] venv aktiviert
- [ ] Dependencies installiert
- [ ] `python -c "import flask; print(flask.__version__)"` funktioniert

### 2.2 Code Quality
```bash
# Im task-6 Directory
flake8 app.py
black --check app.py
isort --check-only app.py
```

- [ ] Flake8 ohne Fehler
- [ ] Black formatiert
- [ ] isort sortiert

### 2.3 Tests
```bash
pytest -v
```

- [ ] Alle Tests bestanden
- [ ] Test Output sichtbar

### 2.4 Docker Build
```bash
cd task-6
docker build -t m324-app:test .
```

- [ ] Docker Image gebaut
- [ ] Keine Build-Fehler
- [ ] Image visible: `docker images`

### 2.5 Docker Run
```bash
docker run -p 5002:5002 m324-app:test &
sleep 3
curl http://localhost:5002/
```

- [ ] Container startet ohne Fehler
- [ ] Port 5002 erreichbar
- [ ] HTTP Response OK (auch wenn MySQL Fehler)

---

## Step 3: DockerHub vorbereiten

### 3.1 Login & Test
```bash
docker login
```

- [ ] Login erfolgreich
- [ ] `~/.docker/config.json` existiert

### 3.2 Image pushen (Test)
```bash
docker tag m324-app:test marcreichardt/m324-app:test
docker push marcreichardt/m324-app:test
```

- [ ] Push erfolgreich
- [ ] Image visible auf DockerHub
- [ ] https://hub.docker.com/r/marcreichardt/m324-app

---

## Step 4: Render Service erstellen

### 4.1 Service erstellen
1. Render Dashboard → **New +** → **Web Service**
2. Wähle **Docker** Environment
3. Registry: **Docker Hub**
4. Image: `marcreichardt/m324-app:latest`
5. Port: `5002`
6. Plan: **Free**
7. **Create Web Service**

- [ ] Service erstellt
- [ ] Status: "Creating..." → "Live"
- [ ] Public URL sichtbar (z.B. `https://m324-app.onrender.com`)

### 4.2 Environment Variables setzen
Settings → Environment:
```
MYSQL_HOST=your_mysql_host
MYSQL_USER=demo
MYSQL_PASSWORD=demo
MYSQL_DATABASE=demo
PORT=5002
```

- [ ] Environment Variables gesetzt
- [ ] Service redeployed

### 4.3 Deploy Hook kopieren
Settings → Deploy Hook → Copy URL
```
https://api.render.com/deploy/srv-xxxxx
```

- [ ] Deploy Hook kopiert
- [ ] URL speichern (für GitHub Secret)

---

## Step 5: GitHub Secrets finalisieren

### 5.1 Fehlende Secrets hinzufügen

Gehe erneut zu **Settings → Secrets and variables → Actions**

| Secret | Wert | Status |
|--------|------|--------|
| `RENDER_DEPLOY_HOOK_URL` | `https://api.render.com/deploy/srv-...` | [ ] |
| `RENDER_SERVICE_URL` | `https://m324-app.onrender.com` | [ ] |

- [ ] RENDER_DEPLOY_HOOK_URL hinzugefügt
- [ ] RENDER_SERVICE_URL hinzugefügt

---

## Step 6: Code pushen & Pipeline starten

### 6.1 Lokale Commits
```bash
# Im Projekt-Root
git add .
git commit -m "feat: add CI/CD pipeline with GitHub Actions, DockerHub, and Render"
git push origin main
```

- [ ] Alle Änderungen committed
- [ ] Push erfolgreich
- [ ] Keine merge conflicts

### 6.2 GitHub Actions Monitor
1. GitHub Repository → **Actions**
2. Wähle **CI/CD Pipeline** Workflow
3. Beobachte die Execution

Workflow sollte folgende Stages zeigen:
```
✓ ci (Tests, Linting)
  ├─ Checkout
  ├─ Python Setup
  ├─ Linting
  ├─ Tests
  └─ Results

✓ build-and-push (Docker Build & Push)
  ├─ Docker Buildx Setup
  ├─ DockerHub Login
  ├─ Build
  └─ Push

✓ deploy (Render Deploy)
  ├─ Checkout
  ├─ Deploy Hook
  └─ Notification
```

- [ ] CI Stage: ✓ Passed
- [ ] Build Stage: ✓ Passed
- [ ] Deploy Stage: ✓ Passed
- [ ] Gesamtstatus: Success

### 6.3 Image auf DockerHub überprüfen
1. DockerHub → Repositories → m324-app
2. Tags überprüfen
   - `latest` sollte existieren
   - `<commit-sha>` sollte existieren

- [ ] Image auf DockerHub sichtbar
- [ ] Tags korrekt

### 6.4 Render Deployment überprüfen
1. Render Dashboard → m324-app
2. Status sollte **Live** sein
3. Logs überprüfen

```
Render Dashboard → m324-app → Logs
```

- [ ] Service Status: Live ✓
- [ ] Logs zeigen keine Errors
- [ ] Public URL funktioniert

### 6.5 Öffentliche URL testen
```bash
# Im Terminal
curl https://<your-render-service>.onrender.com

# Oder im Browser
https://<your-render-service>.onrender.com
```

- [ ] URL antwortet
- [ ] HTTP 200 oder 500 (OK, auch wenn App crasht)
- [ ] Service ist öffentlich erreichbar

---

## Step 7: Finalisierung & Dokumentation

### 7.1 README.md aktualisieren

Ersetze diese Platzhalter:
```markdown
# Öffentliche URL
https://m324-app.onrender.com

# GitHub Actions
https://github.com/YOUR-USERNAME/m324_Marc_Reichardt/actions

# DockerHub
https://hub.docker.com/r/YOUR-USERNAME/m324-app
```

- [ ] README.md URL aktualisiert

### 7.2 Secrets dokumentieren (OHNE Werte!)

Erstellung einer `SECRETS_TEMPLATE.md`:
```
DOCKER_USERNAME=...
DOCKER_PASSWORD=...
RENDER_DEPLOY_HOOK_URL=...
RENDER_SERVICE_URL=...
```

- [ ] Secrets dokumentiert (ohne echte Werte)
- [ ] In `.gitignore`: `SECRETS_*.md`

### 7.3 Test mit neuem Push
```bash
# Kleine Änderung machen
echo "# Updated $(date)" >> README.md

git add README.md
git commit -m "docs: update live URL"
git push origin main
```

- [ ] GitHub Actions startet automatisch
- [ ] Build erfolgreich
- [ ] Render redeployed automatisch

---

## Step 8: Monitoring & Maintenance

### Regelmäßige Überprüfungen

- [ ] **Wöchentlich:** GitHub Actions Logs checken
- [ ] **Monatlich:** Dependencies updaten (`pip list --outdated`)
- [ ] **Monatlich:** Docker Image Scan (DockerHub)
- [ ] **Quartal:** Render Plan überprüfen (Free vs. Paid)

### Optional: Alerts konfigurieren

```bash
# Email Notifications (GitHub Actions)
Settings → Actions → Notifications → Email on build failure

# Slack Integration (optional)
# GitHub Actions → Add Slack Workflow
```

---

## ✅ Fertig!

Herzlich Glückwunsch! Deine CI/CD Pipeline ist nun aktiv!

### Zusammenfassung

| Komponente | Status | URL/Info |
|---|---|---|
| GitHub Actions | ✓ Aktiv | `.github/workflows/ci-cd.yml` |
| DockerHub | ✓ Aktiv | `https://hub.docker.com/r/...` |
| Render | ✓ Aktiv | `https://...onrender.com` |
| Tests | ✓ Automatisch | Auf jedem Push |
| Linting | ✓ Automatisch | flake8, black, isort |
| Docker Build | ✓ Automatisch | main branch nur |
| Deployment | ✓ Automatisch | main branch nach Build |

### Nächste Schritte (Optional)

1. [ ] Code Coverage Reports hinzufügen
2. [ ] Slack Notifications
3. [ ] Custom Domain für Render
4. [ ] PostgreSQL statt MySQL
5. [ ] Monitoring Dashboard
6. [ ] Automated Backups

### Support

Falls Probleme auftreten:
- Siehe: [SETUP_CI_CD.md](SETUP_CI_CD.md)
- Siehe: [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- Siehe: [LOCAL_TESTING.md](LOCAL_TESTING.md)

---

**Erstellt:** $(date)
**Status:** ✓ Produktiv
