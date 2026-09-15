# Real Estate Lead Bot --- Deployment Specification

**Document:** `DEPLOYMENT_SPEC.md`\
**Project:** Real Estate Lead Bot\
**Deployment Target:** Existing VPS\
**Architecture Level:** MVP / Beginner → Intermediate\
**Status:** Initial Specification\
**Primary Stack:** React, FastAPI, PostgreSQL, n8n, Docker, Docker
Compose, Nginx\
**Deployment Model:** Single VPS

------------------------------------------------------------------------

# 1. Purpose

This document defines how the Real Estate Lead Bot should be deployed,
operated, updated, backed up, monitored, and recovered on an existing
Virtual Private Server (VPS).

The VPS is assumed to already exist and be accessible. VPS provisioning
and general Ubuntu/server administration are outside the scope of this
project.

The MVP deployment uses:

-   Docker
-   Docker Compose
-   Nginx
-   React frontend
-   FastAPI backend
-   PostgreSQL database
-   n8n
-   HTTPS
-   Persistent Docker volumes

The goal is to create a deployment that is easy to understand,
reproduce, troubleshoot, back up, update, and roll back.

The project will not use Kubernetes, service meshes, microservices, or
other unnecessary infrastructure at the MVP stage.

------------------------------------------------------------------------

# 2. Deployment Goals

The deployment must allow:

1.  Customers to access the React application through HTTPS.
2.  The frontend to communicate securely with FastAPI.
3.  FastAPI to communicate with PostgreSQL and n8n.
4.  n8n to execute lead-processing workflows.
5.  PostgreSQL data to survive container restarts.
6.  n8n workflows and credentials to survive container restarts.
7.  Nginx to route incoming requests.
8.  Application logs to be inspected.
9.  Database backups to be created and restored.
10. New versions to be deployed with predictable commands.
11. Previous versions to be restored if a deployment fails.

------------------------------------------------------------------------

# 3. MVP Deployment Architecture

``` text
Internet
   |
   v
Domain / DNS
   |
   v
HTTPS
   |
   v
Nginx
   |
   +------------------+
   |                  |
   v                  v
React Frontend    FastAPI Backend
                       |
                       v
                      n8n
                 +-----+------+
                 |            |
                 v            v
                AI        PostgreSQL
                 |
                 v
          Lead Qualification
                 |
                 v
          Sales Notification
                 |
                 v
          Customer Response
```

All major services run on the same existing VPS during the MVP phase.

------------------------------------------------------------------------

# 4. Recommended Project Directory

``` text
/opt/real-estate-lead-bot/
├── docker-compose.yml
├── .env
├── frontend/
│   ├── Dockerfile
│   └── ...
├── backend/
│   ├── Dockerfile
│   └── ...
├── nginx/
│   └── default.conf
├── n8n/
│   └── workflows/
├── scripts/
│   ├── deploy.sh
│   ├── backup-db.sh
│   └── restore-db.sh
└── backups/
```

Application source should be managed through Git.

------------------------------------------------------------------------

# 5. Docker Services

The production Docker Compose stack should contain:

``` text
frontend
backend
postgres
n8n
nginx
```

### frontend

Hosts the production React application.

### backend

Runs the FastAPI application.

### postgres

Stores application data.

### n8n

Runs lead processing, AI, routing, notifications, and integrations.

### nginx

Acts as the public reverse proxy and HTTPS entry point.

------------------------------------------------------------------------

# 6. Docker Compose

Conceptual production configuration:

