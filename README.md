# CTA Campaign Manager

Application web de gestion de campagnes permettant de centraliser le suivi des campagnes, la gestion des contacts et l'import de données.

Le projet est composé d'une API REST développée avec FastAPI et d'une interface utilisateur développée avec Next.js.

---

# Stack technique

## Backend

| Technologie | Utilisation            |
| ----------- | ---------------------- |
| Python 3.11 | Langage principal      |
| FastAPI     | API REST               |
| PostgreSQL  | Base de données        |
| SQLAlchemy  | ORM                    |
| Alembic     | Gestion des migrations |
| JWT         | Authentification       |
| Pydantic    | Validation des données |

## Frontend

| Technologie  | Utilisation                     |
| ------------ | ------------------------------- |
| Next.js      | Framework React                 |
| TypeScript   | Typage statique                 |
| Tailwind CSS | Interface utilisateur           |
| Axios        | Communication avec l'API        |
| React Hooks  | Gestion des données côté client |

---

# Fonctionnalités

## Authentification

* Connexion utilisateur via JWT
* Protection des routes API
* Gestion des rôles utilisateurs

## Campagnes

* Consultation des campagnes
* Consultation du détail d'une campagne
* Gestion des statuts

Statuts disponibles :

```
DRAFT
ACTIVE
DONE
```

## Contacts

* Consultation de la liste des contacts
* Recherche dynamique côté frontend

## Imports

* Consultation de l'historique des imports
* Recherche par fichier
* Import de fichiers depuis le frontend
* Association d'un import à une campagne

---

# Architecture

## Backend

Le backend suit une séparation par responsabilités :

```
backend/
└── app/
    ├── core/
    │   ├── config.py
    │   ├── database.py
    │   └── dependencies.py
    │
    ├── models/
    │   ├── user.py
    │   ├── campaign.py
    │   ├── contact.py
    │   └── imports.py
    │
    ├── schemas/
    │
    ├── services/
    │
    ├── routers/
    │
    └── main.py
```

| Dossier  | Rôle                                          |
| -------- | --------------------------------------------- |
| routers  | Gestion des endpoints API                     |
| services | Logique métier                                |
| schemas  | Validation des données entrantes et sortantes |
| models   | Modèles SQLAlchemy                            |
| core     | Configuration globale et dépendances          |

---

## Frontend

```
frontend/
├── app/
│
├── components/
│   ├── campaign/
│   ├── contact/
│   ├── import/
│   ├── dashboard/
│   └── ui/
│
├── hooks/
│
├── services/
│
└── types/
```

| Dossier    | Rôle                              |
| ---------- | --------------------------------- |
| app        | Pages et routing Next.js          |
| components | Composants réutilisables          |
| hooks      | Gestion de la logique côté client |
| services   | Appels API                        |
| types      | Typage TypeScript                 |

---

# Installation

## Prérequis

* Python >= 3.11
* Node.js >= 22
* PostgreSQL

---

# Backend

Se placer dans le dossier backend :

```bash
cd backend
```

Créer un environnement virtuel :

```bash
python -m venv venv
```

Activation :

Windows :

```bash
venv\Scripts\activate
```

Linux / Mac :

```bash
source venv/bin/activate
```

Installer les dépendances :

```bash
pip install -r requirements.txt
```

Créer un fichier `.env` :

```env
DATABASE_URL=postgresql://user:password@localhost:5432/database
SECRET_KEY=your_secret_key
```

Lancer les migrations :

```bash
alembic upgrade head
```

Démarrer l'API :

```bash
uvicorn app.main:app --reload
```

API disponible sur :

```
http://localhost:8000
```

Documentation Swagger :

```
http://localhost:8000/docs
```

---

# Frontend

Se placer dans le dossier frontend :

```bash
cd frontend
```

Installer les dépendances :

```bash
npm install
```

Créer un fichier `.env.local` :

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Démarrer l'application :

```bash
npm run dev
```

Application disponible sur :

```
http://localhost:3000
```

---

# API principales

## Authentification

```http
POST /auth/login
```

## Campagnes

```http
GET /campaigns/
```

```http
GET /campaigns/{id}
```

## Contacts

```http
GET /contacts/
```

## Imports

```http
GET /imports/
```

```http
POST /imports/
```

---

# Sécurité

Le projet utilise :

* Authentification JWT
* Protection des routes backend
* Vérification des permissions utilisateur
* Validation des données avec Pydantic

---

# Améliorations possibles

## Backend

* Ajout d'un système de refresh token JWT
* Pagination des résultats
* Ajout de tests automatisés
* Gestion centralisée des erreurs
* Ajout d'une couche repository

## Frontend

* Dashboard avec statistiques avancées
* Graphiques d'activité
* Animations UI
* Pagination ou infinite scroll
* Gestion globale des erreurs API

---

# Roadmap

* [x] Authentification
* [x] Gestion des campagnes
* [x] Gestion des contacts
* [x] Gestion des imports
* [x] Interface frontend
* [x] Recherche côté frontend
* [ ] Statistiques avancées
* [ ] Tests automatisés

---

# Auteur

Projet Full Stack réalisé avec FastAPI et Next.js.
