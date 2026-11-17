import os

os.environ.setdefault("APP_ENV", "test")
os.environ.setdefault("DATABASE_URL", "postgresql+psycopg://warik:warik_dev_only@localhost:5432/warik")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")
