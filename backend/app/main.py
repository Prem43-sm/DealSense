import logging
import time
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.api import deals, prices, products
from app.automation import api as automation_api
from app.config import get_settings
from app.logging_config import configure_logging
from app.scheduler.jobs import create_scheduler

configure_logging()
logger = logging.getLogger(__name__)
settings = get_settings()
scheduler: BackgroundScheduler | None = None


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    global scheduler
    if settings.enable_scheduler:
        scheduler = create_scheduler()
        scheduler.start()
        logger.info("Scheduler started", extra={"_interval_hours": settings.price_refresh_hours})
    else:
        logger.info("Scheduler disabled")

    yield

    if scheduler and scheduler.running:
        scheduler.shutdown(wait=False)
        logger.info("Scheduler stopped")


app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description="DealSense Phase 1 product database and price tracking API.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    started_at = time.perf_counter()
    response = await call_next(request)
    duration_ms = round((time.perf_counter() - started_at) * 1000, 2)
    logger.info(
        "API request completed",
        extra={
            "_method": request.method,
            "_path": request.url.path,
            "_status_code": response.status_code,
            "_duration_ms": duration_ms,
        },
    )
    return response


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(products.router)
app.include_router(prices.router)
app.include_router(deals.router)
app.include_router(automation_api.router)
