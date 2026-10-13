import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, campaigns, contacts, dashboard, imports

app = FastAPI(
    title="CTA Campaign Manager API",
    version="1.0.0"
)

app.include_router(
    auth.router
)

app.include_router(
    campaigns.router
)

app.include_router(
    contacts.router
)

app.include_router(
    imports.router
)

app.include_router(
    dashboard.router
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        origin.strip()
        for origin in os.getenv(
            "CORS_ORIGINS",
            "http://localhost:3000"
        ).split(",")
        if origin.strip()
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
def root():

    return {"status": "ok"}
