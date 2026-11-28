"""Create foundation-only service metadata; no household schema is approved here."""
from alembic import op
import sqlalchemy as sa

revision = "0001_service_state"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("service_state", sa.Column("key", sa.String(100), primary_key=True),
                    sa.Column("value", sa.Text(), nullable=False))


def downgrade():
    op.drop_table("service_state")
