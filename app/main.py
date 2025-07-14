from fastapi import FastAPI, HTTPException, Depends
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional, List, Dict
from enum import Enum
from pydantic import BaseModel

from app.db import connect_to_db, disconnect_from_db, get_blacklist, get_whitelist, apply_whitelist, apply_blacklist
from app.discorddetect import fetch_discord_detectable
from app.auth import get_current_user, AdminUser
from app.telegram_bot import send_moderation_request, start_bot, stop_bot

app = FastAPI()

# =================== Startup & Shutdown ===================

@app.on_event("startup")
async def startup():
    await connect_to_db()
    await start_bot()

@app.on_event("shutdown")
async def shutdown():
    await disconnect_from_db()
    await stop_bot()

# =================== Public Routes ===================

@app.get("/blacklist")
async def read_blacklist():
    return await get_blacklist()

@app.get("/whitelist")
async def read_whitelist():
    return await get_whitelist()

@app.get("/gamesdetect")
async def read_gamesdetect():
    return await fetch_discord_detectable()

# =================== Moderation System ===================

class RequestType(str, Enum):
    whitelist = "whitelist"
    blacklist = "blacklist"

class WhitelistEntry(BaseModel):
    gameName: str
    savePath: str
    modPath: Optional[str] = None
    addPath: Optional[str] = None
    specialBackupMark: int = 0

class BlacklistEntry(BaseModel):
    gameName: str

class ModerationRequest(BaseModel):
    id: UUID
    type: RequestType
    submitted_at: datetime
    data: dict
    approved: Optional[bool] = None

pending_requests: Dict[str, ModerationRequest] = {}

@app.post("/whitelist")
async def submit_whitelist(entry: WhitelistEntry):
    req = ModerationRequest(
        id=uuid4(),
        type=RequestType.whitelist,
        submitted_at=datetime.utcnow(),
        data=entry.dict()
    )
    pending_requests[str(req.id)] = req
    await send_moderation_request(str(req.id), req.type.value, req.data)
    return {"detail": "Submitted for moderation", "id": req.id}

@app.post("/blacklist")
async def submit_blacklist(entry: BlacklistEntry):
    req = ModerationRequest(
        id=uuid4(),
        type=RequestType.blacklist,
        submitted_at=datetime.utcnow(),
        data=entry.dict()
    )
    pending_requests[str(req.id)] = req
    await send_moderation_request(str(req.id), req.type.value, req.data)
    return {"detail": "Submitted for moderation", "id": req.id}

@app.get("/pending")
async def get_pending_requests(user: AdminUser = Depends(get_current_user)):
    return [r for r in pending_requests.values() if r.approved is None]

async def process_moderation_action(request_id: str, approved: bool) -> bool:
    request = pending_requests.get(str(request_id))
    if not request:
        return False

    request.approved = approved

    if approved:
        if request.type == RequestType.whitelist:
            await apply_whitelist(request.data)
        elif request.type == RequestType.blacklist:
            await apply_blacklist(request.data)
    return True

@app.post("/moderate/{request_id}")
async def moderate_request(request_id: UUID, approved: bool, user: AdminUser = Depends(get_current_user)):
    success = await process_moderation_action(str(request_id), approved)
    if not success:
        raise HTTPException(status_code=404, detail="Request not found")
    
    return {"detail": "Request processed", "approved": approved}