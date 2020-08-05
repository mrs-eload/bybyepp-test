from fastapi import APIRouter

from app.api import authentication, ligands, users, projects, registration, search, structures

api_router = APIRouter()

@api_router.get("/")
def read_root():
    return {"Hello": "World"}

#
# api_router.include_router(authentication.router, tags=["login"])
# api_router.include_router(users.router, prefix="/users", tags=["users"])

#models
api_router.include_router(structures.router, prefix="/structures", tags=["structures"])
# api_router.include_router(ligands.router, prefix="/ligands", tags=["ligands"])
# api_router.include_router(projects.router, prefix="/projects", tags=["projects"])

# api_router.include_router(search.router, prefix="/search", tags=["search"])
