# --- Build frontend ---
FROM node:18-alpine as node_builder
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci --silent
COPY frontend/ .
RUN npm run build

# --- Build final image ---
FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends         build-essential libssl-dev libffi-dev libcurl4-openssl-dev libexpat1-dev pkg-config cmake git libgit2-dev nginx supervisor curl      && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend + wsgi + git app + supervisord + nginx conf
COPY backend/ ./backend
COPY git_http_wsgi.py ./
COPY supervisord.conf ./
COPY nginx.conf /etc/nginx/nginx.conf
COPY init_container.sh ./init_container.sh
RUN chmod +x ./init_container.sh

# Copy built frontend into backend static directory
COPY --from=node_builder /app/frontend/build /app/backend/frontend_build

ENV GIT_REPOS_ROOT=/data/git
RUN mkdir -p ${GIT_REPOS_ROOT} && mkdir -p /data/static && chown -R www-data:www-data /data || true
VOLUME ["/data"]

EXPOSE 80

# Entrypoint runs initialization then supervisord to manage services
CMD ["/bin/bash", "/app/init_container.sh"]
