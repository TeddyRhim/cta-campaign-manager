from fastapi import FastAPI
from sqlalchemy import text

from app.db.database import engine
from app.routers import auth, campaigns, contacts, imports
from fastapi.middleware.cors import CORSMiddleware


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

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
def root():

    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT version();")
        )

        version = result.fetchone()

    return {
              "database": version[0]
    }