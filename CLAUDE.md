# cta-campaign-manager

Gestion de campagnes, contacts et imports CSV. Backend FastAPI + PostgreSQL (SQLAlchemy, Alembic, JWT, rôles ADMIN et OPERATOR), frontend Next.js 16 / React 19 / Tailwind 4. Le frontend a ses propres règles : lire `frontend/CLAUDE.md` et `frontend/AGENTS.md` avant de toucher au code Next.js (API différente des versions précédentes, documentation dans `node_modules/next/dist/docs/`).

## Commandes
Backend, depuis `backend/` (toujours lancer d'ici, `alembic.ini` a une URL vide et `env.py` lit le `.env`) :
- Installer : `python -m venv .venv`, activer, `pip install -r requirements-dev.txt`.
- Lancer : `uvicorn app.main:app --reload` (port 8000, documentation sur `/docs`).
- Migrations : `alembic upgrade head`.
- Créer un administrateur : `python -m scripts.create_admin` (saisie) ou variables `ADMIN_EMAIL` et `ADMIN_PASSWORD` (12 caractères minimum).
- Tests : `python -m pytest -q`. Lint : `ruff check .` (corriger avec `ruff check . --fix`) ; la CI échoue tant qu'il ne passe pas.

Frontend, depuis `frontend/` : `npm ci`, `npm run dev` (port 3000), `npm run lint`, `npx tsc --noEmit`, `npm run build`. Pas de tests frontend.

La CI (`.github/workflows/ci.yml`) exécute ruff, pytest et `pip-audit` côté backend ; `alembic upgrade head`, `alembic check` et un aller-retour de migration sur PostgreSQL ; lint, types, build et `npm audit` côté frontend. Actions épinglées par SHA, droits en lecture seule.

## Prérequis
Python 3.11+, Node 22+, PostgreSQL (base créée à la main). Variables : `backend/.env` (`DATABASE_URL`, `JWT_SECRET_KEY` obligatoire, `JWT_ALGORITHM`, `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`, `CORS_ORIGINS`) et `frontend/.env.local` (`NEXT_PUBLIC_API_URL`). Pas de Docker. Jamais de secret ni de mot de passe par défaut dans le code.

## Structure
- `backend/app` : `core` (config, sécurité, permissions, dépendances), `db`, `models`, `schemas` (Pydantic v2), `services` (dont `importers/csv_importers.py`), `routers` (auth, campaigns, contacts, imports, dashboard). Routers fins qui délèguent aux services ; permissions via `core/permissions.require_admin`.
- `backend/alembic` (migrations), `backend/scripts` (scripts d'administration), `backend/tests`.
- `frontend/app` (routes), `components`, `hooks` (un hook par ressource), `services` (un service Axios par ressource), `types`, `lib/token.ts`.
- `database/` et `script/` à la racine sont des dossiers locaux vides, non suivis : ne pas s'en servir.

## Règles métier et pièges
- Un opérateur ne voit que ses campagnes et ses imports ; la gestion des contacts est réservée aux ADMIN. `POST /auth/register` est réservé aux administrateurs.
- Listes paginées : `GET /campaigns/`, `/contacts/` et `/imports/` renvoient `{items, total, page, page_size}` ; paramètres `page` (à partir de 1), `page_size` (20 par défaut, 100 au plus) et `search` (texte, sans joker SQL). Toute nouvelle liste passe par `core/pagination.py` (`page_params`, `paginate`) avec un tri stable. Côté frontend, le hook `usePaginatedList` gère page, recherche avec délai et chargement ; la recherche se fait côté serveur, jamais en filtrant la page affichée.
- Les tests forcent `DATABASE_URL=sqlite://` et une clé JWT de test dans `conftest.py` avant tout import : ils ne touchent jamais PostgreSQL. Données de test fictives (`@example.com`).
- Le jeton JWT est stocké dans `localStorage` ; une réponse 401 redirige vers `/login`. JWT signé avec PyJWT (HS256/384/512 seulement), mots de passe hachés avec `bcrypt` directement (compatible avec les empreintes passlib existantes). `JWT_SECRET_KEY` : 32 caractères au moins.
- Connexion : 5 échecs en 5 minutes par IP ou par e-mail bloquent les essais (429). Compteur en mémoire du processus (`core/login_throttle.py`) : prévoir un stockage partagé si plusieurs processus.
- Import CSV : 5 Mo au plus ; e-mail validé et mis en minuscules, téléphone normalisé (chiffres seuls, `+` initial gardé) ; contacts et liens traités par lots ; une ligne dont l'e-mail et le téléphone désignent deux contacts différents est une erreur. Lien campagne-contact unique (`uq_campaign_contacts_campaign_contact`).
- Toute nouvelle migration Alembic se teste sur une base vide ; une modification de modèle sans migration est une erreur.
