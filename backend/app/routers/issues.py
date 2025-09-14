from fastapi import APIRouter, HTTPException, Depends, Query, UploadFile, File
from bson import ObjectId
from datetime import datetime
from app.db.mongodb import mongodb
from app.schemas.issue import IssueCreate, IssueOut
from app.schemas.comment import CommentCreate, CommentOut
from app.schemas.history import HistoryOut
from app.core.deps import get_current_active_user
from app.core.permissions import (
    can_create_issue,
    can_edit_issue,
    can_delete_issue,
    can_transition_issue,
)
from typing import Optional
import os

router = APIRouter()
UPLOAD_DIR = "uploads"

# --- Create Issue ---
@router.post("/", response_model=IssueOut)
async def create_issue(issue: IssueCreate, current_user=Depends(get_current_active_user)):
    if mongodb.db is None:
        raise HTTPException(status_code=500, detail="Database not initialized")

    allowed = await can_create_issue(str(current_user["_id"]), issue.projectId)
    if not allowed:
        raise HTTPException(status_code=403, detail="You cannot create issues in this project")

    # Generate issue key
    project = await mongodb.db.projects.find_one({"_id": ObjectId(issue.projectId)})
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    prefix = project["key"]
    count = await mongodb.db.issues.count_documents({"projectId": issue.projectId})
    key = f"{prefix}-{count + 1}"

    new_issue = {
        "projectId": issue.projectId,
        "key": key,
        "summary": issue.summary,
        "description": issue.description,
        "status": "To Do",
        "assigneeId": issue.assigneeId,
        "priority": issue.priority,
        "labels": issue.labels,
        "customFields": issue.customFields,
        "reporterId": str(current_user["_id"]),   # ✅ who created it
        "createdAt": datetime.utcnow()
    }
    result = await mongodb.db.issues.insert_one(new_issue)
    return IssueOut(id=str(result.inserted_id), **new_issue)


# --- Update Issue ---
@router.patch("/{issue_id}")
async def update_issue(issue_id: str, updates: dict, current_user=Depends(get_current_active_user)):
    if mongodb.db is None:
        raise HTTPException(status_code=500, detail="Database not initialized")

    issue = await mongodb.db.issues.find_one({"_id": ObjectId(issue_id)})
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    allowed = await can_edit_issue(str(current_user["_id"]), issue, issue["projectId"])
    if not allowed:
        raise HTTPException(status_code=403, detail="You cannot edit this issue")

    changes = {}
    for field, new_value in updates.items():
        old_value = issue.get(field)
        if old_value != new_value:
            changes[field] = (old_value, new_value)

    if changes:
        await mongodb.db.issues.update_one(
            {"_id": ObjectId(issue_id)},
            {"$set": updates}
        )
        for field, (old, new) in changes.items():
            await mongodb.db.issue_history.insert_one({
                "issueId": issue_id,
                "changedBy": str(current_user["_id"]),
                "field": field,
                "fromValue": str(old) if old is not None else None,
                "toValue": str(new),
                "createdAt": datetime.utcnow()
            })
    
    watchers = issue.get("watchers", [])
    for w in watchers:
        if w != str(current_user["_id"]):
            await mongodb.db.notifications.insert_one({
                "userId": w,
                "issueId": issue_id,
                "message": f"Issue {issue['key']} updated: {list(changes.keys())}",
                "createdAt": datetime.utcnow(),
                "read": False
            })


    return {"msg": "Issue updated", "changes": list(changes.keys())}


# --- Delete Issue ---
@router.delete("/{issue_id}")
async def delete_issue(issue_id: str, current_user=Depends(get_current_active_user)):
    if mongodb.db is None:
        raise HTTPException(status_code=500, detail="Database not initialized")

    issue = await mongodb.db.issues.find_one({"_id": ObjectId(issue_id)})
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    allowed = await can_delete_issue(str(current_user["_id"]), issue["projectId"])
    if not allowed:
        raise HTTPException(status_code=403, detail="You cannot delete this issue")

    await mongodb.db.issues.delete_one({"_id": ObjectId(issue_id)})

    await mongodb.db.issue_history.insert_one({
        "issueId": issue_id,
        "changedBy": str(current_user["_id"]),
        "field": "deleted",
        "fromValue": None,
        "toValue": "Issue deleted",
        "createdAt": datetime.utcnow()
    })

    return {"msg": "Issue deleted"}


