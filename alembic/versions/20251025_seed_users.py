from alembic import op
from sqlalchemy.orm import Session
from app.models.user import User
import uuid
from typing import Sequence, Union

from app.utils.security import hash_password

revision = "20251025_seed_users"
down_revision: Union[str, Sequence[str], None] = "d7c0cc3cbfe3"
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    session = Session(bind=bind)

    admin = User(
        id=uuid.uuid4(),
        name="Admin User",
        email="admin@example.com",
        password=hash_password("admin123"),
        is_admin=True
    )

    worker = User(
        id=uuid.uuid4(),
        name="Worker User",
        email="worker@example.com",
        password=hash_password("worker123"),
        is_admin=False
    )

    session.add_all([admin, worker])
    session.commit()


def downgrade():
    bind = op.get_bind()
    session = Session(bind=bind)

    session.query(User).filter(User.email.in_(["admin@example.com", "worker@example.com"])).delete()
    session.commit()