from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from datetime import datetime
from app.db.mongodb import mongodb
from app.core.deps import get_current_active_user
from app.schemas.sprint import SprintCreate, SprintOut
from app.core.permissions import get_user_role

router = APIRouter()

# ✅ Create sprint
@router.post("/{project_id}/sprints", response_model=SprintOut)
async def create_sprint(
    project_id: str,
    sprint: SprintCreate,
    current_user=Depends(get_current_active_user)
):
    if mongodb.db is None:
        raise HTTPException(500, "Database not initialized")

    # only admins
    role = await get_user_role(str(current_user["_id"]), project_id)
    if role != "admin":
        raise HTTPException(403, "Only admins can create sprints")

    doc = {
        "projectId": ObjectId(project_id),
        "name": sprint.name,
        "goal": sprint.goal,
        "startDate": sprint.startDate,
        "endDate": sprint.endDate,
        "status": "planned",
        "issues": []
    }
    result = await mongodb.db.sprints.insert_one(doc)
    return SprintOut(id=str(result.inserted_id), **doc)

# ✅ Start sprint
@router.post("/sprints/{sprint_id}/start")
async def start_sprint(sprint_id: str, current_user=Depends(get_current_active_user)):
    sprint = await mongodb.db.sprints.find_one({"_id": ObjectId(sprint_id)})
    if not sprint:
        raise HTTPException(404, "Sprint not found")

    await mongodb.db.sprints.update_one(
        {"_id": ObjectId(sprint_id)},
        {"$set": {"status": "active", "startDate": datetime.utcnow()}}
    )
    return {"msg": "Sprint started"}

# ✅ Complete sprint
@router.post("/sprints/{sprint_id}/complete")
async def complete_sprint(sprint_id: str, current_user=Depends(get_current_active_user)):
    sprint = await mongodb.db.sprints.find_one({"_id": ObjectId(sprint_id)})
    if not sprint:
        raise HTTPException(404, "Sprint not found")

    await mongodb.db.sprints.update_one(
        {"_id": ObjectId(sprint_id)},
        {"$set": {"status": "completed", "endDate": datetime.utcnow()}}
    )
    return {"msg": "Sprint completed"}