# --- Transition Issue ---
@router.post("/{issue_id}/transition")
async def transition_issue(issue_id: str, payload: dict, current_user=Depends(get_current_active_user)):
    if mongodb.db is None:
        raise HTTPException(status_code=500, detail="Database not initialized")

    new_status = payload.get("status")
    if not new_status:
        raise HTTPException(status_code=400, detail="status required")

    issue = await mongodb.db.issues.find_one({"_id": ObjectId(issue_id)})
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    allowed = await can_transition_issue(str(current_user["_id"]), issue, issue["projectId"])
    if not allowed:
        raise HTTPException(status_code=403, detail="You cannot transition this issue")

    project = await mongodb.db.projects.find_one({"_id": ObjectId(issue["projectId"])})
    workflow = await mongodb.db.workflows.find_one({"_id": ObjectId(project["workflowId"])})

    current_status = issue["status"]
    allowed_transitions = workflow["transitions"].get(current_status, [])
    if new_status not in allowed_transitions:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot transition from {current_status} to {new_status}"
        )

    await mongodb.db.issues.update_one(
        {"_id": ObjectId(issue_id)},
        {"$set": {"status": new_status}}
    )

    await mongodb.db.issue_history.insert_one({
        "issueId": issue_id,
        "changedBy": str(current_user["_id"]),
        "field": "status",
        "fromValue": current_status,
        "toValue": new_status,
        "createdAt": datetime.utcnow()
    })

    watchers = issue.get("watchers", [])
    for w in watchers:
        if w != str(current_user["_id"]):
            await mongodb.db.notifications.insert_one({
                "userId": w,
                "issueId": issue_id,
                "message": f"Issue {issue['key']} updated: {list(changes.keys())}",
                "createdAt": datetime.utcnow(),
                "read": False
            })


    return {"msg": f"Issue moved from {current_status} → {new_status}"}

# ✅ Get backlog issues (no sprint assigned)
@router.get("/projects/{project_id}/backlog", response_model=list[IssueOut])
async def get_backlog(project_id: str, current_user=Depends(get_current_active_user)):
    cursor = mongodb.db.issues.find({"projectId": project_id, "sprintId": None})
    issues = []
    async for doc in cursor:
        issues.append(IssueOut(id=str(doc["_id"]), **doc))
    return issues

# ✅ Get active sprint board (issues grouped by status)
@router.get("/projects/{project_id}/board")
async def get_board(project_id: str, current_user=Depends(get_current_active_user)):
    sprint = await mongodb.db.sprints.find_one({"projectId": ObjectId(project_id), "status": "active"})
    if not sprint:
        raise HTTPException(404, "No active sprint")

    issues_by_status = {}
    cursor = mongodb.db.issues.find({"projectId": project_id, "sprintId": str(sprint["_id"])})
    async for issue in cursor:
        status = issue.get("status", "To Do")
        issues_by_status.setdefault(status, []).append({
            "id": str(issue["_id"]),
            "key": issue["key"],
            "summary": issue["summary"],
            "assigneeId": issue.get("assigneeId"),
            "priority": issue.get("priority")
        })
    return {"sprint": sprint["name"], "issues": issues_by_status}

# ✅ Search / filter issues
@router.get("/projects/{project_id}/search", response_model=list[IssueOut])
async def search_issues(
    project_id: str,
    status: Optional[str] = Query(None),
    assigneeId: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    label: Optional[str] = Query(None),
    current_user=Depends(get_current_active_user)
):
    if mongodb.db is None:
        raise HTTPException(500, "Database not initialized")

    query = {"projectId": project_id}
    if status:
        query["status"] = status
    if assigneeId:
        query["assigneeId"] = assigneeId
    if priority:
        query["priority"] = priority
    if label:
        query["labels"] = label

    issues = []
    cursor = mongodb.db.issues.find(query)
    async for doc in cursor:
        issues.append(IssueOut(id=str(doc["_id"]), **doc))
    return issues


# ✅ Add self as watcher
@router.post("/{issue_id}/watch")
async def watch_issue(issue_id: str, current_user=Depends(get_current_active_user)):
    await mongodb.db.issues.update_one(
        {"_id": ObjectId(issue_id)},
        {"$addToSet": {"watchers": str(current_user["_id"])}}
    )
    return {"msg": "Watching issue"}

# ✅ Remove self as watcher
@router.post("/{issue_id}/unwatch")
async def unwatch_issue(issue_id: str, current_user=Depends(get_current_active_user)):
    await mongodb.db.issues.update_one(
        {"_id": ObjectId(issue_id)},
        {"$pull": {"watchers": str(current_user["_id"])}}
    )
    return {"msg": "Unwatched issue"}

@router.post("/{issue_id}/attachments")
async def upload_attachment(
    issue_id: str,
    file: UploadFile = File(...),
    current_user=Depends(get_current_active_user)
):
    if mongodb.db is None:
        raise HTTPException(500, "Database not initialized")

    issue = await mongodb.db.issues.find_one({"_id": ObjectId(issue_id)})
    if not issue:
        raise HTTPException(404, "Issue not found")

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    await mongodb.db.issues.update_one(
        {"_id": ObjectId(issue_id)},
        {"$push": {"attachments": {"filename": file.filename, "path": file_path}}}
    )

    return {"msg": "File uploaded", "filename": file.filename}