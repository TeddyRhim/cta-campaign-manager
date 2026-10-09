"""create contacts table

Revision ID: 7272833257f1
Revises: e1bad1351106
Create Date: 2026-07-22 15:29:17.297078

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7272833257f1'
down_revision: Union[str, Sequence[str], None] = 'e1bad1351106'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema.

    Cette migration créait une seconde fois la table ``contacts`` : la révision
    précédente (e1bad1351106, nommée à tort « create campaign table ») la crée déjà.
    Elle est conservée, vide, pour ne pas casser l'historique des bases existantes.
    """


def downgrade() -> None:
    """Downgrade schema (rien à défaire, voir upgrade)."""
