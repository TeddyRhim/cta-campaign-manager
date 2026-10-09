# CTA Campaign Manager

Application web de gestion de campagnes permettant de centraliser le suivi des campagnes, la gestion des contacts et l'import de données.

Le projet est composé d'une API REST développée avec FastAPI et d'une interface utilisateur développée avec Next.js.

## Aperçu

Captures réalisées avec des données fictives.

| Tableau de bord | Liste des campagnes | Détail d'une campagne |
| --- | --- | --- |
| ![Tableau de bord](docs/screenshots/dashboard.jpg) | ![Liste des campagnes](docs/screenshots/campagnes.jpg) | ![Détail d'une campagne](docs/screenshots/detail-campagne.jpg) |

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

* Création, consultation, modification et suppression des campagnes
* Consultation du détail d'une campagne
* Association de contacts à une campagne
* Gestion des statuts

Statuts disponibles :

```
DRAFT
ACTIVE
PAUSED
FINISHED
```

## Tableau de bord

* Nombre de campagnes, de contacts et d'imports (`GET /dashboard/stats`)

## Contacts

* Création et consultation de la liste des contacts
* Adresse e-mail et téléphone uniques
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
├── alembic/            # migrations
├── scripts/
│   └── create_admin.py # création d'un compte administrateur (identifiants saisis, jamais en dur)
└── app/
    ├── core/           # configuration, sécurité (JWT), permissions, dépendances
    ├── db/             # moteur et sessions SQLAlchemy
    ├── models/         # user, campaign, contact, contact_campaign, imports, enums
    ├── schemas/
    ├── services/       # logique métier (dont importers/ pour les fichiers CSV)
    ├── routers/        # auth, campaigns, contacts, imports, dashboard
    └── main.py
```

| Dossier  | Rôle                                          |
| -------- | --------------------------------------------- |
| routers  | Gestion des endpoints API                     |
| services | Logique métier                                |
| schemas  | Validation des données entrantes et sortantes |
| models   | Modèles SQLAlchemy                            |
| core     | Configuration, sécurité et dépendances        |
| db       | Connexion à la base et sessions               |

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
python -m venv .venv
```

Activation :

Windows :

```bash
.venv\Scripts\activate
```

Linux / Mac :

```bash
source .venv/bin/activate
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

Créer la base PostgreSQL correspondante, puis lancer les migrations :

```bash
alembic upgrade head
```

Créer un compte administrateur (l'adresse et le mot de passe sont demandés au lancement, le mot de passe n'est pas affiché) :

```bash
python -m scripts.create_admin
```

Pour automatiser, passer les valeurs par variables d'environnement (jamais dans le code ni dans le dépôt) :

```bash
ADMIN_EMAIL=moi@exemple.fr ADMIN_PASSWORD='un-mot-de-passe-long' python -m scripts.create_admin
```

Le mot de passe doit faire au moins 12 caractères. Aucun identifiant par défaut n'est fourni.

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

| Domaine | Méthode et route |
| --- | --- |
| Authentification | `POST /auth/register`, `POST /auth/login`, `GET /auth/me` |
| Campagnes | `POST /campaigns/`, `GET /campaigns/`, `GET /campaigns/{id}`, `PUT /campaigns/{id}`, `DELETE /campaigns/{id}`, `POST /campaigns/{id}/contacts/{contact_id}` |
| Contacts | `POST /contacts/`, `GET /contacts/` |
| Imports | `POST /imports/`, `GET /imports/`, `GET /imports/{id}` |
| Tableau de bord | `GET /dashboard/stats` |

La documentation interactive complète est disponible sur `/docs` (Swagger).

---

# Sécurité

Le projet utilise :

* Authentification JWT
* Protection des routes backend
* Vérification des permissions utilisateur
* Validation des données avec Pydantic
* CORS limité à `http://localhost:3000` : à adapter dans `backend/app/main.py` pour un autre hébergement

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
* [x] Tableau de bord (compteurs)
* [ ] Statistiques avancées
* [ ] Tests automatisés

---

# Auteur

Projet Full Stack réalisé avec FastAPI et Next.js.
