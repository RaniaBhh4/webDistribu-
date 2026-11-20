
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from py_eureka_client import eureka_client

from app.routers import notification

# Port read from an environment variable so several instances can run (8084, 8094, ...)
PORT = int(os.getenv("PORT", "8084"))
EUREKA_SERVER = os.getenv("EUREKA_SERVER", "http://localhost:8761/eureka")
EUREKA_ENABLED = os.getenv("EUREKA_ENABLED", "true").lower() == "true"
INSTANCE_HOST = os.getenv("INSTANCE_HOST", "127.0.0.1")


@asynccontextmanager
async def lifespan(_: FastAPI):
    # ---- Startup: register in Eureka as NOTIFICATION ----
    if EUREKA_ENABLED:
        await eureka_client.init_async(
            eureka_server=EUREKA_SERVER,
            app_name="NOTIFICATION",
            instance_id=f"{INSTANCE_HOST}:notification:{PORT}",
            instance_host=INSTANCE_HOST,
            instance_ip=INSTANCE_HOST,
            instance_port=PORT,
            status_page_url=f"http://{INSTANCE_HOST}:{PORT}/info",
            health_check_url=f"http://{INSTANCE_HOST}:{PORT}/health",
        )
    yield
    # ---- Shutdown: unregister from Eureka ----
    if EUREKA_ENABLED:
        await eureka_client.stop_async()


app = FastAPI(
    title="Notification Microservice API",
    version="1.0.0",
    description=(
        "Notification microservice (Python / FastAPI, no database). "
        "Only the hello endpoint is implemented; the notification logic is to be developed by students."
    ),
    contact={"name": "Badia Abouhdid"},
    servers=[{"url": f"http://localhost:{PORT}", "description": "Local"}],
    # Same URLs as the other microservices of the project
    docs_url="/swagger-ui",       # Swagger UI
    openapi_url="/v3/api-docs",   # OpenAPI JSON
    redoc_url="/redoc",           # alternative documentation
    lifespan=lifespan,
)

app.include_router(notification.router)


# ---- Health & info (observabilite, declares dans Eureka) ----
@app.get("/health", tags=["Observabilite"], summary="Etat de sante du service")
def health() -> dict:
    return {"status": "UP"}


@app.get("/info", tags=["Observabilite"], summary="Informations sur le service")
def info() -> dict:
    return {"app": {"name": "notification", "version": app.version, "description": "Notification microservice (Python / FastAPI)"}}

# TODO (students): if you add other routers, include them here.


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=PORT)
