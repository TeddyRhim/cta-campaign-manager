"""Crée un compte administrateur.

L'adresse et le mot de passe ne sont jamais écrits dans le code :
- variables d'environnement ADMIN_EMAIL et ADMIN_PASSWORD (utile en script) ;
- sinon, saisie interactive (le mot de passe n'est pas affiché).
"""
import os
import sys
from getpass import getpass

from app.core.security import hash_password
from app.db.database import SessionLocal
from app.models.enums import UserRole
from app.models.user import User

MIN_PASSWORD_LENGTH = 12


def read_credentials():
    email = os.environ.get("ADMIN_EMAIL") or input("E-mail de l'administrateur : ").strip()
    password = os.environ.get("ADMIN_PASSWORD")
    if not password:
        password = getpass(f"Mot de passe (au moins {MIN_PASSWORD_LENGTH} caractères) : ")
        if password != getpass("Confirmer le mot de passe : "):
            sys.exit("Les mots de passe ne correspondent pas.")
    if "@" not in email:
        sys.exit("Adresse e-mail invalide.")
    if len(password) < MIN_PASSWORD_LENGTH:
        sys.exit(f"Mot de passe trop court : {MIN_PASSWORD_LENGTH} caractères minimum.")
    return email, password


def create_admin():
    email, password = read_credentials()
    db = SessionLocal()
    try:
        if db.query(User).filter(User.email == email).first():
            print("Cet administrateur existe déjà.")
            return

        admin = User(
            email=email,
            password_hash=hash_password(password),
            role=UserRole.ADMIN,
            first_name="Admin",
            last_name="CTA",
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)

        print("Administrateur créé.")
        print(f"E-mail : {admin.email}")
        print(f"Rôle : {admin.role}")
    finally:
        db.close()


if __name__ == "__main__":
    create_admin()
