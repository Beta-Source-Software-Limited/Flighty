# TicketTricket — Flight Booking MVP

Runnable **sandbox** booking project: React + TypeScript + Tailwind CSS, Django REST Framework, MySQL 8 and Django Admin.

## What works
- Responsive homepage, destination cards, flight search by IATA airport codes/date
- Flight inventory seeded into MySQL; live availability derived from DB
- Passenger lead contact, transactional booking creation, seat decrement
- Reservation reference and lookup by reference + email
- Django Admin for flights, bookings and payment-status records
- Basic Django test for booking and overselling

## What does NOT work yet
- **No real airline/GDS API, PNR, e-ticket, ticket issuance or fare repricing**
- **No live Stripe, SSLCommerz, bKash or other payment gateway integration**. Payment records are placeholders, and all reservations remain pending.
- No complete passenger manifest, account registration, refunds, cancellation/restocking, notifications, round trips, or production-grade authentication.
- Do **not** deploy publicly or accept money with this MVP. A booking holds a seat in the demo database indefinitely until further workflow is implemented.

## Quick start (Docker)
Install Docker Desktop (or compatible Docker Engine with Compose), then:

```bash
cp .env.example .env
# Edit .env: set unique passwords and DJANGO_SECRET_KEY
# Generate a secret with: python3 -c 'import secrets; print(secrets.token_urlsafe(64))'
docker compose up --build -d
docker compose ps
docker compose exec backend python manage.py seed_flights
docker compose exec backend python manage.py createsuperuser
```

Open:
- Frontend: http://localhost:5173
- API: http://localhost:8000/api/flights/
- Admin: http://localhost:8000/admin/
- Health: http://localhost:8000/api/health/

Choose a seeded route (`DAC` → `DXB`, `LHR`, `JFK`, `SIN`) and a date in the next 30 days. Seeded flights use UTC departure dates.

Run tests:
```bash
docker compose exec backend python manage.py test
```

Stop:
```bash
docker compose down
```
Do not add `-v` unless you intend to delete the database volume.

## Native setup (without Docker)
Create a MySQL 8 database and user with privileges, configure environment variables as in `.env.example` (with `MYSQL_HOST=127.0.0.1`). From `backend/`:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate --run-syncdb
python manage.py collectstatic --noinput
python manage.py seed_flights
python manage.py createsuperuser
python manage.py runserver
```

In another terminal from `frontend/`:
```bash
npm install
VITE_API_PROXY_TARGET=http://127.0.0.1:8000 npm run dev
```

## API
- `GET /api/health/`
- `GET /api/flights/?origin=DAC&destination=DXB&date=YYYY-MM-DD`
- `POST /api/bookings/` with `{ "flight": 1, "passenger_name": "Test User", "passenger_email": "test@example.com", "passenger_count": 1 }`
- `GET /api/bookings/REFERENCE/?email=test@example.com`

## Architecture / next milestones
1. Move to a migration-based release process (`makemigrations`, commit migrations); the initial MVP uses `migrate --run-syncdb` for convenience.
2. Add verified customer accounts and private booking access, full traveler/passport details, and secure CSRF/CORS design for production.
3. Add a flight-provider adapter, reprice/hold/issue workflows, idempotency keys and provider reconciliation.
4. Add Stripe Checkout and a locally supported gateway using **server-side verified webhooks**; never mark bookings paid from client responses.
5. Add seat hold expiry, cancellation/refund/restock logic, email delivery, rate limits, audit logging, backups, secrets management, HTTPS and observability.
6. CI, integration/e2e tests, load tests, threat modeling and operational runbooks before public launch.

**Important:** `DJANGO_DEBUG=1`, `--reload`, public backend port and seeded demo fares are development-only settings. Production deployment requires separate hardened settings and infrastructure.

## Fixes included in this regenerated version
- Vite API proxy uses `backend:8000` **inside Docker**, rather than `localhost:8000` (which incorrectly points back to the frontend container).
- Django Admin static assets are served by WhiteNoise. Backend startup automatically runs `collectstatic`.
- Frontend waits for Django health, and Django waits for MySQL health.
- To run the frontend natively instead of in Docker, set `VITE_API_PROXY_TARGET=http://127.0.0.1:8000`.

### Upgrade an existing installation without losing bookings
**Back up your MySQL database first.** Extract this archive to a new directory. If you want to reuse an existing MySQL Docker volume, do not run `docker compose down -v` and ensure the Compose project name and database credentials are consistent. For a fresh sandbox database:

```bash
cp .env.example .env
# Edit passwords and secret key
docker compose up --build -d
docker compose exec backend python manage.py seed_flights
docker compose exec backend python manage.py createsuperuser
```

If the API still errors, check `docker compose logs backend --tail=100` and `docker compose logs frontend --tail=100`.

### Quick verification
```bash
curl -i http://localhost:8000/api/health/
curl -i http://localhost:5173/api/health/
curl -I http://localhost:8000/static/admin/css/base.css
```
All three should return HTTP 200. Admin page: http://localhost:8000/admin/ .

**Development only:** this is a sandbox MVP, not a payment-enabled production booking system.
