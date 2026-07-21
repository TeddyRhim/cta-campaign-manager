from app.db.database import SessionLocal
from app.models.user import User
from app.models.enums import UserRole
from app.core.security import hash_password


def create_admin():

    db = SessionLocal()

    try:

        email = "admin@cta.com"
        password = "AdminPassword123"

        existing_user = db.query(User).filter(
            User.email == email
        ).first()


        if existing_user:
            print("Admin already exists")
            return


        admin = User(
            email=email,
            password_hash=hash_password(password),
            role=UserRole.ADMIN,
            first_name="Admin",
            last_name="CTA"
        )


        db.add(admin)
        db.commit()
        db.refresh(admin)


        print("Admin created successfully")
        print(f"Email : {admin.email}")
        print(f"Role : {admin.role}")


    finally:
        db.close()


if __name__ == "__main__":
    create_admin()