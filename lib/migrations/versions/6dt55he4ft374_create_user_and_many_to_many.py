# lib/migrations/versions/6dt55he4ft374_create_user_and_many_to_many.py
"""create user and many-to-many

Revision ID: <new_revision_id>
Revises: a28af33e6866
Create Date: <current_timestamp>

"""
from alembic import op # type: ignore
import sqlalchemy as sa # type: ignore
from sqlalchemy.sql import func # type: ignore

# revision identifiers, used by Alembic.
revision = '5d4e1f7a2b91' # Use a unique ID (e.g., 5d4e1f7a2b91)
down_revision = 'a28af33e6866'
branch_labels = None
depends_on = None

user_game_association_table = sa.Table(
    "user_games",
    sa.MetaData(),
    sa.Column("user_id", sa.ForeignKey("users.id"), primary_key=True),
    sa.Column("game_id", sa.ForeignKey("games.id"), primary_key=True),
)

def upgrade() -> None:
    # 1. Create the 'users' table
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), onupdate=sa.func.now()),
    )

    # 2. Create the 'user_games' association table
    op.create_table(
        "user_games",
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id")),
        sa.Column("game_id", sa.Integer(), sa.ForeignKey("games.id")),
    )

    # 3. Add user_id column to 'reviews' table
    op.add_column("reviews", sa.Column("user_id", sa.Integer()))

    # 4. Create the foreign key constraint
    op.create_foreign_key(
        "fk_user_id_reviews",
        "reviews",
        "users",
        ["user_id"],
        ["id"],
    )

def downgrade() -> None:
    # 1. Drop the foreign key constraint
    op.drop_constraint("fk_user_id_reviews", "reviews", type_="foreignkey")

    # 2. Remove the user_id column from 'reviews' table
    op.drop_column("reviews", "user_id")

    # 3. Drop the 'user_games' association table
    op.drop_table("user_games")

    # 4. Drop the 'users' table
    op.drop_table("users")