``` yaml
services:
  frontend:
    build:
      context: ./frontend
    restart: unless-stopped
    networks:
      - app_network

  backend:
    build:
      context: ./backend
    restart: unless-stopped
    env_file:
      - .env
    depends_on:
      - postgres
    networks:
      - app_network

  postgres:
    image: postgres:16
    restart: unless-stopped
    env_file:
      - .env
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - app_network

  n8n:
    image: n8nio/n8n
    restart: unless-stopped
    env_file:
      - .env
    volumes:
      - n8n_data:/home/node/.n8n
    networks:
      - app_network

  nginx:
    image: nginx:alpine
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/default.conf:/etc/nginx/conf.d/default.conf:ro
    depends_on:
      - frontend
      - backend
    networks:
      - app_network

volumes:
  postgres_data:
  n8n_data:

networks:
  app_network:
    driver: bridge
```

The final configuration must match the actual application
implementation.

------------------------------------------------------------------------

# 7. Domains and DNS

Example domain structure:

``` text
example.com
api.example.com
automation.example.com
```

Suggested responsibilities:

  Domain                     Service
  -------------------------- ----------------
  `example.com`              React frontend
  `api.example.com`          FastAPI
  `automation.example.com`   n8n

Example DNS records:

``` text
A    @             VPS_PUBLIC_IP
A    api           VPS_PUBLIC_IP
A    automation    VPS_PUBLIC_IP
```

Verify DNS before configuring HTTPS.

------------------------------------------------------------------------

# 8. Nginx Reverse Proxy

Nginx should:

-   Accept HTTP/HTTPS traffic
-   Route frontend requests
-   Route API requests
-   Route approved n8n traffic
-   Terminate TLS
-   Forward appropriate proxy headers

Conceptually:

``` text
example.com            -> frontend
api.example.com        -> backend:8000
automation.example.com -> n8n
```

Example API proxy:

``` nginx
server {
    listen 80;
    server_name api.example.com;

    location / {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Production configuration should redirect HTTP to HTTPS.

------------------------------------------------------------------------

# 9. HTTPS

All public production traffic must use HTTPS.

Required endpoints should include:

``` text
https://example.com
https://api.example.com
https://automation.example.com
```

Use a trusted TLS certificate provider such as Let's Encrypt.

Certificate renewal should be automated and periodically verified.

------------------------------------------------------------------------

# 10. Environment Variables

Production secrets and environment-specific values must not be
hardcoded.

Use a production `.env`.

Example:

``` env
APP_ENV=production

POSTGRES_DB=realestate
POSTGRES_USER=realestate_user
POSTGRES_PASSWORD=CHANGE_ME

DATABASE_URL=postgresql://realestate_user:CHANGE_ME@postgres:5432/realestate

N8N_HOST=automation.example.com
N8N_PROTOCOL=https
WEBHOOK_URL=https://automation.example.com/

N8N_ENCRYPTION_KEY=CHANGE_ME

AI_API_KEY=CHANGE_ME
SECRET_KEY=CHANGE_ME

FRONTEND_URL=https://example.com
API_URL=https://api.example.com
```

The exact variables must match the implementation.

------------------------------------------------------------------------

# 11. Secrets

Secrets include:

-   Database passwords
-   AI API keys
-   Authentication secrets
-   n8n encryption key
-   Email credentials
-   Notification credentials
-   Third-party API keys

Secrets must never be committed to Git, embedded in frontend bundles,
written directly into source files, published in documentation, or
printed unnecessarily in logs.

`.gitignore` should include:

``` gitignore
.env
.env.*
backups/
```

Use `.env.example` to document variable names without real secret
values.

------------------------------------------------------------------------

# 12. Persistent Storage

Containers are replaceable. Important application state must survive
container replacement and restart.

Persist at minimum:

``` text
PostgreSQL database
n8n configuration/workflows
```

Use named volumes:

``` text
postgres_data
n8n_data
```

Do not routinely run:

``` bash
docker compose down -v
```

in production because it removes named volumes.

------------------------------------------------------------------------

# 13. PostgreSQL

PostgreSQL should operate as a private Docker service.

Internal hostname:

``` text
postgres:5432
```

Example connection:

``` text
postgresql://user:password@postgres:5432/realestate
```

The application should not depend on `localhost` to reach the PostgreSQL
container.

------------------------------------------------------------------------

# 14. Database Migrations

Database schema changes must be managed through migrations.

For the FastAPI/Python implementation, Alembic is recommended.

Typical sequence:

``` bash
docker compose build
docker compose up -d postgres
docker compose run --rm backend alembic upgrade head
docker compose up -d
```

Before significant migrations:

1.  Back up the database.
2.  Review the migration.
3.  Apply the migration.
4.  Verify migration status.
5.  Test the application.

Example status command:

``` bash
docker compose exec backend alembic current
```

------------------------------------------------------------------------

# 15. Database Backups

Use PostgreSQL `pg_dump` for the MVP.

Example:

``` bash
docker compose exec -T postgres \
pg_dump -U realestate_user realestate \
> backups/realestate_$(date +%Y%m%d_%H%M%S).sql
```

Recommended initial schedule:

``` text
Database backup: Daily
Retention: At least 7 daily backups
```

At least one backup copy should eventually exist outside the VPS.

Backups should periodically be restored into a non-production database
to verify they are usable.

------------------------------------------------------------------------

# 16. n8n Persistence and Production Configuration

Persist n8n data:

``` yaml
volumes:
  - n8n_data:/home/node/.n8n
