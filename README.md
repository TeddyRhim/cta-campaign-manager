# CTA Campaign Manager

Application web de gestion de campagnes permettant de créer et suivre des campagnes, gérer des contacts et importer des fichiers associés.

Le projet est composé d'un backend FastAPI exposant une API REST et d'un frontend Next.js permettant d'interagir avec les différentes fonctionnalités.

---

# Stack technique

## Backend

- Python 3.11
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic (migrations)
- Pydantic
- JWT Authentication

## Frontend

- Next.js
- TypeScript
- Tailwind CSS
- Axios
- React Hooks

---

# Fonctionnalités

## Authentification

- Connexion utilisateur via JWT
- Gestion des utilisateurs
- Gestion des rôles (ex: administrateur)

## Campagnes

- Consultation des campagnes
- Consultation du détail d'une campagne
- Gestion du statut des campagnes

Statuts disponibles :

- DRAFT
- ACTIVE
- DONE
- ...

## Contacts

- Consultation de la liste des contacts
- Recherche côté frontend

## Imports

- Consultation de l'historique des imports
- Recherche par nom de fichier
- Import de fichiers depuis le frontend
- Association d'un import à une campagne

---

# Architecture

## Backend

Le backend suit une séparation par responsabilités :

backend/
└── app/
├── core/
│ ├── config.py
│ ├── database.py
│ └── dependencies.py
│
├── models/
│ ├── user.py
│ ├── campaign.py
│ ├── contact.py
│ └── imports.py
│
├── schemas/
│
├── services/
│
├── routers/
│
└── main.py



Organisation :

- `routers` : gestion des routes API
- `schemas` : validation des données entrantes/sortantes
- `models` : modèles SQLAlchemy
- `services` : logique métier
- `core` : configuration et dépendances globales

---

## Frontend

Organisation principale :

frontend/
├── app/
│
├── components/
│ ├── campaign/
│ ├── contact/
│ ├── import/
│ ├── dashboard/
│ └── ui/
│
├── hooks/
│
├── services/
│
└── types/


Organisation :

- `app` : pages et routing Next.js
- `components` : composants réutilisables
- `hooks` : logique de récupération des données
- `services` : appels API
- `types` : typage TypeScript

---

# Installation

## Prérequis

- Python >= 3.11
- Node.js >= 22
- PostgreSQL

---

# Backend

Se placer dans le dossier backend :

```bash
cd backend

env virtuel :
python -m venv venv (windows : venv\Scripts\activate)

dépendances :
pip install -r requirements.txt

Crée .env
DATABASE_URL=postgresql://user:password@localhost:5432/database
SECRET_KEY=your_secret_key


start : uvicorn app.main:app --reload

api : http://localhost:8000 / docs : http://localhost:8000/docs


Se placer dans le dossier frontend :

cd frontend

Installer les dépendances :

npm install

Créer un fichier .env.local :

NEXT_PUBLIC_API_URL=http://localhost:8000

Lancer le serveur :

npm run dev

Application disponible sur :

http://localhost:3000



API principales
Authentification
POST /auth/login
Campagnes
GET /campaigns/
GET /campaigns/{id}
Contacts
GET /contacts/
Imports
GET /imports/
POST /imports/

Sécurité

Le projet utilise :

Authentification JWT
Routes protégées via dépendances FastAPI
Contrôle des permissions selon le rôle utilisateur

Améliorations possibles

Plusieurs évolutions peuvent être ajoutées :

Backend
    Ajout d'un système de refresh token JWT
    Ajout d'une pagination backend
    Ajout d'une couche repository
    Ajout de tests automatisés
    Gestion avancée des erreurs
Frontend
    Dashboard avec statistiques avancées
    Graphiques d'activité
    Animations et transitions
    Pagination ou infinite scroll
    Gestion globale des erreurs API