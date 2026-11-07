
"""Database models for the Flask Task Manager."""

from datetime import datetime, timezone

from flask_sqlalchemy import SQLAlchemy


# Create our database object.
# We will connect it to our Flask application later.
db = SQLAlchemy()


class Task(db.Model):
    """Represent one task stored in PostgreSQL."""

    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.UUID(as_uuid=True), nullable=True)
    title = db.Column(db.String(80), nullable=False)
    category_id = db.Column(
    db.Integer,
    db.ForeignKey("categories.id", ondelete="SET NULL"),
    nullable=True,
)
    is_complete = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
    )
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

class Category(db.Model):
    """Represent one category stored in PostgreSQL."""

    __tablename__ = "categories"
    __table_args__ = (
        db.UniqueConstraint(
            "user_id",
            "name",
            name="uq_categories_user_id_name",
        ),
    )
    # user_id identifies the catefory's owner,
    # name identifies the category.
    # UniqueConstraint prevents the same user from having two categories with
    # exactly the same name.
    # Different users can still create categories with identical names

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.UUID(as_uuid=True), nullable=True)
    name = db.Column(db.String(40), nullable=False)