```

Keep a stable production `N8N_ENCRYPTION_KEY`.

Production configuration should include:

``` text
N8N_HOST
N8N_PROTOCOL
WEBHOOK_URL
N8N_ENCRYPTION_KEY
```

Production workflows must use production webhook URLs rather than test
webhook URLs.

Workflow exports should be stored under:

``` text
n8n/workflows/
```

Do not commit credentials inside workflow exports.

------------------------------------------------------------------------

# 17. Restart Policy

Production services should normally use:

``` yaml
restart: unless-stopped
```

for:

``` text
frontend
backend
postgres
n8n
nginx
```

This allows containers to recover after ordinary application or VPS
restarts.

------------------------------------------------------------------------

# 18. Health Checks

FastAPI should provide:

``` http
GET /health
```

Example:

``` json
{
  "status": "ok"
}
```

A readiness check may additionally verify database connectivity without
exposing secrets or unnecessary infrastructure details.

Where practical, Docker health checks should also be configured.

------------------------------------------------------------------------

# 19. Logging

For the MVP, Docker logs are sufficient.

``` bash
docker compose logs
docker compose logs -f
docker compose logs -f backend
docker compose logs -f n8n
docker compose logs -f postgres
docker compose logs -f nginx
```

Backend logs should record useful operational events such as lead
creation, workflow calls, qualification, and failures.

Never expose passwords, API keys, access tokens, or unnecessary customer
data in logs.

Configure log size limits where appropriate:

``` yaml
logging:
  driver: json-file
  options:
    max-size: "10m"
    max-file: "3"
```

------------------------------------------------------------------------

# 20. Monitoring

Keep MVP monitoring simple.

Monitor:

-   Application availability
-   Docker container status
-   FastAPI health endpoint
-   PostgreSQL availability
-   n8n availability
-   Disk usage
-   CPU/RAM usage
-   HTTPS certificate validity

Useful commands:

``` bash
docker compose ps
docker stats
df -h
free -h
```

An external uptime monitor may later check the frontend and API health
endpoint.

------------------------------------------------------------------------

# 21. Initial Application Deployment

Assuming the VPS already exists and is accessible:

``` bash
cd /opt
git clone <repository-url> real-estate-lead-bot
cd real-estate-lead-bot
```

Prepare environment:

``` bash
cp .env.example .env
```

Configure production values in `.env`.

Build:

``` bash
docker compose build
```

Start:

``` bash
docker compose up -d
```

Check:

``` bash
docker compose ps
docker compose logs --tail=100
```

Run required migrations and verify the API health endpoint.

------------------------------------------------------------------------

# 22. Standard Deployment Procedure

For normal updates:

``` bash
cd /opt/real-estate-lead-bot

