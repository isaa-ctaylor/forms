from uuid import UUID

from crud import user as user_crud
from crud.utils import check_role
from deps import get_current_user, get_db, require_roles
from fastapi import APIRouter, Depends, HTTPException
from schemas import user as user_schema
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/", response_model=user_schema.User)
def create_user(
    user: user_schema.UserCreate,
    db: Session = Depends(get_db),
    _: None = require_roles["admin"],
):
    db_user = user_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400, detail={"message": "Email already registered"}
        )
    return user_crud.create_user(db=db, user=user)


@router.get("/", response_model=list[user_schema.User])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: None = require_roles["admin", "moderator"],
):
    users = user_crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/me", response_model=user_schema.User)
def get_me(current_user: user_schema.User = Depends(get_current_user)):
    """Get the currently authenticated user's details."""
    return current_user


def get_user_by_uuid(uuid, db):
    db_user = user_crud.get_user_by_uuid(db, uuid=str(uuid))
    if db_user is None:
        raise HTTPException(status_code=404, detail={"message": "User not found"})
    return db_user


@router.get("/{uuid}", response_model=user_schema.User)
def read_user(
    uuid: UUID,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(get_current_user),
):
    """Get a user by UUID. Only admins can access this endpoint with regards to other users. Users can access their own details."""
    if current_user.uuid != str(uuid) and not check_role(current_user, "admin"):
        raise HTTPException(
            status_code=403,
            detail={
                "message": "You do not have the required permissions to access this resource."
            },
        )
    return get_user_by_uuid(uuid, db)


@router.put("/{uuid}", response_model=user_schema.User)
def update_user(
    uuid: UUID,
    user: user_schema.UserUpdate,
    db: Session = Depends(get_db),
    _: None = require_roles["admin"],  # Enforce admin role
):
    uuid = str(uuid)
    db_user = user_crud.get_user_by_uuid(db, uuid=uuid)
    if db_user is None:
        raise HTTPException(status_code=404, detail={"message": "User not found"})
    updated_user = user_crud.update_user(db=db, uuid=uuid, user_update=user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail={"message": "User not found"})
    return updated_user


@router.delete("/{uuid}", response_model=dict)
def delete_user(
    uuid: UUID,
    db: Session = Depends(get_db),
    _: None = require_roles["admin"],  # Enforce admin role
):
    # Check if there are any other admins (only allow deletion if there are others)
    other_admins = user_crud.get_users_by_role(db, role="admin")
    if len(other_admins) <= 1:
        raise HTTPException(
            status_code=400,
            detail={"message": "Cannot delete the last admin user"},
        )

    if user_crud.delete_user(db, uuid=str(uuid)):
        return {"ok": True}
    else:
        raise HTTPException(status_code=404, detail={"message": "User not found"})
