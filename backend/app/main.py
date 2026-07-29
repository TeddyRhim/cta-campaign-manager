from fastapi import FastAPI
from sqlalchemy import text

from app.db.database import engine
from app.routers import auth, campaigns, contacts, imports



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