git status
git fetch --all --tags
git pull

./scripts/backup-db.sh

docker compose build

docker compose run --rm backend alembic upgrade head

docker compose up -d

docker compose ps
docker compose logs --tail=100
```

Then test:

``` bash
curl https://api.example.com/health
```

Finally perform an end-to-end synthetic lead test.

------------------------------------------------------------------------

# 23. Deployment Validation

After deployment verify:

-   Frontend loads
-   HTTPS works
-   API responds
-   Database connects
-   n8n is running
-   Production webhook works
-   Lead can be submitted
-   AI processing works
-   Lead qualification works
-   Lead is stored
-   Sales notification works
-   Customer receives expected response

Deployment is not successful merely because containers are running.

------------------------------------------------------------------------

# 24. Rollback

Every production release should be identifiable by a Git commit or tag.

Before deployment:

``` bash
git rev-parse HEAD
```

If a deployment fails:

``` bash
git checkout <previous-tag-or-commit>
docker compose build
docker compose up -d
docker compose ps
```

Then run smoke tests.

Application rollback and database rollback are different operations.
Reverting Git does not automatically reverse a database migration.

Before risky migrations, create a verified database backup.

------------------------------------------------------------------------

# 25. Update Strategy

Use small, controlled releases:

``` text
Develop
↓
Test locally
↓
Commit
↓
Push
↓
Review
↓
Backup production
↓
Deploy
↓
Run migrations
↓
Smoke test
↓
Run E2E test
↓
Monitor
```

Avoid making untracked source-code changes directly on the production
VPS.

------------------------------------------------------------------------

# 26. Application Security

Application-level deployment requirements include:

-   HTTPS
-   Secrets outside Git
-   Strong database credentials
-   Stable n8n encryption key
-   Production credentials separate from development
-   Input validation in FastAPI
-   Authentication on administrative interfaces
-   Restricted CORS
-   Limited public endpoints
-   Secure API/webhook authentication where required
-   Database backups
-   Least-privilege application access

Lead records may contain names, email addresses, phone numbers, property
preferences, locations, budgets, and conversation content. Use synthetic
data for testing.

------------------------------------------------------------------------

# 27. Failure Scenarios

### Backend unavailable

``` bash
docker compose ps backend
docker compose logs backend
docker compose restart backend
```

### n8n unavailable

``` bash
docker compose logs n8n
docker compose restart n8n
```

### PostgreSQL unavailable

``` bash
docker compose logs postgres
```

Check persistent storage and disk space before making destructive
changes.

### Nginx failure

``` bash
docker compose exec nginx nginx -t
docker compose restart nginx
```

### VPS/application restart

After restart:

``` bash
docker compose ps
```

Confirm all required services recovered.

------------------------------------------------------------------------

# 28. Scaling

Do not introduce Kubernetes for MVP scaling.

Scale vertically first if the VPS becomes resource constrained.

If the project grows significantly, components can later be separated,
for example:

``` text
VPS 1: Frontend + Nginx
VPS 2: FastAPI + n8n
Managed PostgreSQL
```

Possible future additions include a CDN, managed database, Redis,
background workers, centralized logging, or advanced monitoring.

These are not MVP requirements.

------------------------------------------------------------------------

# 29. Production Smoke Test

### Frontend

Open:

``` text
https://example.com
```

Expected: application loads without errors.

### API

Call:

``` text
GET https://api.example.com/health
```

Expected:

``` json
{
  "status": "ok"
}
```

### Database

Submit a synthetic lead and confirm it is stored.

### n8n

Confirm the production workflow receives and processes the request.

### End-to-End Lead

Example synthetic enquiry:

``` text
Name: Amina Yusuf
Phone: 08000000000
Email: amina@example.com

