from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from app.db.mongodb import mongodb
from app.schemas.project import ProjectCreate, ProjectOut
from app.core.deps import get_current_active_user

router = APIRouter()

@router.post("/", response_model=ProjectOut)
async def create_project(
    project: ProjectCreate,
    current_user=Depends(get_current_active_user)
):
    if mongodb.db is None:
        raise HTTPException(status_code=500, detail="Database not initialized")

    # Prevent duplicate project keys
    existing = await mongodb.db.projects.find_one({"key": project.key})
    if existing:
        raise HTTPException(status_code=400, detail="Project key already exists")

    # ✅ Ensure default workflow exists
    default_wf = await mongodb.db.workflows.find_one({"name": "Simple Workflow"})
    if not default_wf:
        default_wf_doc = {
            "name": "Simple Workflow",
            "statuses": ["To Do", "In Progress", "Done"],
            "transitions": {
                "To Do": ["In Progress"],
                "In Progress": ["Done", "To Do"],
                "Done": []
            }
        }
        wf_result = await mongodb.db.workflows.insert_one(default_wf_doc)
        default_wf_doc["_id"] = wf_result.inserted_id
        default_wf = default_wf_doc

    # ✅ Create new project
    new_project = {
        "key": project.key,
        "name": project.name,
        "description": project.description,
        "orgId": "demo-org-id",  # later connect to real orgs
        "leadUserId": str(current_user["_id"]),
        "workflowId": default_wf["_id"]
    }
    result = await mongodb.db.projects.insert_one(new_project)

    # Add creator as admin
    await mongodb.db.project_members.insert_one({
        "projectId": result.inserted_id,
        "userId": current_user["_id"],
        "roles": ["admin"]
    })

    return ProjectOut(id=str(result.inserted_id), **new_project)


@router.get("/{project_id}", response_model=ProjectOut)
async def get_project(
    project_id: str,
    current_user=Depends(get_current_active_user)
):
    if mongodb.db is None:
        raise HTTPException(status_code=500, detail="Database not initialized")

    project = await mongodb.db.projects.find_one({"_id": ObjectId(project_id)})
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return ProjectOut(id=str(project["_id"]), **project)
