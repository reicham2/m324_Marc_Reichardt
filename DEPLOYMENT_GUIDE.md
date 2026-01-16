# Render Deployment Guide

## Überblick

Dieser Guide erklärt wie du die CI/CD Pipeline auf Render.com zum Laufen bringst.

## Was ist Render?

Render ist ein modernes Cloud Platform:
- Kostenlos für kleine Projekte
- Automatische SSL/TLS
- Docker-native Support
- Deploy Hooks für CI/CD Integration

## Step-by-Step Setup

### 1. Render Account erstellen
- Gehe zu https://render.com
- Melde dich an (mit GitHub Account)
- Genehmige Permissions

### 2. Web Service erstellen

#### 2.1 New → Web Service
```
Click: Dashboard → New + → Web Service
```

#### 2.2 Git Repository verbinden (Optional - für Git Push Deploy)
```
Oder: DockerHub durchsuchen
```

#### 2.3 Konfiguration

**Optionen A: Docker Hub Registry (Recommended)**
```
Build: No (use pre-built Docker image)
Registry: Docker Hub
Image: your-docker-username/m324-app
Tag: latest
Port: 5002
```

**Optionen B: Git + Dockerfile**
```
Build: Yes
Repository: your-github-repo
Dockerfile Path: task-6/Dockerfile
Dockerfile Context: task-6
Port: 5002
```

#### 2.4 Environment Variables

Setzen Sie diese in Render:
```
MYSQL_HOST=your-mysql-host
MYSQL_USER=demo
MYSQL_PASSWORD=your-password
MYSQL_DATABASE=demo
FLASK_ENV=production
PORT=5002
```

Für externe MySQL-Database (z.B. Railway):
```
MYSQL_HOST=containers-us-west-123.railway.app
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=railway
```

#### 2.5 Resources
```
Plan: Free (0.05$ / day falls verwendet)
CPU: Shared
Memory: 512 MB (reicht für Demo)
```

### 3. Deploy Hook für CI/CD konfigurieren

#### 3.1 Deploy Hook kopieren
```
Service Dashboard → Settings → Deploy Hook
Copy: https://api.render.com/deploy/srv-xxxxx
```

#### 3.2 In GitHub Secret speichern
```
GitHub Repository → Settings → Secrets → New repository secret
Name: RENDER_DEPLOY_HOOK_URL
Value: https://api.render.com/deploy/srv-xxxxx
```

### 4. Externe Database (Optional)

Falls du externe MySQL brauchst:

#### Option A: Railway.app
```
1. Gehe zu https://railway.app
2. New Project → MySQL
3. Copy Connection String
4. In Render ENV variables einfügen
```

#### Option B: PlanetScale (kostenlos, MySQL compatible)
```
1. https://planetscale.com
2. Erstelle Database
3. Verbinde von Render
```

#### Option C: Render PostgreSQL
```
1. Render Dashboard → New PostgreSQL
2. Passe app.py für PostgreSQL an
3. Connection String kopieren
```

## Deployment Flow

### Automatisch (via GitHub Actions)
```
1. git push origin main
   ↓
2. GitHub Actions CI läuft (Tests, Linting)
   ↓
3. Docker Image zu DockerHub pushed (mit "latest" Tag)
   ↓
4. Deploy Hook ruft Render auf
   ↓
5. Render pullt neues Image von DockerHub
   ↓
6. Service wird neu gestartet
```

### Manuell (direkt auf Render)
```
Render Dashboard → m324-app → Manual Deploy
```

## URL & Domain

Nach dem Deploy erhältst du automatisch:
```
https://m324-app.onrender.com
```

(Der Subdomain-Name wird automatisch generiert)

### Custom Domain (optional)
```
Settings → Custom Domain
Beispiel: m324.example.com
```

## Logs anschauen

```
Dashboard → m324-app → Logs
```

Dort siehst du:
- Build Output
- Deployment Status
- Runtime Errors
- App Output

## Troubleshooting

### Service wird nicht deployed
1. Logs überprüfen
2. Image existiert in DockerHub?
3. Port 5002 korrekt konfiguriert?

### Connection zu MySQL schlägt fehl
1. MYSQL_HOST korrekt?
2. IP Whitelist in Database erlaubt Render?
3. Firewall offen?

### Service crasht nach Deploy
1. Docker Image lokal testen: `docker run -p 5002:5002 ...`
2. Environment Variablen überprüfen
3. Logs: Render Dashboard → Logs

### Performance ist langsam
- Free Plan hat CPU Limits
- Upgrade zu Starter Plan ($12/month)
- Nutze Redis für Caching

## Kosten

**Free Plan:**
- 750 Deployed Hours / Monat
- Reicht für kleine Projekte
- Wird nach 15 min Inaktivität pausiert

**Starter Plan:**
- $12 / Monat
- Kein Auto-Pause
- 3GB RAM

## Backup & Restore

Database-Backups (falls du Daten brauchst):
```
Railway/PlanetScale Admin → Backups
Oder: mysqldump über SSH
```

## Security

### Environment Variables
- ✅ Niemals in Code speichern
- ✅ Nur in Render Settings
- ✅ GitHub Secrets für CI/CD

### SSL/TLS
- ✅ Automatisch durch Render
- ✅ HTTPS immer aktiv
- ✅ Kostenlos

## Weitere Resources

- [Render Docs](https://render.com/docs)
- [Deploy Hooks](https://render.com/docs/deploy-hooks)
- [Environment Variables](https://render.com/docs/environment-variables)
- [Docker Support](https://render.com/docs/docker)
