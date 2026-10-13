"""unique campaign contact link

Revision ID: 4f2c1a9d7e10
Revises: e3b6b67a7145
Create Date: 2026-10-13 17:30:00

"""
from collections.abc import Sequence

from alembic import op

revision: str = "4f2c1a9d7e10"
down_revision: str | Sequence[str] | None = "e3b6b67a7145"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Supprime les liens en double déjà présents (on garde le plus ancien) avant la contrainte.
    op.execute(
        """
        DELETE FROM campaign_contacts a
        USING campaign_contacts b
        WHERE a.campaign_id = b.campaign_id
          AND a.contact_id = b.contact_id
          AND a.id > b.id
        """
    )
    op.create_unique_constraint(
        "uq_campaign_contacts_campaign_contact",
        "campaign_contacts",
        ["campaign_id", "contact_id"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_campaign_contacts_campaign_contact", "campaign_contacts", type_="unique"
    )
