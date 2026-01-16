# Pipeline lokales Testen

Diese Anleitung zeigt wie du die CI/CD Pipeline lokal testen kannst.

## 1. Python Environment vorbereiten

```bash
# In den Projekt-Root-Verzeichnis navigieren
cd /Users/marcreichardt/Projects/m324_Marc_Reichardt

# Virtual Environment erstellen
python3.11 -m venv venv

# Aktivieren
source venv/bin/activate

# Dependencies installieren
pip install -r task-6/requirements.txt
```

## 2. Code Quality Tools testen

### Linting mit flake8
```bash
cd task-6

# Komplette Überprüfung
flake8 app.py

# Mit Ausgabe
flake8 app.py --show-source

# Nur bestimmte Fehler
flake8 app.py --select=E,W
```

### Formatting mit black
```bash
# Überprüfen (ohne Änderungen)
black --check app.py

# Tatsächlich formatieren
black app.py

# Zeige Unterschiede
black --diff app.py
```

### Import-Sortierung mit isort
```bash
# Überprüfen
isort --check-only app.py

# Tatsächlich sortieren
isort app.py

# Zeige Unterschiede
isort --diff app.py
```

## 3. Tests ausführen

### Pytest lokal
```bash
# Alle Tests ausführen
pytest

# Mit Verbosity
pytest -v

# Mit Coverage
pip install coverage
pytest --cov=.

# Nur bestimmte Tests
pytest test_app.py::test_app_exists
```

## 4. Docker lokal bauen & testen

### Bauen
```bash
cd task-6

# Image bauen
docker build -t m324-app:test .

# Mit Build-Arguments
docker build -t m324-app:test --build-arg VERSION=1.0 .
```

### Lokal laufen
```bash
# Einfach
docker run -p 5002:5002 m324-app:test

# Mit Environment Variables
docker run -p 5002:5002 \
  -e MYSQL_HOST=localhost \
  -e MYSQL_USER=demo \
  -e MYSQL_PASSWORD=demo \
  -e MYSQL_DATABASE=demo \
  m324-app:test

# Im Hintergrund
docker run -d -p 5002:5002 --name m324-app-test m324-app:test

# Logs anschauen
docker logs m324-app-test

# Container stoppen
docker stop m324-app-test
```

### Mit docker-compose
```bash
# Im task-6 Directory
docker-compose up --build

# Mit Datenbank
docker-compose up --build -d

# Logs anschauen
docker-compose logs -f

# Stoppen
docker-compose down
```

## 5. GitHub Actions lokal simulieren

### Act installieren
```bash
# macOS
brew install act

# oder Download von https://github.com/nektos/act
```

### Workflow lokal ausführen
```bash
# Alle Jobs
act

# Nur spezifischen Job
act -j ci

# Mit Debug
act -v

# Mit Secret
act --secret DOCKER_USERNAME=user --secret DOCKER_PASSWORD=token
```

## 6. Docker Image pushen

### Zu DockerHub
```bash
# Login
docker login

# Tag
docker tag m324-app:test dein-username/m324-app:latest

# Push
docker push dein-username/m324-app:latest

# Überprüfen auf DockerHub
# https://hub.docker.com/r/dein-username/m324-app
```

## 7. Kompletter Test-Workflow

```bash
#!/bin/bash

echo "=== 1. Code Quality Checks ==="
flake8 task-6/app.py
black --check task-6/app.py
isort --check-only task-6/app.py

echo "=== 2. Unit Tests ==="
pytest task-6/ -v

echo "=== 3. Docker Build ==="
docker build -t m324-app:test task-6/

echo "=== 4. Docker Run Test ==="
docker run -d -p 5002:5002 --name m324-app-test m324-app:test
sleep 3
curl http://localhost:5002/
docker stop m324-app-test
docker rm m324-app-test

echo "=== All tests passed! ==="
```

Speichern als `test-all.sh` und ausführen:
```bash
chmod +x test-all.sh
./test-all.sh
```

## Häufige Fehler

### "ModuleNotFoundError: No module named 'flask'"
```bash
# Sicherstellen dass venv aktiviert ist
source venv/bin/activate
pip install -r task-6/requirements.txt
```

### "flake8: command not found"
```bash
pip install flake8
```

### "Docker daemon not running"
```bash
# Docker Desktop starten oder
# In Linux: sudo systemctl start docker
```

### "Port 5002 already in use"
```bash
# Anderen Process auf Port beenden
lsof -i :5002
kill -9 <PID>

# Oder anderen Port verwenden
docker run -p 8080:5002 m324-app:test
```

## Best Practices

1. **Immer venv aktivieren**
   ```bash
   source venv/bin/activate
   ```

2. **Regelmäßig Dependencies updaten**
   ```bash
   pip install --upgrade -r task-6/requirements.txt
   ```

3. **Docker Cache nutzen**
   ```bash
   # Erste Builds sind langsam
   # Danach wird Cache genutzt
   docker build -t m324-app:test task-6/
   ```

4. **Tests vor Push**
   ```bash
   ./test-all.sh
   git push origin main  # Nur wenn Tests grün
   ```

5. **Logs überprüfen**
   ```bash
   # Docker Logs
   docker logs m324-app-test
   
   # GitHub Actions Logs
   # Repository → Actions → [Run]
   ```