I am looking for a 3-bedroom apartment around Lekki.
My budget is about ₦80 million and I want to buy
within the next two months.
```

Expected structured information includes:

``` text
property_type = apartment
bedrooms = 3
location = Lekki
budget = 80000000
intent = buy
timeline = 2 months
```

Verify qualification, database storage, sales notification, and customer
response.

------------------------------------------------------------------------

# 30. Deployment Checklist

## Production Configuration

-   [ ] Production `.env` prepared
-   [ ] Secrets excluded from Git
-   [ ] Frontend Dockerfile verified
-   [ ] Backend Dockerfile verified
-   [ ] Production `docker-compose.yml` verified

## PostgreSQL

-   [ ] PostgreSQL container running
-   [ ] Persistent volume configured
-   [ ] Database connection works
-   [ ] Production migrations successful
-   [ ] Backup creation works
-   [ ] Restore procedure verified

## n8n

-   [ ] n8n container running
-   [ ] Persistent storage configured
-   [ ] Stable encryption key configured
-   [ ] Production webhook configured
-   [ ] Required workflow imported
-   [ ] Workflow activated
-   [ ] Workflow tested

## Backend

-   [ ] FastAPI container running
-   [ ] `/health` works
-   [ ] FastAPI connects to PostgreSQL
-   [ ] FastAPI connects to n8n
-   [ ] Error handling works

## Frontend

-   [ ] React frontend deployed
-   [ ] Production API URL configured
-   [ ] React communicates with FastAPI
-   [ ] Loading/success/error states work

## Nginx / Domain

-   [ ] Nginx routing configured
-   [ ] Frontend domain works
-   [ ] API domain works
-   [ ] n8n/webhook domain works
-   [ ] HTTPS works
-   [ ] HTTP redirects to HTTPS

## Operations

-   [ ] PostgreSQL persists after restart
-   [ ] n8n persists after restart
-   [ ] Logs are accessible
-   [ ] Log growth is controlled
-   [ ] Basic monitoring works
-   [ ] Rollback procedure verified

## Production Testing

-   [ ] Frontend smoke test passed
-   [ ] API health test passed
-   [ ] Synthetic lead submitted
-   [ ] AI extraction verified
-   [ ] Lead qualification verified
-   [ ] Database record verified
-   [ ] Sales notification verified
-   [ ] Customer response verified
-   [ ] Full production E2E test passed

------------------------------------------------------------------------

# 31. Definition of Done

Deployment is considered **DONE** only when:

-   React is running on the VPS.
-   FastAPI is running on the VPS.
-   PostgreSQL is running with persistent storage.
-   Database migrations have succeeded.
-   n8n is running with persistent storage.
-   Production n8n workflow is active.
-   Nginx routes traffic correctly.
-   Production domains resolve correctly.
-   HTTPS works.
-   React communicates with FastAPI.
-   FastAPI communicates with n8n.
-   AI extraction works.
-   Lead qualification works.
-   Lead data is stored in PostgreSQL.
-   Sales notification works.
-   Customer response works.
-   Database backup works.
-   Application logs are accessible.
-   Rollback procedure is verified.
-   Full production E2E test passes.
-   `TASK.md` is updated.
-   `IMPLEMENTATION.md` is updated.

Final production path:

``` text
Customer
↓
Domain + HTTPS
↓
Nginx
↓
React
↓
FastAPI
↓
n8n
↓
AI Extraction
↓
Lead Qualification
↓
PostgreSQL
↓
Sales Notification
↓
Customer Response
```

------------------------------------------------------------------------

# 32. MVP Deployment Principle

Keep the deployment simple:

``` text
EXISTING VPS
+
DOCKER COMPOSE
+
NGINX
+
REACT
+
FASTAPI
+
POSTGRESQL
+
n8n
+
HTTPS
+
PERSISTENT STORAGE
+
BACKUPS
+
BASIC MONITORING
```

The objective is not to build complicated infrastructure.

The objective is to deploy a Real Estate Lead Bot that is reliable,
recoverable, understandable, maintainable, and easy to improve.
