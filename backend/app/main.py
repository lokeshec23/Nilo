from fastapi import FastAPI
from app.db.mongodb import connect_to_mongo, close_mongo_connection
from app.routers import auth, projects, issues, project_members
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(title="Nilo - Jira Clone")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # during dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(projects.router, prefix="/projects", tags=["projects"])
app.include_router(issues.router, prefix="/issues", tags=["issues"])
app.include_router(project_members.router, prefix="/projects", tags=["project-members"])
