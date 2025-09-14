from fastapi import HTTPException
from bson import ObjectId
from app.db.mongodb import mongodb

# -----------------------------------
# Utility: get role of a user in a project
# -----------------------------------
async def get_user_role(user_id: str, project_id: str) -> str:
    """
    Look up the role of the user inside the project_members collection.
    Returns "admin", "member", or "viewer". Defaults to "viewer" if not found.
    """
    if mongodb.db is None:
        raise HTTPException(status_code=500, detail="Database not initialized")

    membership = await mongodb.db.project_members.find_one({
        "projectId": ObjectId(project_id),
        "userId": ObjectId(user_id)
    })
    if not membership:
        return "viewer"
    roles = membership.get("roles", [])
    if "admin" in roles:
        return "admin"
    if "member" in roles:
        return "member"
    return "viewer"


# -----------------------------------
# Permission checks
# -----------------------------------
async def can_create_issue(user_id: str, project_id: str) -> bool:
    role = await get_user_role(user_id, project_id)
    return role in ["admin", "member"]


async def can_edit_issue(user_id: str, issue: dict, project_id: str) -> bool:
    role = await get_user_role(user_id, project_id)
    if role == "admin":
        return True
    if role == "member":
        return (
            issue.get("reporterId") == str(user_id)
            or issue.get("assigneeId") == str(user_id)
        )
    return False


async def can_delete_issue(user_id: str, project_id: str) -> bool:
    role = await get_user_role(user_id, project_id)
    return role == "admin"


async def can_transition_issue(user_id: str, issue: dict, project_id: str) -> bool:
    role = await get_user_role(user_id, project_id)
    if role == "admin":
        return True
    if role == "member":
        return (
            issue.get("reporterId") == str(user_id)
            or issue.get("assigneeId") == str(user_id)
        )
    return False
