from uuid import UUID

from crud import user as user_crud
from deps import get_db
from fastapi import APIRouter, Depends, HTTPException
from schemas import user as user_schema
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/", response_model=user_schema.User)
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_crud.create_user(db=db, user=user)


@router.get("/", response_model=list[user_schema.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = user_crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_uuid}", response_model=user_schema.User)
def read_user(user_uuid: UUID, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_uuid(db, uuid=str(user_uuid))
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/member_id/{member_id}", response_model=user_schema.User)
def read_user_by_member_id(member_id: str, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_member_id(db, member_id=member_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put("/{uuid}", response_model=user_schema.User)
def update_user(
    uuid: UUID, user: user_schema.UserCreate, db: Session = Depends(get_db)
):
    uuid = str(uuid)
    db_user = user_crud.get_user_by_uuid(db, uuid=uuid)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    updated_user = user_crud.update_user(db=db, uuid=uuid, user_update=user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@router.delete("/{uuid}", response_model=dict)
def delete_user(uuid: UUID, db: Session = Depends(get_db)):
    if user_crud.delete_user(db, uuid=str(uuid)):
        return {"ok": True}
    else:
        raise HTTPException(status_code=404, detail="User not found")
