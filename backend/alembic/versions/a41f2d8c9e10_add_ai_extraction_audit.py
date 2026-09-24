"""add ai extraction audit fields

Revision ID: a41f2d8c9e10
Revises: 7b1d91a4e2f0
Create Date: 2026-09-24
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "a41f2d8c9e10"
down_revision: Union[str, Sequence[str], None] = "7b1d91a4e2f0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "leads",
        sa.Column(
            "missing_fields",
            sa.JSON(),
            nullable=False,
            server_default=sa.text("'[]'"),
        ),
    )
    op.add_column(
        "leads",
        sa.Column(
            "ambiguous_fields",
            sa.JSON(),
            nullable=False,
            server_default=sa.text("'[]'"),
        ),
    )
    op.add_column(
        "leads",
        sa.Column(
            "ai_prompt_version",
            sa.String(length=50),
            nullable=True,
        ),
    )
    op.alter_column("leads", "missing_fields", server_default=None)
    op.alter_column("leads", "ambiguous_fields", server_default=None)


def downgrade() -> None:
    op.drop_column("leads", "ai_prompt_version")
    op.drop_column("leads", "ambiguous_fields")
    op.drop_column("leads", "missing_fields")
