## Web App (Flask + MySQL) – CI/CD & Deployment

Öffentliche URL Render: `https://<dein-render-service>.onrender.com` (bitte ersetzen, sobald Render live ist)
Öffentliche URL Vercel: `https://<dein-vercel-project>.vercel.app` (bitte ersetzen, sobald live)

### CI/CD Pipeline (GitHub Actions)
- Trigger: Push/Merge auf `main` oder Tags `v*`; PRs gegen `main` laufen nur CI.
- Jobs: `ci` (Flake8, Black-Check, Pytest) → `build-and-push` (Docker Buildx, Push zu DockerHub) → Deploy (Render-Deploy-Hook) und Deploy (Vercel via CLI).
- Deploys laufen nur, wenn `ci` erfolgreich war und nur auf `main`/`v*`.
- Image-Tags: Branch/Tag-basiert, Semver, SHA, und immer `latest`.

### Benötigte Secrets/Env Variablen
- GitHub Secrets: `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`, `RENDER_DEPLOY_HOOK`, `VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID`.
- App/Deploy-Umgebung (Render/Vercel): `MYSQL_HOST`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DATABASE`, optional `FLASK_ENV=production`.

### Lokale Entwicklung
```bash
cd task-6
pip install -r requirements.txt
pip install flake8 black pytest
flake8 app.py
black --check app.py
pytest
```
App starten:
```bash
flask --app app run --host 0.0.0.0 --port 5002
```
Letzte Aktualisierung: Fri Jan 16 11:46:06 UTC 2026
