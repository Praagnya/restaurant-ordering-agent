from fastapi import FastAPI

from app.api.routes import chat, menu

app = FastAPI(title="Pragnya Bites Ordering API")

app.include_router(chat.router)
app.include_router(menu.router)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}
