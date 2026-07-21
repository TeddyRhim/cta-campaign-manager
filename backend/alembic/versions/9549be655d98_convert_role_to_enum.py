"""convert role to enum

Revision ID: 9549be655d98
Revises: 5ba2de46bf79
Create Date: 2026-07-21 12:58:55.884995

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9549be655d98'
down_revision: Union[str, Sequence[str], None] = '5ba2de46bf79'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    user_role_enum = sa.Enum(
        'ADMIN',
        'OPERATOR',
        name='userrole'
    )

    user_role_enum.create(
        op.get_bind()
    )

    op.execute(
        """
        ALTER TABLE users
        ALTER COLUMN role TYPE userrole
        USING role::userrole
        """
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.alter_column(
        'users',
        'role',
        existing_type=sa.Enum(
            'ADMIN',
            'OPERATOR',
            name='userrole'
        ),
        type_=sa.VARCHAR(),
        existing_nullable=False
    )

    user_role_enum = sa.Enum(
        'ADMIN',
        'OPERATOR',
        name='userrole'
    )

    user_role_enum.drop(
        op.get_bind()
    )
