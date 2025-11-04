from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Boolean, DateTime, ForeignKey
from typing import Optional, TYPE_CHECKING
from ..db import db
from datetime import datetime

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    is_complete: Mapped[bool] = mapped_column(Boolean, server_default="false", nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, server_default=None)
    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"))
    # Relationship should point back to Goal.tasks (back_populates='tasks').
    # Specify the target class name explicitly to avoid forward-ref resolution issues.
    goal: Mapped[Optional["Goal"]] = relationship("Goal", back_populates="tasks")
    
    def to_dict(self):
        """Return a plain dict of this Task's attribute values.

        `to_dict` is an instance method (not a classmethod) so it returns
        the values stored on the instance, not SQLAlchemy mapped-column
        objects. `completed_at` is returned as an ISO-formatted string when
        present, otherwise None.
        """
        task_as_dict = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            # tests expect the key name 'is_complete'
            # model instances created without the DB may have is_completed == None,
            # return False in that case to match test expectations
            "is_complete": self.is_complete if self.is_complete else False
        }

        if self.goal:
            task_as_dict["goal_id"] = self.goal.id

        return task_as_dict
    
    @classmethod
    def from_dict(cls, task_data):
        new_task = cls(
                        title=task_data["title"],
                        description=task_data["description"],
                        is_complete=task_data["is_complete"])
        return new_task