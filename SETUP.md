# DOCKER Setup Instructions

# Running with Docker Compose

## Prerequisites

- Docker installed
- Docker Compose installed

To Build and start all services (Redis, Nginx, chatapp(Django App), Celery worker) and network:

    docker compose up --build

### This will
- Build the `chatapp` and `celery_worker` images from the current directory
- Start Redis using the official Alpine image
- Start Nginx, exposing port 80
- Run Django migrations, create users, collect static files, and start Daphne server inside `chatapp`
- Start Celery worker connected to Redis

You can visit `http://localhost/` to view app in browser



## Running the Application Manually

## Prerequisites

- Python 3.x installed (tested with 3.12)
- Redis server 

### 1. Install and Start Redis server
By default the app 
- On **Arch Linux**:
```
sudo pacman -S redis
sudo systemctl start redis
sudo systemctl enable redis # Optional
```

- On **Windows-WSL & Linux**
from:https://redis.io/docs/latest/operate/oss_and_stack/install/archive/install-redis/install-redis-on-windows/
```
sudo apt-get install redis-server
sudo service redis-server start
```

- Or Using Docker
```
docker run  --name redis -p 6379:6379 redis:alpine
```

### 2. Install Python dependencies
In Projects Main directory run 
```python -m pip install -r requirements.txt```

Or use `uv`
```
uv sync
OR
uv pip install -r requirements.txt
```

### 3. Run Django management commands
    python3 manage.py makemigrations
    python3 manage.py migrate
    python3 manage.py runscript create_superuser #creates super user z@z.com and paswd z
    python3 manage.py runscript create_randomusers #creates user a@a.com ... i@i.com with paswd a,b..i
    python3 manage.py collectstatic --noinput

### 4. Start Celery worker (in a separate terminal)
    celery -A chatserver worker --loglevel=info -E

### 5. Start the Django application with Daphne
    daphne -b 0.0.0.0 -p 8000 chatserver.asgi:application

- In `chatserver/settings.py` set `DEBUG = True` for daphne to server static files else use reverse proxy like nginx (setup below)

      daphne -b 0.0.0.0 -p 8000 chatserver.asgi:application
      OR
      python manage.py runserver # uses daphne
  
### 6. (Optional) for using nginx
    Install nginx
    create `/etc/nginx/sites-available/`
    create config file it should point to daphne running at `localhost:8000`

visit `http://localhost` on web browser
