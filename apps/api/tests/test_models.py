from app import models  # noqa: F401
from app.db import Base


def test_phase_one_schema_registers_required_tables() -> None:
    expected = {
        "users",
        "tasks",
        "actions",
        "approvals",
        "memories",
        "integrations",
        "ledger_events",
    }

    assert expected.issubset(Base.metadata.tables.keys())


def test_ledger_and_approval_tables_have_explicit_security_fields() -> None:
    approval_columns = Base.metadata.tables["approvals"].columns
    ledger_columns = Base.metadata.tables["ledger_events"].columns

    assert "token_hash" in approval_columns
    assert "expires_at" in approval_columns
    assert "event_hash" in ledger_columns
    assert "previous_hash" in ledger_columns
