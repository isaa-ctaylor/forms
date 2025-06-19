from crud import user as user_crud
from database.database import get_db
from schemas.user import UserCreate
from sqlalchemy.orm import Session
from utils.password import generate_memorable_password


def create_default_admin():
    """Create a default admin user if it does not exist."""
    db: Session = next(get_db())
    admins = user_crud.get_users_by_role(db, role="admin")
    if not admins:
        password = generate_memorable_password()
        admin_user = UserCreate(
            email="admin@admin.admin", password=password, role="admin"
        )
        user_crud.create_user(db, user=admin_user)
        print(
            f"No admin user found. Created default admin user with username 'admin@admin.admin' and password '{password}' PLEASE CHANGE IT IMMEDIATELY AFTER LOGIN!"
        )
