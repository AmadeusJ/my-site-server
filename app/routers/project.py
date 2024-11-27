from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas import ProjectList, ProjectDetail, ChatMessageCreate

router = APIRouter()


@router.get("/projects", response_model=ProjectList)
async def get_projects(db: AsyncSession = Depends(get_db)):
    projects = await db.execute(select(Portfolio))
    return ProjectList(projects=projects.scalars().all())


@router.get("/projects/{project_id}", response_model=ProjectDetail)
async def get_project(project_id: int, db: AsyncSession = Depends(get_db)):
    project = await db.get(Portfolio, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return ProjectDetail(project=project)


