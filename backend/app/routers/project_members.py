from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from app.db.mongodb import mongodb
from app.core.deps import get_current_active_user
from app.core.permissions import get_user_role
from app.schemas.project_member import ProjectMemberInvite, ProjectMemberOut

router = APIRouter()

# ✅ Invite user to project
@router.post("/{project_id}/invite", response_model=ProjectMemberOut)
async def invite_member(
    project_id: str,
    payload: ProjectMemberInvite,
    current_user=Depends(get_current_active_user)
):
    if mongodb.db is None:
        raise HTTPException(status_code=500, detail="Database not initialized")

    # Only admins can invite
    role = await get_user_role(str(current_user["_id"]), project_id)
    if role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can invite members")

    # Check user exists
    user = await mongodb.db.users.find_one({"email": payload.email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Add or update membership
    await mongodb.db.project_members.update_one(
        {"projectId": ObjectId(project_id), "userId": user["_id"]},
        {"$set": {"roles": payload.roles}},
        upsert=True
    )

    return ProjectMemberOut(
        userId=str(user["_id"]),
        email=user["email"],
        fullName=user["fullName"],
        roles=payload.roles
    )


# ✅ List project members
@router.get("/{project_id}/members", response_model=list[ProjectMemberOut])
async def list_members(project_id: str, current_user=Depends(get_current_active_user)):
    if mongodb.db is None:
        raise HTTPException(status_code=500, detail="Database not initialized")

    members = []
    cursor = mongodb.db.project_members.find({"projectId": ObjectId(project_id)})
    async for m in cursor:
        user = await mongodb.db.users.find_one({"_id": m["userId"]})
        if user:
            members.append(ProjectMemberOut(
                userId=str(user["_id"]),
                email=user["email"],
                fullName=user["fullName"],
                roles=m["roles"]
            ))
    return members


# ✅ Remove a member
@router.delete("/{project_id}/remove/{user_id}")
async def remove_member(project_id: str, user_id: str, current_user=Depends(get_current_active_user)):
    if mongodb.db is None:
        raise HTTPException(status_code=500, detail="Database not initialized")

    # Only admins can remove
    role = await get_user_role(str(current_user["_id"]), project_id)
    if role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can remove members")

    result = await mongodb.db.project_members.delete_one(
        {"projectId": ObjectId(project_id), "userId": ObjectId(user_id)}
    )
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Member not found in project")

    return {"msg": "Member removed from project"}
