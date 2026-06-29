# DealSense Backend

FastAPI backend for DealSense Phase 1: product database, store prices, price history, deal detection, mock collectors, and scheduled refresh jobs.

## Stack

- FastAPI
- PostgreSQL
- SQLAlchemy 2
- Alembic
- APScheduler
- Pydantic
- Docker Compose with PostgreSQL and Redis

## Local Setup

Windows:

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m alembic upgrade head
python scripts/seed.py
uvicorn app.main:app --reload
```

Optional `.env` setup:

```bash
copy .env.example .env
```

Update `.env` if your database connection differs:

```txt
DATABASE_URL=sqlite:///./dealsense.db
ENABLE_SCHEDULER=false
PRICE_REFRESH_HOURS=12
```

For PostgreSQL:

```txt
DATABASE_URL=postgresql+psycopg2://dealsense:dealsense@localhost:5432/dealsense
```

On Python 3.14+, use the psycopg v3 driver if connecting to PostgreSQL:

```txt
DATABASE_URL=postgresql+psycopg://dealsense:dealsense@localhost:5432/dealsense
```

One-command Windows helper:

```bat
start.bat
```

## Alembic Migrations

```bash
cd backend
python -m alembic upgrade head
```

Create a future migration:

```bash
python -m alembic revision --autogenerate -m "describe change"
```

## Seed Data

Seed products, stores, current prices, and initial price history from mock collectors:

```bash
cd backend
python scripts/seed.py
```

Seeded products:

- Lenovo LOQ
- ASUS TUF Gaming
- Acer Nitro V
- HP Victus
- Dell G15

Seeded stores:

- Amazon
- Flipkart
- Croma

## Run Server

```bash
cd backend
uvicorn app.main:app --reload
```

Open:

- API health: `http://localhost:8000/health`
- Swagger docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

```txt
GET /health
GET /products?page=1&limit=20
GET /products/{id}
GET /products/{id}/prices
GET /products/{id}/history?page=1&limit=100
GET /deals?page=1&limit=20
GET /search?q=lenovo&page=1&limit=20
```

## Scheduler

Set this in `.env`:

```txt
ENABLE_SCHEDULER=true
PRICE_REFRESH_HOURS=12
```

On API startup, APScheduler registers a 12-hour job that:

1. Runs Amazon, Flipkart, and Cuelinks mock collectors.
2. Creates missing products and stores.
3. Updates current prices.
4. Stores price history on price changes.
5. Recalculates deal scores when prices drop.

## Docker

```bash
cd backend
copy .env.example .env
docker compose up --build
```

The compose stack starts:

- FastAPI on `http://localhost:8000`
- PostgreSQL on `localhost:5432`
- Redis on `localhost:6379`

The API container runs migrations and seed data before starting Uvicorn.

## Phase 1 Status

- Products stored in PostgreSQL
- Multiple stores supported
- Current prices stored
- Price history tracked
- Deals automatically calculated on price drops
- Product and search APIs available
- Scheduler ready for recurring collection
- Mock collector architecture ready for real APIs
- Foundation ready for Phase 2 Shopping Assistant AI
