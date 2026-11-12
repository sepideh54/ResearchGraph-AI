"""remove filename from papers

Revision ID: 8c57578ac620
Revises: 9ff0f5a43039
"""

from typing import Sequence, Union

from alembic import op

revision: str = "8c57578ac620"
down_revision: Union[str, Sequence[str], None] = "9ff0f5a43039"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column("papers", "filename")


def downgrade() -> None:
    op.add_column(
        "papers",
        op.Column("filename", op.String(length=255), nullable=True),
    )