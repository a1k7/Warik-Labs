"""Initial relational schema for the Warik execution runtime.

Revision ID: 0001_initial
Revises:
Create Date: 2026-11-17
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("phone_e164", sa.String(20)),
        sa.Column("display_name", sa.String(120)),
        sa.Column("preferred_language", sa.String(16), nullable=False, server_default="en-IN"),
        sa.Column("timezone", sa.String(64), nullable=False, server_default="Asia/Kolkata"),
        sa.Column("consent_version", sa.String(32)),
        sa.Column("consented_at", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True)),
    )
    op.create_index("ix_users_phone_e164", "users", ["phone_e164"], unique=True)

    op.create_table(
        "tasks",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("channel", sa.String(24), nullable=False, server_default="dashboard"),
        sa.Column("external_message_id", sa.String(160)),
        sa.Column("idempotency_key", sa.String(128)),
        sa.Column("title", sa.String(240), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("status", sa.String(32), nullable=False, server_default="queued"),
        sa.Column("priority", sa.Integer(), nullable=False, server_default="3"),
        sa.Column("budget_paise", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("cost_paise", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("user_id", "idempotency_key", name="uq_tasks_user_idempotency"),
    )
    op.create_index("ix_tasks_user_status_created", "tasks", ["user_id", "status", "created_at"])

    op.create_table(
        "actions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("task_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False),
        sa.Column("sequence", sa.Integer(), nullable=False),
        sa.Column("capability", sa.String(100), nullable=False),
        sa.Column("action_type", sa.String(40), nullable=False),
        sa.Column("status", sa.String(32), nullable=False, server_default="pending"),
        sa.Column("is_irreversible", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("input_json", postgresql.JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("output_json", postgresql.JSONB()),
        sa.Column("error_code", sa.String(80)),
        sa.Column("started_at", sa.DateTime(timezone=True)),
        sa.Column("completed_at", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_actions_task_sequence", "actions", ["task_id", "sequence"])

    op.create_table(
        "approvals",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("task_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False),
        sa.Column("action_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("actions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("token_hash", sa.String(128), nullable=False, unique=True),
        sa.Column("status", sa.String(16), nullable=False, server_default="pending"),
        sa.Column("requested_via", sa.String(24), nullable=False, server_default="whatsapp"),
        sa.Column("decision_via", sa.String(24)),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("decided_at", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_approvals_status_expiry", "approvals", ["status", "expires_at"])

    op.create_table(
        "memories",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("memory_path", sa.String(500), nullable=False),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("markdown_content", sa.Text(), nullable=False, server_default=""),
        sa.Column("checksum_sha256", sa.String(64)),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("sensitivity", sa.String(24), nullable=False, server_default="normal"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True)),
        sa.UniqueConstraint("user_id", "memory_path", name="uq_memories_user_path"),
    )

    op.create_table(
        "integrations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("provider", sa.String(64), nullable=False),
        sa.Column("status", sa.String(24), nullable=False, server_default="disconnected"),
        sa.Column("granted_scopes", postgresql.JSONB(), nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("credential_ref", sa.String(240)),
        sa.Column("connected_at", sa.DateTime(timezone=True)),
        sa.Column("revoked_at", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("user_id", "provider", name="uq_integrations_user_provider"),
    )

    op.create_table(
        "ledger_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("task_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tasks.id", ondelete="SET NULL")),
        sa.Column("action_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("actions.id", ondelete="SET NULL")),
        sa.Column("event_type", sa.String(80), nullable=False),
        sa.Column("actor", sa.String(32), nullable=False),
        sa.Column("payload", postgresql.JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("previous_hash", sa.String(64)),
        sa.Column("event_hash", sa.String(64), nullable=False, unique=True),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_ledger_user_occurred", "ledger_events", ["user_id", "occurred_at"])
    op.create_index("ix_ledger_task_occurred", "ledger_events", ["task_id", "occurred_at"])


def downgrade() -> None:
    op.drop_index("ix_ledger_task_occurred", table_name="ledger_events")
    op.drop_index("ix_ledger_user_occurred", table_name="ledger_events")
    op.drop_table("ledger_events")
    op.drop_table("integrations")
    op.drop_table("memories")
    op.drop_index("ix_approvals_status_expiry", table_name="approvals")
    op.drop_table("approvals")
    op.drop_index("ix_actions_task_sequence", table_name="actions")
    op.drop_table("actions")
    op.drop_index("ix_tasks_user_status_created", table_name="tasks")
    op.drop_table("tasks")
    op.drop_index("ix_users_phone_e164", table_name="users")
    op.drop_table("users")
