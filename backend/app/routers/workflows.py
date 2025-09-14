from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from app.db.mongodb import mongodb
from app.schemas.workflow import WorkflowCreate, WorkflowOut
from app.core.deps import get_current_active_user

router = APIRouter()

# ✅ Create workflow
@router.post("/", response_model=WorkflowOut)
async def create_workflow(
    wf: WorkflowCreate,
    current_user=Depends(get_current_active_user)
):
    if mongodb.db is None:
        raise HTTPException(status_code=500, detail="Database not initialized")

    doc = wf.dict()
    result = await mongodb.db.workflows.insert_one(doc)
    return WorkflowOut(id=str(result.inserted_id), **doc)

# ✅ Get workflow
@router.get("/{workflow_id}", response_model=WorkflowOut)
async def get_workflow(workflow_id: str, current_user=Depends(get_current_active_user)):
    if mongodb.db is None:
        raise HTTPException(status_code=500, detail="Database not initialized")

    wf = await mongodb.db.workflows.find_one({"_id": ObjectId(workflow_id)})
    if not wf:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return WorkflowOut(id=str(wf["_id"]), **wf)
