"""add lead idempotency key

Revision ID: 7b1d91a4e2f0
Revises: 2cb455e93ac7
Create Date: 2026-09-24
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "7b1d91a4e2f0"
down_revision: Union[str, Sequence[str], None] = "2cb455e93ac7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "leads",
        sa.Column(
            "idempotency_key",
            sa.String(length=128),
            nullable=True,
        ),
    )
    op.create_index(
        "ix_leads_idempotency_key",
        "leads",
        ["idempotency_key"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index("ix_leads_idempotency_key", table_name="leads")
    op.drop_column("leads", "idempotency_key")
