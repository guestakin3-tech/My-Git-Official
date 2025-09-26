# MyGit - Full Ready-to-Deploy Starter (with nginx proxy & sample data)

This package includes:
- Django + DRF backend (apps/gitserver)
- pygit2 + dulwich Git HTTP endpoint under `/git/`
- React frontend (simple) built and served as static files via nginx/whitenoise
- nginx reverse-proxy serving `/` and proxying `/git/` to the internal git HTTP server
- supervisord to run nginx, gunicorn (Django), and the git HTTP server
- Dockerfile (multi-stage) that builds frontend and produces a container ready for Render
- `init_container.sh` script that runs migrations and creates a sample superuser and repository on first boot

## Quick deploy to Render
1. Push this repo to GitHub.
2. Create a Web Service on Render using the repo. Use **Docker** environment.
3. Attach a **Persistent Disk** at `/data` (size >= 2GB suggested).
4. Create a managed Postgres DB on Render and copy credentials into Render env vars.
5. Set these environment variables in Render:
   - DJANGO_SECRET_KEY (random secret)
   - DEBUG=False
   - DB_NAME, DB_USER, DB_PASS, DB_HOST, DB_PORT
   - GIT_REPOS_ROOT=/data/git
6. Deploy. The container will run `init_container.sh` on startup to run migrations and create a sample user/repo.
7. Access:
   - App & frontend: https://<your-app>.onrender.com/
   - Admin: https://<your-app>.onrender.com/admin/
   - Git smart HTTP: https://<your-app>.onrender.com/git/<owner>/<repo>.git

## Notes
- This is an educational MVP; for production at scale consider using Gitea or similar.
- `pygit2` requires libgit2; Dockerfile installs it.
- Ensure the persistent disk `/data` is configured so repos survive restarts.
