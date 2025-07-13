from fastapi import FastAPI
from app.db import connect_to_db, disconnect_from_db, get_blacklist, get_whitelist
from app.discorddetect import fetch_discord_detectable

app = FastAPI()

@app.on_event("startup")
async def startup():
    await connect_to_db()

@app.on_event("shutdown")
async def shutdown():
    await disconnect_from_db()

@app.get("blacklist")
async def read_blacklist():
    return await get_blacklist()

@app.get("whitelist")
async def read_whitelist():
    return await get_whitelist()

@app.get("gamesdetect")
async def read_gamesdetect():
    return await fetch_discord_detectable()